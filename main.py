from __future__ import print_function

import subprocess
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from apiclient.http import MediaFileUpload



def get_service(api_name, api_version, scopes, key_file_location): 
    credentials = service_account.Credentials.from_service_account_file(key_file_location)
    scoped_credentials = credentials.with_scopes(scopes)
    service = build(api_name, api_version, credentials=scoped_credentials)

    return service

def get_mac_backup(): 
    hostname = subprocess.check_output("hostname | awk -F \. '{print $1}'", shell=True).decode('ascii').strip() 
    current_user = subprocess.check_output("scutil <<< \"show State:/Users/ConsoleUser\" | awk '/Name :/ && ! /loginwindow/ { print $3}'", shell=True).decode('ascii').strip()

    zip_name = f"{current_user}@{hostname}.zip"

    print(zip_name)
    zip_cmd = f"cd /Users/{current_user} && rm -f {zip_name} && zip -r {zip_name} Documents Desktop Downloads"
    copy_cmd = f"mv /Users/{current_user}/{zip_name} {zip_name}"

    os.system(zip_cmd)
    os.system(copy_cmd)
    

    
    if os.path.exists(zip_name): 
        return zip_name
    else: 
        return False
    
     

def main():
    zip_name = get_mac_backup()
    folder_id = "1##########" #Gdrive folder to move the file into

    scope = 'https://www.googleapis.com/auth/drive'
    key_file_location = 'service-accounts-credentials.json'

    if (zip_name): 
        #Create the gdrive service 
        try: 
            service = get_service(
                api_name='drive', 
                api_version='v3', 
                scopes=[scope],
                key_file_location=key_file_location)
            
            file_metadata = {
                'name': zip_name, 
                'mimeType': '*/*'
            }
                     
            #Upload the file
            media = MediaFileUpload(zip_name, mimetype='*/*', resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute() 
            file_id = file.get('id')
            
            #Move to shared folder
            # Retrieve the existing parents to remove
            uploaded_file = service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(uploaded_file.get('parents'))
            
            return service.files().update(
                    fileId=file_id,
                    addParents=folder_id,
                    removeParents=previous_parents,
                    fields='id, parents'
                ).execute()           
        
        
        except HttpError as error: 
            print(f'Error:  {error}')


if __name__ == '__main__':
    main()
