import os
import requests

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVUTRNemhDUVVWQk1rTkJNemszUTBNMlFVVTRRekkyUmpWQ056VTJRelUxUTBVeE5EZzFNUSJ9.eyJodHRwczovL3BsYXRmb3JtLnN5bWJsLmFpL3VzZXJJZCI6IjU5ODQ5ODYxMDE1Nzk3NzYiLCJpc3MiOiJodHRwczovL2RpcmVjdC1wbGF0Zm9ybS5hdXRoMC5jb20vIiwic3ViIjoiQTQzZmcycXZXN0p3MFBmMGJUdDd2Y3lPQ0NLdVVZNW1AY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vcGxhdGZvcm0ucmFtbWVyLmFpIiwiaWF0IjoxNzE0OTM1ODMzLCJleHAiOjE3MTUwMjIyMzMsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkE0M2ZnMnF2VzdKdzBQZjBiVHQ3dmN5T0NDS3VVWTVtIn0.0Qk2NBNNInKj5QJPYwXuuA6V61bA2YTI2GZYu0H_WXKI1nLJ6RR8SUY2xXfbNRlpwcvcC_DDM7_XqcqYwd3YP0kA46xjlsKT40v4q_xkR2P15g_0XbCbYrgrXx6b9u25QUrHQ9nzC7qaMmyjZUQuXKHDd4fi9NtTM9rwzJZkXTl1_HKjvi481XRyi5OkSybXvSetpcTGAHBBQrPuwBgRKWk4E1ivYg9WB5yMFtnjfrETHcsjlQCRoMmVcUztRkxBdVBOmFNfkQpEAMvIWC6r-i8IbXjhosIpKb-lzdhrV8YjlAi6YTgY2LxWFJ8IKLB3e0LWZCbu-OsO4vlxR948jQ"
file_path = R"C:\Users\ryanj\OneDrive\Documents\Sound Recordings\Recording (2).wav"
language = "it-IT"
symblai_params = {
  "name": "Test convo 2",
  "languageCode": language
}
content_type = "audio/wav"

headers = {
  "Authorization": "Bearer " + access_token,
  "Content-Type": content_type
}

with open(file_path, "rb") as file:
  request_body = file.read()

response = requests.request(
  method="POST", 
  url="https://api.symbl.ai/v1/process/audio",
  params=symblai_params,
  headers=headers,
  data=request_body
)


transcriptor = requests.get("https://api.symbl.ai/v1/conversations/" + response.text[(response.text.find(R'"conversationId":') + 18):(response.text.find(",") - 1)] + "/messages", headers=headers)
textIndex = transcriptor.text.find('"text"') + 8
transcription = transcriptor.text[textIndex:len(transcriptor.text)]
transcription = transcription[0:transcription.find(',') - 1]
print(transcription)
