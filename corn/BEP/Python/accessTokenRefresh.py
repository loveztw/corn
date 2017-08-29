#!usr/bin/python
import sqlite3
import os
import urllib.request
import json, time
from time import sleep

DB_PATH = '../../db.sqlite3'

STOP_FILE = '../Config/accessTokenRefresh.stop'

def getAccessToken(appid, secret):
    
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid, secret)
    
    response = urllib.request.urlopen(url)
    res_byte = response.read()
    res_txt = res_byte.decode('utf-8')
    res_dict = json.loads(res_txt)
    
    if 'errcode' in res_dict:
        errcode = res_dict['errcode']
        errmsg = res_dict['errmsg']
        err = "errcode = %d, errmsg = %s" % (errcode, errmsg)
        print('Failed in get accesstoken. appid = %s' % appid)
        raise Exception(err)
    
    print(res_dict)
    return res_dict

print('accessTokenRefresh start.')

while True:
    if os.path.exists(STOP_FILE):
        print('accessTokenRefresh stop.')
        break
        
    try:
        conn = sqlite3.connect(DB_PATH)
        
        c = conn.cursor()

        sets = c.execute("SELECT appid, secret, expire, strftime ('%s', tokenupdatedate) from wechat_manage_projectinfo where deleteflag = '0'")
        for row in sets:
            appid = row[0]
            secret = row[1]
            expire = row[2]
            updatedate = row[3]
            
            if updatedate != None:
                curfTime = time.time()
                diffTime = curfTime - int(updatedate)
            
            resDict = {}
            if updatedate == None or diffTime > int(expire) - 100:
                try:
                    resDict = getAccessToken(appid, secret)
                except Exception as e:
                    print('Accesstoken get failed. err = %s' % e)
                    continue
                
                c.execute("update wechat_manage_projectinfo set accesstoken = '%s', \
                expire = '%s', tokenupdatedate = datetime()" % (resDict['access_token'], resDict['expires_in']))
                conn.commit()
                
    except Exception as e:
        print('Access token refresh failed. err = %s' % e)
        break
    
    sleep(60)
