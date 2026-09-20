# dashboard/gdrive_vault.py - Direct Google Drive Cloud API Vault
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveCloudVault:
    def __init__(self, credentials_path="credentials.json", token_path="token.pickle"):
        self.credentials_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", credentials_path)
        self.token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", token_path)
        self.service = None
        self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(self.token_path):
            try:
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
            except Exception as e:
                print(f"[!] Error loading token.pickle: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    creds = None
            if not creds and os.path.exists(self.credentials_path):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open(self.token_path, 'wb') as token:
                        pickle.dump(creds, token)
                except Exception as ex:
                    print(f"[!] OAuth Flow error: {ex}")
            elif not creds:
                print("[!] credentials.json not found in root directory. Operating in local-sync mode.")
                return

        if creds and creds.valid:
            try:
                self.service = build('drive', 'v3', credentials=creds)
                print("[+] Google Drive Cloud API Connected Successfully!")
            except Exception as e:
                print(f"[!] Failed to build Drive service: {e}")

    def upload_artifact(self, file_path, folder_id=None):
        if not self.service or not os.path.exists(file_path):
            print(f"[*] Cloud API offline or file missing. File saved locally: {file_path}")
            return f"Saved locally: {file_path}"
            
        try:
            file_name = os.path.basename(file_path)
            file_metadata = {'name': file_name}
            if folder_id:
                file_metadata['parents'] = [folder_id]

            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
            
            cloud_link = file.get('webViewLink')
            print(f"[+] Direct Cloud Upload Complete! Link: {cloud_link}")
            return cloud_link
        except Exception as ex:
            print(f"[!] Cloud upload error: {ex}")
            return f"Saved locally: {file_path}"

drive_cloud_vault = GoogleDriveCloudVault()