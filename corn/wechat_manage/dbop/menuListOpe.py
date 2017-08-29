'''
Created on Aug 11, 2017

@author: zhout
'''
from wechat_manage.models import menuList, menuType
from wechat_manage import constDef
from wechat_manage.dto import menuDto
from django.db.models import Q 

def getMenuList(appid):
    sql = "select ml.id, ml.menuname, ml.parent, ml.key, ml.url, mt.type, ml.editflag, \
            (select menuname from wechat_manage_menulist where id = ml.parent) as parentname \
            from wechat_manage_menulist as ml \
            left join wechat_manage_menutype as mt on ml.menutype_id = mt.id \
            where ml.project_id = '%s'" % appid
    result = menuList.objects.raw(sql)
    
    i = 0
    retList = []
    for item in result:
        i = i + 1
        
        retList.append({
                'no' : i,
                'id' : item.id,
                menuDto.menuDto.KEY_MENUNAME : item.menuname,
                menuDto.menuDto.KEY_KEY : item.key,
                menuDto.menuDto.KEY_TYPE : item.type,
                menuDto.menuDto.KEY_URL : item.url,
                menuDto.menuDto.KEY_PARENT : item.parentname,
                menuDto.menuDto.KEY_EDITFLAG : item.editflag
            })
        
    return retList

def getMenuByParent(pid, appid):
    sql = "select ml.id, ml.menuname, ml.parent, ml.key, ml.url, mt.type, \
            (select menuname from wechat_manage_menulist where id = ml.parent) as parentname \
            from wechat_manage_menulist as ml \
            left join wechat_manage_menutype as mt on ml.menutype_id = mt.id \
            where ml.project_id = '%s' and ml.parent = %s and ml.editflag != 2" % (appid, pid)
    result = menuList.objects.raw(sql)
    
    retList = []
    for item in result:
        
        retList.append({
                'id' : item.id,
                menuDto.menuDto.KEY_MENUNAME : item.menuname,
                menuDto.menuDto.KEY_KEY : item.key,
                menuDto.menuDto.KEY_TYPE : item.type,
                menuDto.menuDto.KEY_URL : item.url,
                menuDto.menuDto.KEY_PARENT : item.parentname,
                menuDto.menuDto.KEY_PARENTID : item.parent
            })
        
    return retList 

def getMenuTypeId(type):
    idStr = menuType.objects.filter(type=type).values('id').first()
    return int(idStr['id'])

def getMenuTypeList():
    sql = "select id, type from wechat_manage_menutype"
    result = menuType.objects.raw(sql)
    
    retList = []
    for item in result:
        retList.append({'id' : item.id,
                        'type' : item.type})
        
    return retList

def getMenuid(name, appid):
    idStr = menuList.objects.filter(menuname=name, project_id=appid).values('id').first()
    return int(idStr['id'])

def saveMenuList(menulist, appid):
    for item in menulist:
        name = ''
        key = ''
        type = ''
        typeid = -1
        url = ''
        parentid = -1
        
        if menuDto.menuDto.KEY_MENUNAME in item:
            name = item[menuDto.menuDto.KEY_MENUNAME]
        
        if menuDto.menuDto.KEY_KEY  in item:
            key = item[menuDto.menuDto.KEY_KEY]
            
        if menuDto.menuDto.KEY_TYPE  in item:
            type = item[menuDto.menuDto.KEY_TYPE]
            typeid = getMenuTypeId(type)
        elif menuDto.menuDto.KEY_TYPEID in item:
            typeid = item[menuDto.menuDto.KEY_TYPEID]
            
        if menuDto.menuDto.KEY_URL  in item:
            url = item[menuDto.menuDto.KEY_URL]
        
        if menuDto.menuDto.KEY_PARENT  in item:
            parent = item[menuDto.menuDto.KEY_PARENT]        
            parentid = getMenuid(parent, appid)
        elif menuDto.menuDto.KEY_PARENTID in item:
            parentid = item[menuDto.menuDto.KEY_PARENTID]
        
        menuInfo = menuList(menuname=name,
                            parent=parentid, key=key,
                            url=url, menutype_id=typeid, project_id=appid,
                            editflag=1)
        menuInfo.save()

def deleteUneditMenu(appid):
    menuList.objects.filter(editflag=1,project_id=appid).delete()
    menuList.objects.filter(editflag=2,project_id=appid).update(editflag=0)
    
def getEditedMenuCount(appid):
    retlist = menuList.objects.filter(~Q(editflag=0), project_id=appid).values_list()
    return len(retlist)

def deleteMenuByID(appid, mid):
    menuList.objects.filter(id=mid, project_id=appid).update(editflag=2)
    
def menuUpdateSuccess(appid):
    menuList.objects.filter(editflag=1,project_id=appid).update(editflag=0)
    menuList.objects.filter(editflag=2,project_id=appid).delete()