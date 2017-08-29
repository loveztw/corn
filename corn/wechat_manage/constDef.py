#session define
SESSION_USERINFO = 'userinfo'

#db common
DB_UPDATEDATE = 'updatedate'

#db field define for userinfo
USER_NAME = 'username'
MAIL_ADDRESS = 'mailaddress'
PASSWORD = 'password'
PROJECT_INFOS = 'projectinfos'
CUR_PROJECTID = 'curproid'

#db field define for roleinfo
ROLENAME = 'rolename'
#db field define for projectinfo
PROJECT_ID = 'appid'
PROJECT_NAME = 'projectname'
ROLE_ID = 'roleid'
ABILITY = 'ability'
PROJECT_SECRET = 'secret'
ACCESS_TOKEN = 'accesstoken'

#db field define for userlist
USERLIST_PROJECT_ID = 'project_id'

#db field define for menulist
MENU_NAME = 'menuname'
MENU_PARENTNAME = 'parentname'
MENU_KEY = 'key'
MENU_TYPE = 'type'
MENU_URL = 'url'

#role ability define
#admin
ROLE_SUPER = 0xFFFFFFFF
ABILITY_MENU = 0x01
ABILITY_ARTICLE = 0x01 << 1
ABILITY_OVERVIEW = 0x01 << 2
ABILITY_ROLE = 0x01 << 3
ABILITY_USER = 0x01 << 4

ABILITY_CB_OVERVIEW = 'overview'
ABILITY_CB_ROLE = 'role'
ABILITY_CB_USER = 'user'
ABILITY_CB_MENU = 'menu'
ABILITY_CB_ARTICLE = 'article'

