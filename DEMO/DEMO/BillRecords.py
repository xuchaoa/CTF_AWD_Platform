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

  # 话单下载
  # @param date     day 代表前一天的数据（从00:00 – 23:59）
  # @param keywords   客户的查询条件，由客户自行定义并提供给云通讯平台。默认不填忽略此参数

def billRecords(date,keywords):
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.billRecords(date,keywords)
    for k,v in result.iteritems(): 
        print '%s:%s' % (k, v)
   
   
#billRecords('查询方式','查询条件')