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

    # 外呼通知
    # @param to 必选参数    被叫号码
    # @param mediaName 可选参数    语音文件名称，格式 wav。与mediaTxt不能同时为空。当不为空时mediaTxt属性失效。
    # @param mediaTxt 可选参数    文本内容
    # @param displayNum 可选参数    显示的主叫号码
    # @param playTimes 可选参数    循环播放次数，1－3次，默认播放1次。
    # @param respUrl 可选参数    外呼通知状态通知回调地址，云通讯平台将向该Url地址发送呼叫结果通知。
    # @param userData 可选参数    用户私有数据
    # @param maxCallTime 可选参数    最大通话时长
    # @param speed 可选参数    发音速度
    # @param volume 可选参数    音量
    # @param pitch 可选参数    音调
    # @param bgsound 可选参数    背景音编号

def landingCall(to,mediaName,mediaTxt,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound):

    
    #初始化REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.landingCall(to,mediaName,mediaTxt,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound)
    for k,v in result.iteritems(): 
        
        if k=='LandingCall' :
                for k,s in v.iteritems(): 
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
   
   
#landingCall('被叫号码','语音文件名称','文本内容','显示的主叫号码','循环播放次数','外呼通知状态通知回调地址','用户私有数据','最大通话时长','发音速度','音量','音调','背景音编号')