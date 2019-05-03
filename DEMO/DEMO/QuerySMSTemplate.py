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

# 短信模板查询
# @param templateId  必选参数   模板Id，不带此参数查询全部可用模板 
def QuerySMSTemplate(templateId):
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.QuerySMSTemplate(templateId)
    i=1
    for k,v in result.iteritems(): 
        
        if k=='TemplateSMS' :
            for m in v:
                print ('第'+str(i)+'个模板')
                i=i+1
                for k,v in m.iteritems(): 
                    print '%s:%s' % (k, v)
        else:
            print '%s:%s' % (k, v)
   
   
#QuerySMSTemplate('')