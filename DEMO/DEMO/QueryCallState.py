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

    # 呼叫状态查询
    # @param callSid   必选参数    一个由32个字符组成的电话唯一标识符
    # @param action      可选参数     查询结果通知的回调url地址 

def QueryCallState(callid,action):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.QueryCallState(callid,action)
    for k,v in result.iteritems(): 
            print '%s:%s' % (k, v)
   
   
#QueryCallState('callSid','查询结果通知的回调url地址')