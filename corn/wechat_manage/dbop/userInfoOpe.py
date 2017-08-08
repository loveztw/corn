from wechat_manage.models import userInfo, userList
from wechat_manage import constDef
import datetime
from corn.util import dateUtils

def saveUserInfo(uname, mail, password):
    #curDate = datetime.datetime.now()
    curDate = dateUtils.getSqliteSystime()
    uinfo = userInfo(username=uname, mailaddress=mail, password=password,
                      createdate=curDate, updatedate=curDate, deleteflag="0")
    uinfo.save()
    
def isUserNameExist(uname):
    ret = userInfo.objects.filter(username=uname)
    count = ret.count()
    if count > 0:
        return False
    
    return True
    
def isMailExist(mail):
    ret = userInfo.objects.filter(mailaddress=mail)
    count = ret.count()
    if count > 0:
        return False
    
    return True

def getUserPass(mail):
    ret = userInfo.objects.filter(mailaddress=mail).values_list(constDef.PASSWORD, flat=True)
    count = len(ret)
    if count == 0:
        return ""
    
    return ret.get()

def getUserInfo(mail):
    return userInfo.objects.filter(mailaddress=mail).values(constDef.USER_NAME).first()

def getUserProInfo(mail):
    userProList = []
    userlist = userList.objects.raw("select pinfo.appid, pinfo.projectname, role.id, role.ability from wechat_manage_userlist as ul"
                                    " join wechat_manage_projectinfo as pinfo on ul.project_id = pinfo.appid"
                                    " join wechat_manage_role as role on ul.roleinfo_id = role.id"
                                    " where ul.user_id = '%s' and ul.deleteflag = '0'" % mail)
    
    for user in userlist:
        projId = user.appid
        projName = user.projectname
        roleid = user.id
        ability = user.ability
        
        userProList.append((projId, projName, roleid, ability))
    
    return userProList
        
def getProjectUserList(appid):
    retList = []
    userlist = userList.objects.raw("select ul.id, ul.user_id, uinfo.username, role.rolename, ul.updatedate from wechat_manage_userlist as ul"
                                    " join wechat_manage_userinfo as uinfo on ul.user_id = uinfo.mailaddress"
                                    " join wechat_manage_role as role on ul.roleinfo_id = role.id"
                                    " where ul.project_id = '%s' and ul.deleteflag = '0'" % appid)
    i = 0
    for user in userlist:
        i = i + 1
        retList.append({'no' : i,
                        'id' : user.id,
                        constDef.MAIL_ADDRESS : user.user_id,
                        constDef.ROLENAME : user.rolename,
                        constDef.USER_NAME : user.username,
                        constDef.DB_UPDATEDATE : user.updatedate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]})
        
    return retList
        
def deleteUserList(listid, updatedate):
    userlist = userList.objects.get(id=listid, updatedate=updatedate)
    userlist.deleteflag = '1'
    userlist.updatedate = dateUtils.getSqliteSystime()
    userlist.save()
