from __future__ import print_function
import pickle
import os.path, io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import sys
from cryptserve import *
parents_id=[]



SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service
    service = build('drive', 'v3', credentials=creds)

def mkdir(name):
    main()
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get('id')

def createFolder(name,parents):
    main()
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder', 'parents' : parents
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get('id')



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


def push(name, namepath,parents):
    check()
    main()
    encrypt(name,namepath)
    file_metadata = {'name': '{}.bcpt'.format(name), 'parents': parents}
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



def searchFile(query):
    main()
    page_token = None
    while True:
        response = service.files().list(q="name contains '{}'".format(query),
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name, size, modifiedTime)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            print('Found file: %s %.2fMB %s' % (file.get('name'),int(file.get('size'))/(1048576),file.get('modifiedTime')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

def check():
    main()
    page_token = None
    while True:
        response = service.files().list(q="name contains 'CryptDrive'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name, mimeType)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            if 'application/vnd.google-apps.folder'==file.get('mimeType'):
                parents_id.append(file.get('id'))
                break
            else:
                continue
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

def pushdir(dir):
    check()
    a = os.path.split(dir)
    par = ['{}'.format(createFolder(a[-1],parents_id))]
    for item in os.listdir(dir):
        push(item, "{}/{}".format(dir,item),par)


if __name__ == '__main__':
    try:
        if 'setup' in sys.argv:
            setup()
        elif sys.argv[1]=='push':
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
            push(name, path,parents_id)
        elif sys.argv[1] == 'pull':
            pull("{}.bcpt".format(sys.argv[2]), sys.argv[2])
        elif sys.argv[1] == 'mkdir':
            mkdir(sys.argv[2])
        elif sys.argv[1] == 'lookfor':
            searchFile(sys.argv[2])
        elif sys.argv[1] == 'pushdir':
            pushdir(sys.argv[2])
    except:
        print("""        Usage python3 main.py setup - To Generate KEYFILE
        python3 main.py push [PATH_TO_FILE] - To encrypt and push file to Google Drive.
        python3 main.py pull [FILE_NAME_SAVED_IN_DRIVE] - To decrypt and pull file from Google Drive
        python3 main.py pushdir [PATH_TO_DIR] - To encrypt and push directory and its files to Google Drive
        python3 main.py mkdir [NEW_DIR_NAME_IN_GDRIVE] - To Create NEW directory in google drive
        python3 main.py lookfor [FILE_NAME] - To search in Google Drive""")