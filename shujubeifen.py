#-*- coding: UTF-8 -*- 
#!/usr/bin/python 
#==================================================== 

#==================================================== 
import datetime 
import subprocess 
import os 
import sys 
import logging 
logging.basicConfig(level=logging.DEBUG, 
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                datefmt='%a, %d %b %Y %H:%M:%S', 
                filename='backup.log', 
                filemode='a') 
backuser = 'root'
backpass = '123456'
basedir = '/backups'
todaydate = datetime.datetime.now().strftime("%y%m%d") 
fullback_dir = "%s/%s" %(basedir,todaydate) 
cuhour = datetime.datetime.now().strftime("%H")  
increment_dir = '%s/%s' %(basedir,cuhour) 
increbase_dir='' 
stores = '/stores'
  
#转储老的备份数据，移动到以当前年月日命名的文件夹内，目录如150209-bak 
def storebefore(): 
    suffix = datetime.datetime.now().strftime("%y%m%d") 
    storedir = "%s/%s-bak" %(stores,suffix) 
    if not os.path.exists(storedir): 
        subprocess.call("mkdir -p %s" %(storedir),shell=True) 
    command = "cd %s && mv * %s" %(basedir,storedir) 
    subprocess.call(command,shell=True) 
      
# 删除转储目录中超过7天的备份数据 
#def cleanstore(): 
#    command = "find %s -type d -mtime +7 |xargs rm -fr" % stores 
#    subprocess.call(command,shell=True) 
  
# 备份方法，每天23点完整备份，第二天0-22点增量备份 
def backup(): 
    if not os.path.exists(basedir): 
        subprocess.call("mkdir -p %s"%basedir,shell=True) 
    commandfull = "innobackupex --host=127.0.0.1 --user=%s --password=%s --no-timestamp %s" %(backuser,backpass,fullback_dir) #利用innobackupex进行全备份
    if cuhour == '16': 
        storebefore() 
        subprocess.call("rm -fr %s/*"%basedir,shell=True) 
        subprocess.call(commandfull,shell=True) 
        logging.info(commandfull) 
    else: 
        if int(cuhour) - 16 = 1:  
             increbase_dir = "%s/%s" %(basedir,todaydate) 
        else: 
             increbase_dir = '%s/%s' %(basedir,str(int(cuhour) - 1)) 
        commandincre = "innobackupex --host=127.0.0.1 --user=%s --password=%s --no-timestamp --incremental --incremental-basedir=%s %s" %( 
                        backuser,backpass,increbase_dir,increment_dir) 
        subprocess.call(commandincre,shell=True) 
        logging.info(commandincre) 
          
if __name__ == '__main__': 
    backup() 
#    cleanstore()
