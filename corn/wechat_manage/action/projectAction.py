from wechat_manage.dbop import projectInfoOpe, roleOpe, userInfoOpe
from wechat_manage import constDef
from django.db import transaction, IntegrityError
from django.http.response import HttpResponseRedirect
from wechat_manage.dto import userInfoDto

@transaction.atomic
def doCreateProject(request):
    projName = request.POST['inputName']
    appid = request.POST['inputAppid']
    secret = request.POST['inputSecret']

    ret = projectInfoOpe.saveProjetInfo(projName, appid, secret)
    if ret == False:
        err = "Project is already exist. appid = %s" % appid
        raise Exception(err)
    
    user = request.session[constDef.SESSION_USERINFO]
 
    roleOpe.saveRole('super', constDef.ROLE_SUPER, appid)
    ret = roleOpe.getSuperRoleid(appid)
    projectInfoOpe.saveUserList(user[constDef.MAIL_ADDRESS], appid, ret['id'])  
         
    userDto = userInfoDto.userInfoDto(user[constDef.USER_NAME], user[constDef.MAIL_ADDRESS])
    projlist = userInfoOpe.getUserProInfo(user[constDef.MAIL_ADDRESS])
    
    firstPro = ''
    for proj in projlist:
        if firstPro == '':
            firstPro = proj[0]
        userDto.createProject(proj[0], proj[1], proj[2], proj[3])

    if user[constDef.CUR_PROJECTID] != '':
        userDto.setCurPorjectId(user[constDef.CUR_PROJECTID])
    else:
        userDto.setCurPorjectId(firstPro)

    request.session[constDef.SESSION_USERINFO] = userDto.toDict()
    
    return HttpResponseRedirect('/dashboard')

        