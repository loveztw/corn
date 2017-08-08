from django.db import models

# Create your models here.


class userInfo(models.Model):
    username = models.CharField(max_length=32)
    mailaddress = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    createdate = models.DateTimeField()
    updatedate = models.DateTimeField()
    deleteflag = models.CharField(max_length=1)
        
    def __unicode__(self):
        return self.username
    
class projectInfo(models.Model):
    projectname = models.CharField(max_length=32)
    appid = models.CharField(max_length=64, primary_key=True)
    secret = models.CharField(max_length=64)
    createdate = models.DateTimeField()
    updatedate = models.DateTimeField()
    deleteflag = models.CharField(max_length=1)
    
    def __unicode__(self):
        return self.projectname
    
class role(models.Model):
    rolename = models.CharField(max_length=32)
    ability = models.IntegerField(null=True)
    createdate = models.DateTimeField()
    updatedate = models.DateTimeField()
    deleteflag = models.CharField(max_length=1)
    
    project = models.ForeignKey(projectInfo, null=True)

    def __unicode__(self):
        return self.rolename        
    
class userList(models.Model):
    user = models.ForeignKey(userInfo)
    project = models.ForeignKey(projectInfo)
    roleinfo = models.ForeignKey(role, null=True)
    createdate = models.DateTimeField()
    updatedate = models.DateTimeField()
    deleteflag = models.CharField(max_length=1)   
    
    