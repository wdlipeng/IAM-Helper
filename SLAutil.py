'''
Created on Nov 21, 2017

@author: ezhonho
'''
import yamlutil
import httplib
from string import Template


def provisionSP(spId):
    (ip,port)=yamlutil.get_provision_endpoint_info()
    headers = {"Content-Type": "application/xml"}
    bodyTemplate='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                     <Entity xmlns="http://schemas.ericsson.com/provisioning/generic" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                     <EntityType>ServiceProvider</EntityType>
                     <TypeSpace>DefaultSpace</TypeSpace>
                     <Category xsi:nil="true"/>
                     <Id name="ServiceProviderId" value="${SP}"/>
                     <Property name="Name" value="${SP}"/>
                     <Property name="Status" value="active"/>
                     </Entity>'''
    body=Template(bodyTemplate).substitute(SP=spId)
    conn=httplib.HTTPConnection(ip,port)
    conn.request("POST", "/Provisioning/generic/entity/v2",body, headers)
    response = conn.getresponse()
    status=response.status
    print "response status is:"+str(status)
    conn.close()
    if (status==200):
        print "onboard SP:"+spId+" sucess!"
    elif(status== 409):
        print "onboard SP:"+spId+" already exist,will not update!"
    else:
        print "onboard SP:"+spId+" failed!"
        

        
def provisionSPSS(spId,scId,typeSpace):
    (ip,port)=yamlutil.get_provision_endpoint_info()
    headers = {"Content-Type": "application/xml"}
    bodyTemplate='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                      <Entity xmlns="http://schemas.ericsson.com/provisioning/generic">
                      <EntityType>ServiceProviderServiceSubscription</EntityType>
                      <TypeSpace>${TP}</TypeSpace>
                      <Category>${SC_ID}</Category>
                      <Id name="SubscriptionId" value="${SP}_${SC_ID}"/>
                      <Ref name="ServiceCapabilityId" value="${SC_ID}"/>
                      <Ref name="ServiceProviderId" value="${SP}"/>
                      <Ref name="SubscriptionCode" value="${SP}_${SC_ID}_subCode"/>
                      </Entity>'''
    body=Template(bodyTemplate).substitute(SP=spId,SC_ID=scId,TP=typeSpace)
    conn=httplib.HTTPConnection(ip,port)
    conn.request("POST", "/Provisioning/generic/entity/v2",body, headers)
    response = conn.getresponse()
    status=response.status
    conn.close()
    if (status==200):
        print "onboard SPSS:"+spId+" sucess!"
    elif(status== 409):
        print "onboard SPSS:"+spId+" already exist,will not update!"
    else:
        print "onboard SPSS:"+spId+" failed!"
        
        
def provisionAPP(appId,password,spId,scId):
    (ip,port)=yamlutil.get_provision_endpoint_info()
    headers = {"Content-Type": "application/xml"}
    bodyTemplate='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <Entity xmlns="http://schemas.ericsson.com/provisioning/generic" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <EntityType>Application</EntityType>
                    <TypeSpace>DefaultSpace</TypeSpace>
                    <Category xsi:nil="true"/>
                    <Id name="ApplicationId" value="${APP}"/>
                    <Ref name="ServiceProviderId" value="${SP}"/>
                    <Property name="Name" value="${APP}"/>
                    <Property name="Password" value="${PASSWORD}"/>
                    <Property name="Status" value="active"/>
                    <Property name="Desc" value="${APP}"/>
                 </Entity>'''
    body=Template(bodyTemplate).substitute(APP=appId,PASSWORD=password,SP=spId,SC_ID=scId)
    #print "onboard APP,body is"+body
    conn=httplib.HTTPConnection(ip,port)
    conn.request("POST", "/Provisioning/generic/entity/v2",body, headers)
    response = conn.getresponse()
    status=response.status
    conn.close()
    if (status==200):
        print "onboard APP:"+appId+" sucess!"
    elif(status== 409):
        print "onboard APP:"+appId+" already exist,will not update!"
    else:
        print "onboard APP:"+appId+" failed!"
        
        
def provisionASS(appId,spId,scId,redirectUris,postRedirectUris,typeSpace,allowScopes):
    (ip,port)=yamlutil.get_provision_endpoint_info()  
    headers = {"Content-Type": "application/xml"}
    bodyTemplate='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <Entity xmlns="http://schemas.ericsson.com/provisioning/generic">
                    <EntityType>ApplicationServiceSubscription</EntityType>
                    <TypeSpace>${TP}</TypeSpace>
                    <Category>${SC_ID}</Category>
                    <Id name="SubscriptionId" value="${APP}_${SC_ID}"/>
                    <Ref name="PartnerSubscriptionId" value="${SP}_${SC_ID}"/>
                    <Ref name="ApplicationId" value="${APP}"/>
                    <Ref name="ServiceCapabilityId" value="${SC_ID}"/>
                    <Ref name="ServiceProviderId" value="${SP}"/>
                    <Property name="AllowOfflineAccess" value="true"/>
                    <Property name="AutoApprove" value="true"/>
                    <Property name="AllowedGrantTypes" value="authorization_code,client_credentials"/>
                    <Property name="RedirectUris" value="${REDIRECT_URI}"/>
                    <Property name="PostLogoutRedirectUris" value="${POST_REDIRECT_URI}"/>
                    <Property name="AllowedScopes" value="${AS}"/>
                    </Entity>'''
    body=Template(bodyTemplate).substitute(APP=appId,SP=spId,SC_ID=scId,REDIRECT_URI=redirectUris,POST_REDIRECT_URI=postRedirectUris,TP=typeSpace,AS=allowScopes)
    #print "onboard ASS,body is"+body
    conn=httplib.HTTPConnection(ip,port)
    conn.request("POST", "/Provisioning/generic/entity/v2",body, headers)
    response = conn.getresponse()
    status=response.status
    conn.close()
    if (status==200):
        print "onboard ASS:"+appId+" sucess!"
    elif(status== 409):
        print "onboard ASS:"+appId+" already exist,will not update!"
    else:
        print "onboard ASS:"+appId+" failed!"
    
    
def provisionSystemUserASS(appId,spId,scId,typeSpace,allowScopes):
    (ip,port)=yamlutil.get_provision_endpoint_info()
    headers = {"Content-Type": "application/xml"}
    bodyTemplate='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                    <Entity xmlns="http://schemas.ericsson.com/provisioning/generic">
                    <EntityType>ApplicationServiceSubscription</EntityType>
                    <TypeSpace>${TP}</TypeSpace>
                    <Category>${SC_ID}</Category>
                    <Id name="SubscriptionId" value="${APP}_${SC_ID}"/>
                    <Ref name="PartnerSubscriptionId" value="${SP}_${SC_ID}"/>
                    <Ref name="ApplicationId" value="${APP}"/>
                    <Ref name="ServiceCapabilityId" value="${SC_ID}"/>
                    <Ref name="ServiceProviderId" value="${SP}"/>
                    <Property name="TokenMode" value="self-contained"/>
                    <Property name="AllowedGrantTypes" value="client_credentials"/>
                    <Property name="AllowedScopes" value="${AS}"/>
                    </Entity>'''
    body=Template(bodyTemplate).substitute(APP=appId,SP=spId,SC_ID=scId,TP=typeSpace,AS=allowScopes)
    #print "onboard ASS,body is"+body
    conn=httplib.HTTPConnection(ip,port)
    conn.request("POST", "/Provisioning/generic/entity/v2",body, headers)
    response = conn.getresponse()
    status=response.status
    conn.close()
    if (status==200):
        print "onboard ASS:"+appId+" sucess!"
    elif(status== 409):
        print "onboard ASS:"+appId+" already exist,will not update!"
    else:
        print "onboard ASS:"+appId+" failed!"                      
   

if __name__ == '__main__':
    pass