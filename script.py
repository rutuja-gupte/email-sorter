import base64
from email.message import EmailMessage

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from bs4 import BeautifulSoup as bs

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
           
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        print("Accessed. Yay!")
        return creds

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

def check_messages(creds):
    service = build("gmail", "v1", credentials=creds)
    key = service.users().messages()
    messages = key.list(userId="me").execute().get("messages")
    message_id = [item['id'] for item in messages]

    # accessing the messages gives dict with payload that has a messagepart object
    # MessagePart object had body key with MessagePartBody object
    # MessagePart object has data key in base64
    final_message_list = []
    heads = []
      
    for msg_id in message_id:
        try:
            msg = key.get(userId="me", id=msg_id).execute().get('payload').get('parts')[0].get('body').get('data')
            msg2 = str(base64.urlsafe_b64decode(msg), encoding='utf-8')
            final_msg = bs(msg2, "html.parser").get_text()

        except:
            msg = key.get(userId="me", id=msg_id).execute().get('payload').get('body').get('data')
            msg2 = str(base64.urlsafe_b64decode(msg), encoding='utf-8')
            final_msg = bs(msg2, "html.parser").get_text()
        
        head = key.get(userId="me", id=msg_id).execute().get('payload').get('headers')
        head_new = {d['name']:d['value'] for d in head if d['name'] in ['From', 'Date', 'Subject', 'To']}
        heads.append(head_new)
        final_message_list.append(final_msg)
    
    return heads, final_message_list

if __name__ == "__main__":
    creds = authenticate()
    messages = check_messages(creds)