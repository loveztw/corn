from wechat_manage.models import role, userList
from wechat_manage import constDef
import datetime
from corn.util import dateUtils

def getSuperRoleid(appid):
    return role.objects.filter(ability=constDef.ROLE_SUPER, project_id=appid).values('id').first()

def saveRole(roleName, ability, appid):
    #curDate = datetime.datetime.now()
    curDate = dateUtils.getSqliteSystime()
    roleinfo = role(rolename=roleName, ability=ability, project_id=appid,
                    createdate=curDate, updatedate=curDate, deleteflag="0")
    roleinfo.save()

def getRoleName(roleid):
    return role.objects.filter(id=roleid, deleteflag='0').values(constDef.ROLENAME).first()

def isRoleUsed(roleid):
    ret = userList.objects.filter(roleinfo_id=roleid, deleteflag='0')
    count = len(ret)
    if count != 0:
        return True
    
    return False

def deleteRole(roleid, updatedate):
    roleInfo = role.objects.get(id=roleid, updatedate=updatedate)
    roleInfo.deleteflag = '1'
    roleInfo.updatedate = dateUtils.getSqliteSystime()
    roleInfo.save()

def getRoleList(appid):
    retlist = []
    rets = role.objects.raw("select id, rolename, ability,"
                            " updatedate"
                            " from wechat_manage_role where project_id = '%s' and deleteflag = '0'" % appid)
    i = 0
    for item in rets:
        i = i + 1
        retDict = { 'no' : i,
                    constDef.ROLE_ID : item.id,
                    constDef.ROLENAME : item.rolename, 
                    constDef.ABILITY : abilityToString(item.ability),
                    constDef.DB_UPDATEDATE : item.updatedate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
        retlist.append(retDict)
    
    return retlist

def abilityToString(ability):
    retString = ''
    if ability & constDef.ABILITY_ARTICLE:
        retString = '%s; %s' % (constDef.ABILITY_CB_ARTICLE, retString)
    if  ability & constDef.ABILITY_MENU:
        retString = '%s; %s' % (constDef.ABILITY_CB_MENU, retString)
    if  ability & constDef.ABILITY_OVERVIEW:
        retString = '%s; %s' % (constDef.ABILITY_CB_OVERVIEW, retString)
    if  ability & constDef.ABILITY_ROLE:
        retString = '%s; %s' % (constDef.ABILITY_CB_ROLE, retString)        
    if  ability & constDef.ABILITY_USER:
        retString = '%s; %s' % (constDef.ABILITY_CB_USER, retString)  
        
    return retString