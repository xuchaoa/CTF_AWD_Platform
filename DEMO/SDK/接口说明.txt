接口说明

     # 初始化
     # @param serverIP       必选参数    服务器地址
     # @param serverPort     必选参数    服务器端口
     # @param softVersion    必选参数    REST版本号
    def __init__(self,ServerIP,ServerPort,SoftVersion)
  
  
    # 设置主帐号
    # @param AccountSid  必选参数    主帐号
    # @param AccountToken  必选参数    主帐号Token
    def setAccount(self,AccountSid,AccountToken):
	
	
    # 设置子帐号
    # 
    # @param SubAccountSid  必选参数    子帐号
    # @param SubAccountToken  必选参数    子帐号Token
    def setSubAccount(self,SubAccountSid,SubAccountToken):
	

    # 设置应用ID
    # 
    # @param AppId  必选参数    应用ID
    def setAppId(self,AppId):
	
	
  
    # 创建子账号
    # @param friendlyName   必选参数      子帐号名称
    def CreateSubAccount(self, friendlyName):
  
  
    #  获取子帐号
    # @param startNo  可选参数    开始的序号，默认从0开始
    # @param offset 可选参数     一次查询的最大条数，最小是1条，最大是100条
    def getSubAccounts(self, startNo,offset):
   
   
    # 子帐号信息查询
    # @param friendlyName 必选参数   子帐号名称
    def querySubAccount(self, friendlyName):
  
  
    # 发送模板短信
    # @param to  必选参数     短信接收彿手机号码集合,用英文逗号分开
    # @param datas 可选参数    内容数据
    # @param tempId 必选参数    模板Id       
    def sendTemplateSMS(self, to,datas,tempId):
  
  
    # 双向回呼
    # @param fromPhone  必选参数   主叫电话号码
    # @param to 必选参数    被叫电话号码
    # @param customerSerNum 可选参数    被叫侧显示的客服号码  
    # @param fromSerNum 可选参数    主叫侧显示的号码
    # @param promptTone 可选参数    第三方自定义回拨提示音  
    # @param alwaysPlay 可选参数 是否一直播放提示音
    # @param terminalDtmf 可选参数 用于终止播放提示音的按键
    # @param userData 可选参数    第三方私有数据  
    # @param maxCallTime 可选参数    最大通话时长
    # @param hangupCdrUrl 可选参数    实时话单通知地址	
    # @param needBothCdr 可选参数 是否给主被叫发送话单
    # @param needRecord 可选参数 是否录音
    # @param countDownTime 可选参数 设置倒计时时间
    # @param countDownPrompt 可选参数 到达倒计时时间播放的提示音    
    def callBack(self,fromPhone,to,customerSerNum,fromSerNum,promptTone,alwaysPlay,terminalDtmf,userData,maxCallTime,hangupCdrUrl,needBothCdr,needRecord,countDownTime,countDownPrompt): 
  

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
    def landingCall(self,to,mediaName,mediaTxt,displayNum,playTimes,respUrl,userData,maxCallTime,speed,volume,pitch,bgsound): 
   

    # 语音验证码
    # @param verifyCode  必选参数   验证码内容，为数字和英文字母，不区分大小写，长度4-8位
    # @param playTimes  可选参数   播放次数，1－3次
    # @param to 必选参数    接收号码
    # @param displayNum 可选参数    显示的主叫号码
    # @param respUrl 可选参数    语音验证码状态通知回调地址，云通讯平台将向该Url地址发送呼叫结果通知
    # @param lang 可选参数    语言类型
    # @param userData 可选参数    第三方私有数据
    def voiceVerify(self,verifyCode,playTimes,to,displayNum,respUrl,lang,userData):
  

    # IVR外呼
    # @param number  必选参数     待呼叫号码，为Dial节点的属性
    # @param userdata 可选参数    用户数据，在<startservice>通知中返回，只允许填写数字字符，为Dial节点的属性
    # @param record   可选参数    是否录音，可填项为true和false，默认值为false不录音，为Dial节点的属性
    def ivrDial(self,number,userdata,record):
  
  
    # 话单下载
    # @param date   必选参数    day 代表前一天的数据（从00:00 – 23:59）
    # @param keywords  可选参数     客户的查询条件，由客户自行定义并提供给云通讯平台。默认不填忽略此参数
    def billRecords(self,date,keywords):


    # 主帐号信息查询
    def queryAccountInfo(self):

    # 短信模板查询
    # @param templateId  必选参数   模板Id，不带此参数查询全部可用模板
    def QuerySMSTemplate(self,templateId):

    # 取消回拨
    # @param callSid   必选参数    一个由32个字符组成的电话唯一标识符
    # @param type      可选参数    0： 任意时间都可以挂断电话；1 ：被叫应答前可以挂断电话，其他时段返回错误代码；2： 主叫应答前可以挂断电话，其他时段返回错误代码；默认值为0。
    def CallCancel(self,callSid,type):

    # 呼叫结果查询
    # @param callSid   必选参数    呼叫ID
    def CallResult(self,callSid):

    # 呼叫状态查询
    # @param callSid   必选参数    一个由32个字符组成的电话唯一标识符
    # @param action      可选参数     查询结果通知的回调url地址 
    def QueryCallState (self,callid,action):

    # 语音文件上传
    # @param filename   必选参数    文件名
    # @param budy      可选参数     二进制数据
    def MediaFileUpload (self,filename,body):

    #子帐号鉴权
    def subAuth(self):


    #主帐号鉴权
    def accAuth(self):


    #设置包头
    def setHttpHeader(self,req):
  

 
 


 
 
  
  

  
  

  
  


  
   

  
    

 
   