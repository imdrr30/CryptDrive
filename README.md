# CryptDrive
 - Simple Cryptography Tool that saves and retrives files from your G Drive with a single line of command.

## Unlimited Storage for Any Organization
- Google provides unlimited storage for Any Organization using GSuite. But the Organization has access to the files you stored on the unlimited GSuite Drive. To Prevent them accessing, We can encrpyt. CryptDrive provides you One-Line solution for this. Using oneline commands you can get unlimited storage.

## Install Dependencies
```
pip3 install google-api-python-client
pip3 install cryptography
pip3 install oauth2client
```
## Usage
- `python3 main.py setup` to generate NEWKEY based on your Password. Key will be generated and saved as `key.key` in Current active Directory. Make a Secure Backup of the key file.
- `python3 main.py push [PATH_TO_FILE]`. This Command will push the file to the Drive using default Browser.
