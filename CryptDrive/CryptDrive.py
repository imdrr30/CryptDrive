from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

parents_id = []

SCOPES = ['https://www.googleapis.com/auth/drive']

def new(uinp):
    password = uinp.encode() # Convert to type bytes
    salt=os.urandom(256)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    file = open('key.key', 'wb')
    file.write(key)
    file.close()
    return True

def decrypter(name,orgi):
    file = open(name, 'rb')
    filedata = file.read()
    print("File Opened")
    file.close()
    file2 = open('key.key', 'rb')
    print("Key Opened")
    key2 = file2.read()
    file2.close()
    ff = Fernet(key2)
    decrpd = ff.decrypt(filedata)
    with open(orgi, 'wb') as fd:
        fd.write(decrpd)
    print("Decrypted")
    os.remove(name)


def encrypter(name,namepath):
    file1 = open('key.key', 'rb')
    key = file1.read()
    print("Key opened")
    file1.close()
    file2 = open(namepath, 'rb')
    filedata = file2.read()
    print("File opened")
    file2.close()
    f = Fernet(key)
    encrpd = f.encrypt(filedata)
    with open('{}.bcpt'.format(name), 'wb') as f:
        f.write(encrpd)
        print("Encrypted")

def encrypterdir(name,namepath):
    file1 = open('key.key', 'rb')
    key = file1.read()
    print("Key opened")
    file1.close()
    file2 = open(namepath, 'rb')
    filedata = file2.read()
    print("File opened")
    file2.close()
    f = Fernet(key)
    encrpd = f.encrypt(filedata)
    with open('{}.bcpt'.format(namepath), 'wb') as f:
        f.write(encrpd)
        print("Encrypted")

def auth():
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
    auth()
    file_metadata = {
    'name' : name,
    'mimeType' : 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get('id')


def createFolder(name,parents):
    auth()
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder', 'parents' : parents
    }
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    return file.get('id')


def pull2(name,orgi):
    puller(10,"name contains '{}'".format(name), name,orgi)


def puller(size,query,name,orgi):
    auth()
    results = service.files().list(
    pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType, size)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            print(item['name'],'%.2fMB' % (int(item['size'])/1048576))
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
            decrypter(name,orgi)


def pusher(name, namepath,parents):
    check()
    auth()
    encrypter(name,namepath)
    file_metadata = {'name': '{}.bcpt'.format(name), 'parents': parents}
    media = MediaFileUpload('{}.bcpt'.format(name),
                            mimetype='application/octet-stream')
    print("File is being uploaded")
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


def lookfor(query):
    auth()
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
    auth()
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
            if parents_id == []:
                mkdir("CryptDrive")
                check()
            break


def pushdir(dir):
    check()
    a = os.path.split(dir)
    par = ['{}'.format(createFolder(a[-1],parents_id))]
    for item in os.listdir(dir):
        pusher(item, "{}/{}".format(dir,item),par)


def push(data):
    i = -1
    global name, path
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
    pusher(name, path, parents_id)


def pull(data):
    pull2("{}.bcpt".format(data), data)


def decrypt(data):
    decrypter(data, data[:-5])


def decryptdir(data):
    for file in os.listdir(data):
        decrypter('{}/{}'.format(data, file), '{}/{}'.format(data, file[:-5]))
        try:
            os.remove('{}/{}'.format(data, file))
        except:
            pass


def encrypt(data):
    encrypter(data,data)


def encryptdir(data):
    for file in os.listdir(data):
        try:
            encrypterdir(file,'{}/{}'.format(data, file))
        except:
            pass