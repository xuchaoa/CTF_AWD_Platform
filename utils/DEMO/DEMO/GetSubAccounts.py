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

  # 获取子帐号
  # @param startNo 开始的序号，默认从0开始
  # @param offset 一次查询的最大条数，最小是1条，最大是100条

def getSubAccounts(startNo,offset):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    result = rest.getSubAccounts(startNo,offset)

    i=1
    for k,v in result.iteritems(): 
        
        if k=='SubAccount' :
            for m in v:
                print ('第'+str(i)+'个子帐号为')
                i=i+1
                for k,v in m.iteritems(): 
                    print '%s:%s' % (k, v)
        else:
            print '%s:%s' % (k, v)
   
#getSubAccounts('开始的序号','最大条数')