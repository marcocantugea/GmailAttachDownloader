# Author: Marco Cantu Gea
# Clase para manipular archivos localmente usando rutas relativas
# Version 0.0.1


from pathlib import Path


class LocalStorage:

    def __init__(self, pathName=".", fileName=None):
        self.pathName = pathName
        self.PathObj = Path(pathName)
        self.fileName = fileName

    def setPathName(self, pathName):
        self.PathObj = Path(pathName)
        self.pathName = pathName
        return self

    def getPathName(self=None):
        return self.pathName

    def setFileName(self, fileName):
        self.fileName = fileName
        return self

    def getFileName(self):
        return self.fileName

    def getCurrentPath(self):
        return Path(".").cwd()

    def exist(self):
        return self.PathObj.exists()

    def existFile(self):
        fileToSearch = self.pathName + "/" + self.fileName
        return Path(fileToSearch).exists()

    def makeDir(self):
        if len(self.pathName) >= 3:
            self.PathObj.mkdir()

        return self

    def removeDir(self):
        if len(self.pathName) >= 3:
            self.PathObj.rmdir()
            self.pathName = ""
            self.PathObj = None

        return self

    def getPathContent(self, arg='*.*'):
        return self.PathObj.glob(arg)

    def searchFileInPath(self, fileName=None):
        foundFile = fileName is None and self.fileName or fileName
        return self.getPathContent(foundFile)

    def getFileContent(self, fileName=None, mode="r", encoding="cp1252"):
        if not Path(self.pathName + "/" + self.fileName).exists():
            return None

        fileNameToExtract = fileName is None and self.pathName + "/" + self.fileName or fileName
        return open(file=fileNameToExtract, mode=mode, encoding=encoding).read()

    def getFileContentInLines(self, fileName=None, mode="r", encoding="cp1252"):
        if not Path(self.pathName + "/" + self.fileName).exists():
            return None

        fileNameToExtract = fileName is None and self.pathName + "/" + self.fileName or fileName
        return open(file=fileNameToExtract, mode=mode, encoding=encoding).readlines()

    def getFileContentBytes(self, fileName=None):
        if not Path(self.pathName + "/" + self.fileName).exists():
            return None

        fileNameToExtract = fileName is None and self.pathName + "/" + self.fileName or fileName
        return Path(fileNameToExtract).read_bytes()

    def saveFileContent(self, content, fileName=None, mode="w+"):

        if content is None:
            return None

        fileNameToCreate = fileName is None and self.pathName + "/" + self.fileName or fileName

        writer = open(file=fileNameToCreate, mode=mode)
        writer.write(content)
        writer.close()

        return fileNameToCreate


