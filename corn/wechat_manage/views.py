from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from wechat_manage.action import registerAction, projectAction, settingAction,\
    menuAction
from wechat_manage import constDef
from wechat_manage.dbop import roleOpe, userInfoOpe, projectInfoOpe, menuListOpe
from wechat_manage.models import menuType

# Create your views here.
def isLogin(request):
    if constDef.SESSION_USERINFO in request.session:
        request.session.set_expiry(600)
        return True
    
    return False

def login(request):
    if not isLogin(request):
        return render(request, 'wechat_manage/login.html', {})
    
    return HttpResponseRedirect('/dashboard')  
    
def register(request):
    return render(request, 'wechat_manage/register.html', {})

def createProject(request):
    if not isLogin(request):
        return render(request, 'wechat_manage/login.html', {})
    
    return render(request, 'wechat_manage/project.html', {})

def dashboard(request):
    if not isLogin(request):
        return render(request, 'wechat_manage/login.html', {})
    
    url = request.path
    ctx = {}
    
    try:
        if url == '/dashboard/menu/list':
            return showMenulistView(request)
        elif url == '/dashboard/menu/add':
            return showMenuAddView(request)
        elif url == '/dashboard/overview':
            return showOvervieView(request)
        elif url == '/dashboard/role/list':
            return showRoleListView(request)
        elif url == '/dashboard/role/add':
            ctx['page'] = 'role_add'
        elif url == '/dashboard/user/list':
            return showUserListView(request)
        elif url.startswith('/dashboard/user/add'):
            return showUserAddView(request)
        elif url == '/dashboard/article/list':
            ctx['page'] = 'article_list'
        elif url == '/dashboard/article/add':
            ctx['page'] = 'article_add'
        elif url == '/dashboard/welcome' or url == '/dashboard/':
            ctx['page'] = 'welcome'
    except Exception as e:
        ctx = {}
        ctx['rlt'] = "Exception happened during view render: %s" % e
        return render(request, 'wechat_manage/error.html', ctx)
                                 
    return render(request, 'wechat_manage/dashboard.html', ctx)

def normal_page(request):
    if not isLogin(request):
        return render(request, 'wechat_manage/login.html', {})
    
    url = request.path
    ctx = {}
    if url == '/user/profile/':
        ctx['page'] = 'user_profile'
      
    return render(request, 'wechat_manage/page_base.html', ctx)   

def doAction(request):
    url = request.path
    
    if request.POST:
        try:
            if url == '/action/register/':
                return registerAction.doRegister(request)    
            elif url == '/action/mailcheck':
                return registerAction.doMailCheck(request)
            elif url == '/action/namecheck':
                return registerAction.doNameCheck(request)
            elif url == '/action/login/':
                return registerAction.doLogin(request)             

        except Exception as e:
            ctx = {}
            ctx['rlt'] = "Exception happened during action: %s" % e
            return render(request, 'wechat_manage/error.html', ctx)

    if not isLogin(request):
        return render(request, 'wechat_manage/login.html', {})

    if request.POST:
        try:
            if url == '/action/createproject/':
                return projectAction.doCreateProject(request)
            elif url == '/action/createrole/':
                return settingAction.doCreateRole(request)
            elif url == '/action/deleterole/':
                return settingAction.doDeleteRole(request)
            elif url == '/action/useradd/':
                return settingAction.doAddUserToProject(request)
            elif url == '/action/deleteuserlist/':
                return settingAction.doDeleteUserFromProject(request)
            elif url == '/action/menuadd/':
                return menuAction.menuAddAction(request)
            elif url == '/action/menuapply/':
                return menuAction.menuApplyAction(request)
            elif url == '/action/menudelete/':
                return menuAction.menuDeleteAction(request)
        except Exception as e:
            ctx = {}
            ctx['rlt'] = "Exception happened during action: %s" % e
            return render(request, 'wechat_manage/error.html', ctx)
        
    else:        
        if url == '/action/logout/':
            del request.session[constDef.SESSION_USERINFO]
            return render(request, 'wechat_manage/login.html', {})

def showRoleListView(request):
    userDto = request.session[constDef.SESSION_USERINFO]
    curPid = userDto[constDef.CUR_PROJECTID]
    #proInfos = userDto[constDef.PROJECT_INFOS]
    #curPro = proInfos[curPid]
    rolelist = roleOpe.getRoleList(curPid)
    
    return render(request, 'wechat_manage/dashboard.html', {'page' : 'role_list', 'rolelist' : rolelist})

def showUserListView(request):
    userDto = request.session[constDef.SESSION_USERINFO]
    curPid = userDto[constDef.CUR_PROJECTID]
    
    userlist = userInfoOpe.getProjectUserList(curPid)
    
    return render(request, 'wechat_manage/dashboard.html', {'page' : 'user_list', 'userlist' : userlist})
    
def showUserAddView(request):
    userDto = request.session[constDef.SESSION_USERINFO]
    curPid = userDto[constDef.CUR_PROJECTID]
    
    mail = request.GET.get(constDef.MAIL_ADDRESS)
    
    rolelist = roleOpe.getRoleList(curPid)
    
    return render(request, 'wechat_manage/dashboard.html', {'page' : 'user_add', 
                                                            'rolelist' : rolelist,
                                                            'mailaddress' : mail}) 
    
def showOvervieView(request):
    ctx = {'page' : 'overview'}
    
    userDto = request.session[constDef.SESSION_USERINFO]
    projectinfo = projectInfoOpe.getProjectInfo(userDto[constDef.CUR_PROJECTID])
    
    ctx[constDef.PROJECT_INFOS] = projectinfo
    
    return render(request, 'wechat_manage/dashboard.html', ctx)

def showMenulistView(request):
    userDto = request.session[constDef.SESSION_USERINFO]
    appid = userDto[constDef.CUR_PROJECTID]
    
    retlist = menuAction.menuListAction(request, appid)
    editCount = menuListOpe.getEditedMenuCount(appid)
    return render(request, 'wechat_manage/dashboard.html', {'page' : 'menu_list',
                                                            'menulist' : retlist,
                                                            'editcount' : editCount})
    
def showMenuAddView(request):
    retlist = menuListOpe.getMenuTypeList()
    
    userDto = request.session[constDef.SESSION_USERINFO]
    appid = userDto[constDef.CUR_PROJECTID]
    menulist = menuListOpe.getMenuList(appid)
    
    return render(request, 'wechat_manage/dashboard.html', {'page' : 'menu_add', 
                                                            'menutype' : retlist,
                                                            'menulist' : menulist})   