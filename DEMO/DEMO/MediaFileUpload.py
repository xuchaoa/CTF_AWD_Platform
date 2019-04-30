#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '您的主帐号';

#主帐号Token
accountToken= '您的主帐号Token';

#应用Id
appId='您的应用ID';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

    # @param filename   必选参数    文件名
    # @param path      可选参数     文件所在路径

def MediaFileUpload(filename,path):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    file_object = open(path,'rb')
    try:
        body = file_object.read()
    finally:
        file_object.close()
	
    result = rest.MediaFileUpload(filename,body)
    for k,v in result.iteritems(): 
            print '%s:%s' % (k, v)
   
   
#MediaFileUpload('文件名','文件所在路径')