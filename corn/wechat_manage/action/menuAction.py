'''
Created on Aug 11, 2017

@author: zhout
'''
from wechat_manage.dbop import projectInfoOpe, menuListOpe
from wechat_manage import constDef, views
import urllib.request, json
from corn.util import common
from wechat_manage.dto import menuDto
from django.db import transaction
from wechat_manage.models import projectInfo

def menuListAction(request, appid):
    
    retList = menuListOpe.getMenuList(appid)
    count = len(retList)
    if count == 0:
        ''' No Data in db, get from wechat server. '''
        result = projectInfoOpe.getAccessToken(appid)
        accessToken = result[constDef.ACCESS_TOKEN]
            
        url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        req = urllib.request.Request(url, None)
        f = urllib.request.urlopen(req)
        res_dict = common.httpResponseToDict(f)
        print(res_dict)
        
        if 'errcode' in res_dict:
            errCode = res_dict['errcode']
            if errCode != 0:
                if errCode == 46003:
                    return []
                
                errmsg = res_dict['errmsg']
                err = "Failed in get menu list from wechat server. errcode = %d, errmsg = %s" % (errCode, errmsg)
                raise Exception(err)
            
            
        menuData = menuDto.menuDto()
        menuData.dictLoad(res_dict)
        retList = menuData.getMenuList()
        menuListOpe.saveMenuList(retList, appid)
        retList = menuListOpe.getMenuList(appid)
#    return res_dict
    return retList

def makeMenu(menuInfo, appid):
    
    mid = -1
    if 'id' in menuInfo:
        mid = menuInfo['id']
        
    menulist = menuListOpe.getMenuByParent(mid, appid)
        
    subButtonArr = []
    for item in menulist:
        subButton = {}

        if item[menuDto.menuDto.KEY_MENUNAME] != '':
            subButton['name'] = item[menuDto.menuDto.KEY_MENUNAME]

        ret = makeMenu(item, appid)
        if len(ret) != 0:
            subButton['sub_button'] = ret
        else:    
            if item[menuDto.menuDto.KEY_TYPE] != '':
                subButton['type'] = item[menuDto.menuDto.KEY_TYPE]
            
            if item[menuDto.menuDto.KEY_URL] != '':
                subButton['url'] = item[menuDto.menuDto.KEY_URL]
                
            if item[menuDto.menuDto.KEY_KEY] != '':
                subButton['key'] = item[menuDto.menuDto.KEY_KEY]
            
        subButtonArr.append(subButton)
            
    return subButtonArr

'''@transaction.atomic'''
def menuAddAction(request):
    name = request.POST['inputMenuName'].strip()
    mtype = request.POST['inputMenuType']
    key = request.POST['inputMenuKey'].strip()
    parent = request.POST['inputMenuParent']
    url = request.POST['inputMenuUrl'].strip()
  
    userDto = request.session[constDef.SESSION_USERINFO]
    appid = userDto[constDef.CUR_PROJECTID]
    
    addMenuDict = {
                menuDto.menuDto.KEY_MENUNAME : name,
                menuDto.menuDto.KEY_KEY : key,
                menuDto.menuDto.KEY_TYPEID : mtype,
                menuDto.menuDto.KEY_URL : url,
                menuDto.menuDto.KEY_PARENTID : parent
            }
    
    menuListOpe.saveMenuList([addMenuDict], appid)

    return views.showMenulistView(request)
    
def menuApplyAction(request):
    userDto = request.session[constDef.SESSION_USERINFO]
    appid = userDto[constDef.CUR_PROJECTID]
    
    if 'apply' in request.POST:
        buttonDict = {}
        buttonDict['button'] = makeMenu({}, appid)
        buttonJson = json.dumps(buttonDict)
        print(buttonJson)
        
        result = projectInfoOpe.getAccessToken(appid)
        accessToken = result[constDef.ACCESS_TOKEN]
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken

        req = urllib.request.Request(url, bytes(buttonJson, encoding = "utf8"))
        f = urllib.request.urlopen(req)
        res_dict = common.httpResponseToDict(f)
        
        if 'errcode' in res_dict:
            errcode = res_dict['errcode']
            if errcode != 0:
                errmsg = res_dict['errmsg']
                err = "Failed in create menu in wechat server. errcode = %d, errmsg = %s" % (res_dict['errcode'], errmsg)
                raise Exception(err)
        
        menuListOpe.menuUpdateSuccess(appid)
    else:
        menuListOpe.deleteUneditMenu(appid)
        
    return views.showMenulistView(request)
    
def menuDeleteAction(request):
    userDto = request.session[constDef.SESSION_USERINFO]
    appid = userDto[constDef.CUR_PROJECTID]
    
    checkList = request.POST.getlist("checkItem")
    for mid in checkList:
        menuListOpe.deleteMenuByID(appid, mid)
        
    return views.showMenulistView(request)