# Author: Marco Cantu Gea
# Clase para obtener el servicio del cliente de google
# Version 0.0.1

import pickle
from Storage.LocalStorage import LocalStorage
from json import loads, dumps
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class ClientLoader:

    _CREDENTIALS_PATH = "credentials"
    _CREDENTIALS_FILENAME = "client_secret.json"
    _TOKEN_PATH = _CREDENTIALS_PATH
    _TOKEN_FILENAME = "token.pickle"
    _SCOPE = ['https://www.googleapis.com/auth/gmail.readonly']
    _CREDENTIALS = None
    _TOKEN = None
    _CLIENT = None

    def __init__(self):
        self._loadCredentials()

    @classmethod
    def getClient(cls):
        # cargamos el token
        cls._loadToken()
        #si el token no existe abre la pagina de autentificacion o si existe y requiere actualizarse se actualiza el
        #token
        if not cls._TOKEN or not cls._TOKEN.valid:
            credentias_file=cls._CREDENTIALS_PATH+"/"+cls._CREDENTIALS_FILENAME
            flow = InstalledAppFlow.from_client_secrets_file(credentias_file, cls._SCOPE)
            cls._TOKEN=flow.run_local_server(port=0)
            cls.updateTokenFile()
        elif cls._TOKEN and cls._TOKEN.expired and cls._TOKEN.refresh_token:
            cls._TOKEN.refresh(Request())

        cls._CLIENT = build('gmail', 'v1', credentials=cls._TOKEN)

        return cls._CLIENT

    # Carga las credenciales de un archivo json
    @classmethod
    def _loadCredentials(cls):
        local_storage = LocalStorage(cls._CREDENTIALS_PATH)
        local_storage.setFileName(cls._CREDENTIALS_FILENAME)

        if not local_storage.existFile():
            raise NameError("missing file for credentials")

        file_content = local_storage.getFileContent()
        cls._CREDENTIALS = loads(file_content)

        return cls

    # Carga el token del archivo json
    @classmethod
    def _loadToken(cls):
        local_storage = LocalStorage(cls._TOKEN_PATH)
        local_storage.setFileName(cls._TOKEN_FILENAME)

        if not local_storage.existFile():
            return False

        token_file=cls._TOKEN_PATH+"/"+cls._TOKEN_FILENAME
        with open(token_file, 'rb') as token:
            cls._TOKEN =pickle.load(token)

        return cls

    @classmethod
    def updateTokenFile(cls):
        with open(cls._TOKEN_PATH+'/'+cls._TOKEN_FILENAME, 'wb') as token:
            pickle.dump(cls._TOKEN, token)

        return cls

    def setCredentialsPath(self,credentialPath):
        self._CREDENTIALS_PATH=credentialPath
        return self

    def getCredentialsPath(self):
        return self._CREDENTIALS_PATH

    def setCredentialFileName(self, credentialFileName):
        self._CREDENTIALS_FILENAME=credentialFileName
        return self

    def setTokenPath(self, tokenPath):
        self._TOKEN_PATH= tokenPath
        return self

    def getTokenPath(self):
        return self._TOKEN_PATH

    def setTokenFileName(self, tokenFileName):
        self._TOKEN_FILENAME= tokenFileName
        return self

    def getTokenFileName(self):
        return self._TOKEN_FILENAME



