from wechat_manage import constDef, views
from wechat_manage.dbop import roleOpe, projectInfoOpe, userInfoOpe
from django.shortcuts import render
from django.db import transaction

def doCreateRole(request):
    checkList = request.POST.getlist("check_box_list")
    roleName = request.POST['inputRoleName']
    ability = 0
    
    for item in checkList:
        if item == constDef.ABILITY_CB_ARTICLE:
            ability = ability | constDef.ABILITY_ARTICLE
        elif item == constDef.ABILITY_CB_MENU:
            ability = ability | constDef.ABILITY_MENU
        elif item == constDef.ABILITY_CB_OVERVIEW:
            ability == ability | constDef.ABILITY_OVERVIEW
        elif item == constDef.ABILITY_CB_ROLE:
            ability == ability | constDef.ABILITY_ROLE
        elif item == constDef.ABILITY_CB_USER:
            ability == ability | constDef.ABILITY_USER
            
    userDto = request.session[constDef.SESSION_USERINFO]
    
    roleOpe.saveRole(roleName, ability, userDto[constDef.CUR_PROJECTID])
    return views.showRoleListView(request)

@transaction.atomic
def doDeleteRole(request):
    checkList = request.POST.getlist("checkItem")
    for data in checkList:
        datalist = data.split(",")
        roleid = datalist[0]
        updatedate = datalist[1]
        
        ret = roleOpe.isRoleUsed(roleid)
        if ret:
            rolename = roleOpe.getRoleName(roleid)
            ctx = {}
            ctx['rlt'] = "Role is Used. Can not be deleted. Rolename = %s" % rolename[constDef.ROLENAME]
            return render(request, 'wechat_manage/error.html', ctx)            
                
        roleOpe.deleteRole(roleid, updatedate)
        
    return views.showRoleListView(request)

def doAddUserToProject(request):
    mail = request.POST['inputUserName']
    
    #mail check
    ret = userInfoOpe.isMailExist(mail)
    if ret == True:
        ctx = {}
        ctx['rlt'] = "User mail address is not found, please check. %s" % mail
        return render(request, 'wechat_manage/error.html', ctx)
    
    roleid = request.POST['inputUserRole']
    userDto = request.session[constDef.SESSION_USERINFO]
    projectInfoOpe.saveUserList(mail, userDto[constDef.CUR_PROJECTID], roleid)
    
    return views.showUserListView(request)

def doDeleteUserFromProject(request):
    checkList = request.POST.getlist("checkItem")
    for data in checkList:
        datalist = data.split(",")
        listid = datalist[0]
        updatedate = datalist[1]
        userInfoOpe.deleteUserList(listid, updatedate)
        
    return views.showUserListView(request)