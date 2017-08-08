
from wechat_manage.models import userList, projectInfo
from wechat_manage import constDef
import datetime
from corn.util import dateUtils

def getProjectInfoCount(appid):
    rets = projectInfo.objects.filter(appid=appid)
    return len(rets)

def saveProjetInfo(name, appid, secret):
    
    count = getProjectInfoCount(appid)
    if count != 0:
        return False
    
    #curDate = datetime.datetime.now()
    curDate = dateUtils.getSqliteSystime()
    pinfo = projectInfo(projectname=name, appid=appid, secret=secret,
                      createdate=curDate, updatedate=curDate, deleteflag="0")
    pinfo.save()
    return True
    
def saveUserList(mail, pid, roleid):
    #curDate = datetime.datetime.now()
    curDate = dateUtils.getSqliteSystime()
    userProList = userList(user_id=mail, project_id=pid, roleinfo_id=roleid,
                        createdate=curDate, updatedate=curDate, deleteflag="0")
                        
    userProList.save()
    
    