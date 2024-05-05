from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Milvus
import os

###################################################### for conversation history
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
###############################################################################

class ai_chat:
    def __init__(self, url, place, language, ai_role, user_role, session_id):
        load_dotenv()

        OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

        ######################################################### scrape and parse info
        # taken as param xxxurl = "https://en.wikipedia.org/wiki/Star_Wars"

        headers_to_split_on = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
            ("h4", "Header 4"),
            ("div", "Divider")
        ]

        html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        html_header_splits = html_splitter.split_text_from_url(url)

        chunk_size = 1024
        chunk_overlap = 128
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        # Split
        splits = text_splitter.split_documents(html_header_splits)

        llm = OctoAIEndpoint(
                model_name="llama-2-13b-chat-fp16",
                max_tokens=1024,
                presence_penalty=0,
                temperature=0.1,
                top_p=0.9,
                
            )
        embeddings = OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings")

        ############################################################# store information
        vector_store = Milvus.from_documents(
            splits,
            embedding=embeddings,
            connection_args={"host": "localhost", "port": 19530},
            collection_name="starwars"
        )

        retriever = vector_store.as_retriever()
        ###############################################################################

        ######################################################## Contextualize question
        contextualize_q_system_prompt = """Given a chat history and the latest user response \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        ################################################################# prompt set up
        template="""You are an assistant for role-playing tasks. Respond in """ + language + """. \
        The setting is""" + place + """, you are """ + ai_role + """ and the user is """ + user_role + """ \
        Use the following pieces of retrieved context to continue the conversation. \
        Use three sentences maximum and keep the answer concise.

        {context}"""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm, prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        ######################################################## chat history managment - https://python.langchain.com/docs/use_cases/question_answering/chat_history/
        self.store = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]


        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        self.session_id = session_id

    ################################################################## conversation

    # prompts user for input based on given string prompt
    # returns string of user response
    # session id example: "abc123"
    def getAIResponse(self, user_input):
        ai_response = self.conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": self.session_id}},
            )["answer"]
        return ai_response