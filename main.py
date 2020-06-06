from __future__ import print_function
import pickle
import os.path, io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import sys
from cryptserve import *

SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service
    service = build('drive', 'v3', credentials=creds)


def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))



def pull(name,orgi):
    puller(10,"name contains '{}'".format(name), name,orgi)


def puller(size,query,name,orgi):
    main()
    results = service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            print(item)
            print(item['id'])
        request = service.files().get_media(fileId=item['id'])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(item['name'], 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
            decrypt(name,orgi)


def push(name, namepath):
    main()
    encrypt(name,namepath)
    file_metadata = {'name': '{}.bcpt'.format(name)}
    media = MediaFileUpload('{}.bcpt'.format(name),
                            mimetype='application/octet-stream')
    print("fileuploading")
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))
    os.remove('{}.bcpt'.format(name))

def setup():
    if new(input("Please Enter New Password to generate Key: ")):
        print("Key Generated Successfully and saved as key.key")
    else:
        print("Key is not Generated. Please Try again..")

if __name__ == '__main__':
    if 'setup' in sys.argv:
        setup()
    if sys.argv[1]=='push':
        data = sys.argv[2]
        i = -1
        while True:
            try:
                if data[i] == '/':
                    break
                i += -1
            except IndexError:
                name = data
                path = data
                break
        name = data[i + 1:]
        path = data
        push(name, path)
    if sys.argv[1] == 'pull':
        pull("{}.bcpt".format(sys.argv[2]), sys.argv[2])