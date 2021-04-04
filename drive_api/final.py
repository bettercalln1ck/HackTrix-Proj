from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
from apiclient.http import MediaFileUpload
import os
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
import os
class g_auth:
  def __init__(self,cred_file):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    self.creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(cred_file):
        with open(cred_file, 'rb') as token:
            self.creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
                'media/client_secrets.json', SCOPES)
        self.creds = flow.run_local_server(host='http://f2332888.ngrok.io', port=80, authorization_prompt_message='Please visit this URL to authorize this application:{url}', success_message='The authentication flow has completed. You may close this window.', open_browser=False)
        # Save the credentials for the next run
        with open(cred_file, 'wb') as token:
          pickle.dump(self.creds, token)
    self.drive_service = build('drive', 'v3', credentials=self.creds)
  def list_file(self,max_size):
    # Call the Drive v3 API
    results = self.drive_service.files().list(
        pageSize=max_size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
      print('Files:')
      for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
  def upload_file(self,filename,locF):
    print(os.getcwd())
    file_metadata = {'name': filename}
    media = MediaFileUpload(locF,mimetype='image/jpeg')
    file = self.drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    def callback(request_id, response, exception):
      if exception:
        print(exception)
      else:
        print("Permission Id: %s" % response.get('id'))
    batch = self.drive_service.new_batch_http_request(callback=callback)
    user_permission = {
      'type': 'anyone',
      'role': 'reader'
    }
    batch.add(self.drive_service.permissions().create(
        fileId=file.get('id'),
        body=user_permission,
        fields='id',
    ))
    batch.execute()
    return file.get('id')
  def copy_to_drive(self,file_id,copy_name):
    copied_file = {'title': copy_name}
    try:
      return self.drive_service.files().copy(
          fileId=file_id, body=copied_file).execute()
    except errors.HttpError:
      print('An error occurred: %s' % error)

  def share_file(self,file_id,to_user):
    def callback(request_id, response, exception):
      if exception:
        print(exception)
      else:
        print("Permission Id: %s" % response.get('id'))
    batch = self.drive_service.new_batch_http_request(callback=callback)
    user_permission = {
      'type': 'user',
      'role': 'reader',
      'emailAddress': to_user
    }
    print(user_permission)
    batch.add(self.drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id',
    ))
    return batch.execute()

  def copy_file(self, origin_file_id, copy_title):
    copied_file = {'title': copy_title}
    try:
      return self.drive_service.files().copy(fileId=origin_file_id, body=copied_file).execute()
    except errors.HttpError:
      print('An error occurred: %s' % error)
    return None

  def create_folder():
     file_metadata = {
      'name': 'Invoices',
      'mimeType': 'application/vnd.google-apps.folder'
     }
     file = self.drive_service.files().create(body=file_metadata,fields='id').execute()
     print('Folder ID: %s' % file.get('id'))
     return file.get('id')

# id1='token1.pickle'
# id2='token2.pickle'
# f=g_auth('token1.pickle')
# f.share_file(file_id.to_user)
# f=g_auth('token2.pickle')
# f.copy_file(file_id,'aaa')
