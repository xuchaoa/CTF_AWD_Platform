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

  # IVR外呼
  # @param number   待呼叫号码，为Dial节点的属性
  # @param userdata 用户数据，在<startservice>通知中返回，只允许填写数字字符，为Dial节点的属性
  # @param record   是否录音，可填项为true和false，默认值为false不录音，为Dial节点的属性
def ivrDial(number,userdata,record):
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    #call createSubAccount
    result = rest.ivrDial(number,userdata,record)
    for k,v in result.iteritems(): 
        print '%s:%s' % (k, v)
   
   
#ivrDial('待呼叫号码','用户数据',是否录音)