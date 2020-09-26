#!/usr/bin/env python
# encoding: utf-8
'''
@author: duanqiyang
@project: ApiShopping
@file: T005_AccountAuth.py
@time: 2019-10-23 16:51:15
@desc: 新账号认证
'''

import requests

def auth(custNo):
    url = 'http://esbpre.cnsuning.com:9106/SuNingServiceWeb/mb'

    data="""<?xml version="1.0" encoding="utf-8"?>
            <MbfService xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><input1><MbfHeader>
            <ServiceCode>MemberInfoMgmt</ServiceCode>
            <Operation>updateEnterpriseMemberIndividualInfo</Operation>
            <AppCode>SOA</AppCode>
            <UId>174eb7f3e6f6456a9d00531f877fcb64ab7de6ac33bd43a6</UId>
            <AuthId>$[esb.http.AuthId]</AuthId>
            </MbfHeader>
            <MbfBody>
            <sysHeader>
            <transCode>TU01030010</transCode>
            <userName/>
            <password/>
            <tranDate/>
            <tranTimestamp/>
            <sourceSystemNo>139000000670</sourceSystemNo>
            <destSystemNo>139000000080</destSystemNo>
            <tranType>1000</tranType>
            <createdTime>2014-11-07 15:07:11.664</createdTime>
            <updatedTime>2014-11-07 15:07:11.664</updatedTime>
            <sourceByEmployee/>
            <sourceChannel/>
            </sysHeader>
            <appHeader>
            <getRecNum/>
            <beginRecNum/>
            </appHeader>
            <body>
            <ecoType>140000000010</ecoType>
            <custNum>%s</custNum>
            <organizationInfo>
            <registration/>
            <organizationBase>
            <certValidStat>233000000030</certValidStat>
            <certValidStatUpdRsn></certValidStatUpdRsn>
            <vatQlfctStat>234000000040</vatQlfctStat>
            <vatQlfctStatUpdRsn></vatQlfctStatUpdRsn>
            </organizationBase>
            </organizationInfo>
            </body>
            </MbfBody>
            </input1>
            </MbfService>"""%custNo


    req=requests.post(url=url,data=data)
    print(req.text)

if __name__ == '__main__':

    auth(custNo="7017976067")