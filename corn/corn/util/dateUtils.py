import datetime

def getSqliteSystime():
    curfTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return datetime.datetime.strptime(curfTime, '%Y-%m-%d %H:%M:%S.%f')
    