# CryptDrive
Simple Cryptography Tool that saves and retrives files from your G Drive with a single line of command. Make use of unlimited cloud storage provided by Google.

## Unlimited Storage for Any Organization
Google provides unlimited storage for Any Organization using GSuite. But the Organization has access to the files you stored on the unlimited GSuite Drive. To Prevent them accessing, We can encrpyt. CryptDrive provides you One-Line solution for this. Using oneline commands you can get unlimited storage.

## Install Dependencies
```
pip3 install google-api-python-client
pip3 install cryptography
pip3 install oauth2client
```
## Usage
### First things first
- Get your own API-KEY from Google, `credentials.json` file will be generated. Place that in the working directory along with source code.
- Use [this link](https://developers.google.com/drive/api/v3/quickstart/python) to generate your own `credentials.json`. Click Enable Google Drive API to Generate.
- Since, all the Authentication process is taken care by Google we have access only to API. 
- `credentials.json` Contains only API-KEY.

### One-Line Wonders
- `python3 main.py setup` to generate NEWKEY based on your Password. Key will be generated and saved as `key.key` in Current active Directory. Make a Secure Backup of the key file.
- `python3 main.py push [PATH_TO_FILE]`. This Command will push the file to the Drive using default Browser.
- `python3 main.py pull [FILE_NAME_OF_THE_ENCRYPTED_PUSHED_TO_DRIVE]` to pull the file to the working directory.
- Make sure `key.key` file is placed in working directory.
