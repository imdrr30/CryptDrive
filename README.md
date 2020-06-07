# CryptDrive
Simple Cryptography Tool that saves and retrives files from your G Drive with a single line of command. Make use of unlimited cloud storage provided by Google.

## Unlimited Storage for Any Organization
Google provides unlimited storage for Any Organization using GSuite. But the Organization has access to the files you stored on the unlimited GSuite Drive. To Prevent them accessing, We can encrpyt. CryptDrive provides you One-Line solution for this. Using oneline commands you can get unlimited storage.

## Installation
```
pip3 install CryptDrive
```
## Usage
### First things first
- Get your own API-KEY from Google, `credentials.json` file will be generated. Place that in the working directory along with source code.
- Use [this link](https://developers.google.com/drive/api/v3/quickstart/python) to generate your own `credentials.json`. 
- Click Enable Google Drive API to Generate.
- Choose `Desktop App` from the dropdown.
- Then Click `Download Client Configuration`. 
- `credentials.json` will be downloaded.
- Since, all the Authentication process is taken care by Google we have access only to API. 
- `credentials.json` Contains only API-KEY.
### Setup KEY
- `from CryptDrive import CryptDrive`
- `CryptDrive.setup()` to generate NEWKEY based on your Password. Key will be generated and saved as `key.key` in Current active Directory. 
- Make a Secure Backup of the key file. If it is lost, your data cant be retreived.
- Make sure `key.key` file is placed in working directory.
### One-Line Wonders
- `CryptDrive.push(PATH_TO_FILE)`. This Command will encrypt push the file to the Drive using default Browser.
- `CryptDrive.pull(FILE_NAME_OF_THE_ENCRYPTED_PUSHED_TO_DRIVE)` to decrypt pull the file to the working directory.
- `CryptDrive.pushdir(PATH_TO_DIR)`- To encrypt and push directory and its files to Google Drive.
- `CryptDrive.decrypt(PATH_TO_FILE)` - To decrpt encrypted file locally.
- `CryptDrive.encrypt(PATH_TO_FILE)` - To encrypt file locally.
- `CryptDrive.decryptdir(PATH_TO_FOLDER)` - To decrpt encrypted folder locally.
- `CryptDrive.encryptdir(PATH_TO_FOLDER)` - To encrypt folder locally.
- `CryptDrive.mkdir(NEW_DIR_NAME_IN_GDRIVE)` - To Create NEW directory in google drive
- `CryptDrive.lookfor(FILE_NAME)` - To search in Google Drive
- Make sure `key.key` file is placed in working directory.
