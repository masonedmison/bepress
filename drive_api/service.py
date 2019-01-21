from __future__ import print_function
from drive_api.auth import Auth
from googleapiclient.http import MediaFileUpload


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


class Service(object):
    def __init__(self):
        auth = Auth(SCOPES)
        self.service = auth.get_service()

    def get_results(self):
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

    def upload_file(self, filepath, filename, mimetype):
        file_metadata = {
            'name': filename,
        }
        media = MediaFileUpload(filepath,
                                mimetype=mimetype,
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))

    def create_folder(self, folder_name):
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=folder_metadata,
                                            fields='id').execute()
        return 'Folder ID: %s' % file.get('id')

    def insert_to_folder(self, folder_id, file_name, file_path):
        folder_id = folder_id
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path,
                                mimetype='image/jpeg',
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        print('File ID: %s' % file.get('id'))
        return file.get('id')


if __name__ == '__main__':
    service = Service()
    #service.get_results()
    folder_id = service.create_folder('zuck_thumbnails')
    folder_id = '9tcjTyAhjJ2G7VrlgLbiiMiac4c6V6XC'
    print(folder_id)


