#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Archerx
# @time: 2019/4/19 上午 08:18

from utils.DEMO.SDK.CCPRestSDK import REST


class SendSMS(object):
    def __init__(self):
        self.ACCOUNT_SID = '8a216da86a2a8174016a39f0748d09ec'
        self.AUTH_TOKEN = 'dd49474506d14a07b5acffdf0468c44f'
        self.serverIP='app.cloopen.com';
        self.serverPort='8883';
        self.softVersion='2013-12-26'
        self.appId = '8a216da86a2a8174016a39f074e809f3'
    def Send_SMS(self,to,data,tempId):
        rest = REST(self.serverIP, self.serverPort, self.softVersion)
        rest.setAccount(self.ACCOUNT_SID, self.AUTH_TOKEN)
        rest.setAppId(self.appId)

        result = rest.sendTemplateSMS(to, data, tempId)
        print(result)  #返回dict结果
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print
        #             '%s:%s' % (k, s)
        #     else:
        #         print
        #         '%s:%s' % (k, v)


if __name__ == '__main__':
    a = SendSMS()
    a.Send_SMS('15615833854',['a','s'],1)