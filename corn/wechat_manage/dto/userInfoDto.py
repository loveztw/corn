from wechat_manage import constDef
from wechat_manage.constDef import ABILITY

class projectInfoDto:
    def __init__(self, projectId, projectName, roleid, ability):
        self.__projectId = projectId
        self.__projectName = projectName
        self.__roleid = roleid
        self.__ability = ability
        
    def toDict(self):
        retDict = {}
        retDict[constDef.PROJECT_ID] = self.__projectId
        retDict[constDef.PROJECT_NAME] = self.__projectName
        retDict[constDef.ROLE_ID] = self.__roleid
        retDict[constDef.ABILITY] = self.__ability
        return retDict

class userInfoDto:
    
    def __init__(self, uname, mail, projectDict = {}, curPid = ''):
        self.__userName = uname
        self.__email = mail
        self.__projectInfoDict = projectDict
        self.__curProjectId = curPid
        
    def getUserName(self):
        return self.__userName
        
    def getEmail(self):
        return self.__email
    
    def setCurPorjectId(self, id):
        self.__curProjectId = id
    
    def getCurProjectId(self):
        return self.__curProjectId
    
    def toDict(self):
        retDict = {}
        retDict[constDef.USER_NAME] = self.__userName
        retDict[constDef.MAIL_ADDRESS] = self.__email
        retDict[constDef.CUR_PROJECTID] = self.__curProjectId
        retDict[constDef.PROJECT_INFOS] = self.__projectInfoDict
        return retDict
    
    def createProject(self, projectId, projectName, roleid, ability):
        if projectId in self.__projectInfoDict:
            return False
        
        projInfoDto = projectInfoDto(projectId, projectName, roleid, ability)
        self.__projectInfoDict[projectId] = projInfoDto.toDict()
        return True

    def getProjectDict(self):
        return self.__projectInfoDict