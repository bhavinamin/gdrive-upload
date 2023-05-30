# gdrive-upload
Python script to zip up directories and upload to Google Drive using a service account


main.py - uses service-account-credentials.json to auth into Google, zip up files, upload into the service accounts root folder and then move the file from the root folder into either a shared folder or wherever else you desire by specifying a folder_id (found in URL)

common-gdrive-functions.txt - code snippets in case we need to create folders or set folder permissions in Gdrive



Notes: 
  - service accounts cred json file won't be OAuth (clientid + secret), it will be an actual service account within GCP
  - this script is dependent on the Google Client Library for Python to be installed on the local system 
     
     `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthli`

