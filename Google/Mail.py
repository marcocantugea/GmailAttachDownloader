# Author: Marco Cantu Gea
# Clase para las operaciones del lecura de mensajes del correo
# Version 0.0.1

from Google.Client import ClientLoader
from Configurations.Loader import Loader
from pathlib import Path
import base64
from Storage.LocalStorage import LocalStorage


class EmailReader:
    _USER_ID = "me"
    _FILES_FOUND = []
    _FOLDER_FORFILES = "Downloads"

    def __init__(self):
        pass

    @classmethod
    def getMessages(cls, token=None):

        client = ClientLoader().getClient()
        max_result = Loader.get_config("maxRequestEmails")
        query = Loader.get_config("mailQuery")
        gmailLabels = Loader.get_config("GmailsLables")
        next_page_token = token is None and None or token

        if next_page_token is None:
            result = client.users().messages().list(maxResults=max_result,
                                                    userId=cls._USER_ID,
                                                    q=query,
                                                    labelIds=gmailLabels).execute()
        else:
            result = client.users().messages().list(maxResults=max_result,
                                                    userId=cls._USER_ID,
                                                    q=query,
                                                    labelIds=gmailLabels, pageToken=token).execute()
        messages = result.get('messages')
        next_page_token =result.get('nextPageToken')

        # obtiene la informacion de los mensajes y los archivos adjuntos
        for msg in messages:
            # una vez obtenido los id de los mensajes obtenemos el mensaje
            email_message = client.users().messages().get(userId=cls._USER_ID, id=msg['id']).execute()

            try:
                payload = email_message['payload']
                parts = payload.get('parts')

                cls._getIDAttachments(msg['id'], parts)

            except:
                print("Error getting the messages from GMAIL API")

        if next_page_token is not None:
            cls.getMessages(next_page_token)

        # una vez recolectada la informacion obtiene el contenido de los archivos adjuntos recolectados
        # guardamos los archivos en el folder configurado
        cls._getAttchmentData()._savePhisicalFiles()

    @classmethod
    def _getIDAttachments(cls, messageId, parts):

        if not parts:
            return None

        for part in parts:
            if part['filename']:
                item = {
                    'messageID': messageId,
                    'AttachmentId': part['body']['attachmentId'],
                    'fileName': part['filename'],
                    'mimeType': part['mimeType'],
                    'size': 0,
                    'data': ""
                }
                cls._FILES_FOUND.append(item)

        return cls

    @classmethod
    def _getAttchmentData(cls):

        if len(cls._FILES_FOUND) <= 0:
            return None

        index = 0
        for item in cls._FILES_FOUND:
            client = ClientLoader().getClient()
            result = client.users().messages().attachments().get(userId=cls._USER_ID,
                                                                 messageId=item['messageID'],
                                                                 id=item['AttachmentId']).execute()

            cls._FILES_FOUND[index]['size'] = result['size']
            cls._FILES_FOUND[index]['data'] = result['data']
            index += 1

        return cls

    @classmethod
    def _savePhisicalFiles(cls):

        if len(cls._FILES_FOUND) <= 0:
            return None

        index = 0
        for item in cls._FILES_FOUND:

            try:
                file = LocalStorage(cls._FOLDER_FORFILES)
                file.setFileName(item['fileName'])
                content = base64.urlsafe_b64decode(item['data'].encode('utf-8'))
                file.saveFileContent(content=content, mode="wb")
                print(f"File Saved {item['fileName']}")

            except:
                print(f"Fail to save the file {item['fileName']}")

        return cls

    def setFolderForFiles(self, folderPath):
        if not Path(folderPath).exists():
            raise NameError("The selected folder do not exist")

        self._FOLDER_FORFILES = folderPath

        return self
