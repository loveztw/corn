from wechat_manage.dbop import userInfoOpe
import json
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from wechat_manage.dto import userInfoDto
from wechat_manage import constDef
from corn.util import encryption

def doRegister(request):
    mail = request.POST['inputEmail']
    uname = request.POST['inputName']
    password = request.POST['inputPassword']
    
    userInfoOpe.saveUserInfo(uname, mail, encryption.encrypt(password))
    
    html = 'wechat_manage/login.html'
    return render(request, html, {})
    
    
def doMailCheck(request):
    mail = request.POST['inputEmail']
    ret = userInfoOpe.isMailExist(mail)
    return_json = {'result' : ret}
    return HttpResponse(json.dumps(return_json))

def doNameCheck(request):
    uname = request.POST['inputName']
    ret = userInfoOpe.isUserNameExist(uname)
    return_json = {'result' : ret}
    return HttpResponse(json.dumps(return_json))
    
def doLogin(request):
    ctx = {}
    mail = request.POST['inputEmail']
    password = request.POST['inputPassword']
    dbenpass = userInfoOpe.getUserPass(mail)
    if dbenpass == "":
        ctx['rlt'] = "User name is not exist."
        ctx['uname'] = mail
        return render(request, 'wechat_manage/login.html', ctx)
    
    dbpass = encryption.decrypt(dbenpass)
    if password != dbpass:
        ctx['rlt'] = "Password mismatch."
        ctx['uname'] = mail
        return render(request, 'wechat_manage/login.html', ctx)
        
    ret = userInfoOpe.getUserInfo(mail)
    userDto = userInfoDto.userInfoDto(ret[constDef.USER_NAME], mail)
    
    projectList = userInfoOpe.getUserProInfo(mail)
    for proj in projectList:
        userDto.createProject(proj[0], proj[1], proj[2], proj[3])
    
    proCount = len(projectList)
    if proCount != 0:
        userDto.setCurPorjectId(projectList[0][0])
        
    request.session[constDef.SESSION_USERINFO] = userDto.toDict()
    return HttpResponseRedirect('/dashboard')