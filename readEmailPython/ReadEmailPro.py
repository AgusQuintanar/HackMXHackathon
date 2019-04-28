from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
   
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    

    if not messages:
        print("No messages found.")
    else:
        msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
        correo = msg['snippet']
        
        import re
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', correo)
        correo = correo.split()
        palabras = [(correo[x].lower()) for x in range(len(correo)) if correo[x] not in urls ]
        print("Correo: ",correo)
        print("Urls: ",urls)
        print("Palabras: ",palabras)


if __name__ == '__main__':
    main()