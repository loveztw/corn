from django import template
from wechat_manage import constDef

register = template.Library()

@register.filter(name='hasPrivilege')
def hasPrivilege(value, menuType):
    
    ability = 0
    if menuType == "overview": 
        ability = constDef.ABILITY_OVERVIEW
    elif menuType == "role":
        ability = constDef.ABILITY_ROLE
    elif menuType == "user":
        ability = constDef.ABILITY_USER
    elif menuType == "menu":
        ability = constDef.ABILITY_MENU
    elif menuType == "article":
        ability = constDef.ABILITY_ARTICLE
    
    proId = value[constDef.CUR_PROJECTID]
    proInfos = value[constDef.PROJECT_INFOS]
    
    if proId == "" or len(proInfos) == 0:
        return False
    
    proinfo = proInfos[proId]
    
    return ability & proinfo[constDef.ABILITY]
    
@register.filter(name='getProjectList')
def getProjectList(value):
    proList = []
    
    if len(value) == 0:
        return proList
    
    for k,v in value.items():
        for k1,v1 in v.items():
            if k1 == constDef.PROJECT_NAME:
                proList.append({'appid': k, constDef.PROJECT_NAME : v1})
                
    return proList

            