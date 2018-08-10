'''
Created on Nov 20, 2017

@author: ezhonho
'''

import yamlutil
import cmdutil
import SLAutil
import time
import os



ECE_BASE_PATH = os.environ.get("ECE_BASE_PATH")

def get_cm_value(DPname,component,item,value):
    cmd="iam-dp-cli get-key -d "+DPname+" -c "+component+" -V all -k "+item+"|awk -F '|' 'NR==4{print $6}'"
    value_c=cmdutil.run_cmd_r(cmd).replace("\n","").strip()
    if value_c != value:
        print "unmatched value: %s ,it should be set to %s \n" % (value_c, value)
    else:
        print "value matched\n"

# def get_cm_value(DPname,component,item,value):
#     cmd="iam-dp-cli get-key -d "+DPname+" -c "+component+" -V all -k "+item+"|awk -F '|' 'NR==4{print $6}'"
#     value_c=cmdutil.run_cmd_r(cmd,value)


# def get_shared_cm_value(component,item,value):
#     cmd="iam-dp-cli get-key -c "+component+" -V all -k "+item+"|awk -F '|' 'NR==4{print $6}'"
#     value_c=cmdutil.run_cmd_r(cmd).replace("\n","").strip()
#     if value_c != value:
#         print "unmatched value: %s ,it should be set to %s " % (value_c, value)
#     else:
#         print "value matched"

def get_shared_cm_value(component,item,value):
    cmd="iam-dp-cli get-key -c "+component+" -V all -k "+item+"|awk -F '|' 'NR==4{print $6}'"
    value_c=cmdutil.run_cmd_r(cmd).replace("\n","").strip()
    if value_c != value:
        print "unmatched value: %s ,it should be set to %s " % (value_c, value)
    else:
        print "value matched"

def get_value_by_cm_cli(key,value):
    cmd="cm-cli get -k "+ECE_BASE_PATH+"/"+key
    value_c=cmdutil.run_cmd_r(cmd).replace("\n","").strip()
    if value_c != value:
        print "unmatched value: %s ,it should be set to %s " % (value_c, value)
    else:
        print "value matched"


def generate_jwks_into_db():
    (keyStoreType,keyStoreFilePath,storePass,keyalias,keyPass,keyalg,keysize,validity,dname)=yamlutil.get_jwt_info()
    now=int(time.time())
    validTo=int(validity)*3600*24+now
    sql="INSERT INTO sigdb.JWK_INFO (KID,ALIAS,KEYPASS,STATUS,CURRENT_USE,VALID_FROM,VALID_TO) VALUES ('kid_"+keyalias+"','"+keyalias+"','"+keyPass+"','ACTIVE','Y','"+str(now)+"','"+str(validTo)+"');"
    cmd='mysqlclient -e "'+sql+'"'
    cmdutil.run_cmd_r(cmd)

def compare_jwks_configuration():

    (keyStoreType,keyStoreFilePath,storePass,keyalias,keyPass,keyalg,keysize,validity,dname)=yamlutil.get_jwt_info()
    if os.path.exists(keyStoreFilePath):
        print keyStoreFilePath +" already exist,will not update jwks related configuration again!"
        return
    cmd='keytool -genkey -keystore '+keyStoreFilePath+' -storetype '+keyStoreType+' -storepass '+storePass+' -keypass '+keyPass+' -keyalg '+keyalg+' -alias '+keyalias+' -keysize '+keysize+'  -dname "CN=IAM, OU=IAM, O=Ericsson, C=CN" -noprompt'
    cmdutil.run_cmd_r(cmd)
    generate_jwks_into_db()
    get_shared_cm_value("foundation-shared","oauth.jwt.keyStoreType",keyStoreType)
    get_shared_cm_value("foundation-shared","oauth.jwt.keyStoreFilePath",' file:'+keyStoreFilePath)
    get_shared_cm_value("foundation-shared","oauth.jwt.storePass",storePass)
    get_shared_cm_value("foundation-shared","oauth.jwt.keyalias",keyalias)
    get_shared_cm_value("foundation-shared","oauth.jwt.keyPass",keyPass)


def compare_cpa_configuration():
    (cpaUrl,clientid,password,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_cpa_info()
    get_cm_value("DP-NotificationServer-Traffic","notification-server","rm.iam.cpa.url",cpaUrl)
    get_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.clientid",clientid)
    get_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.password",password)
    get_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.truststore.type",trustStoreType)
    get_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.truststore.file",trustStoreFile)
    get_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.truststore.pass",trustStorePass)

def compare_cpa_configuration_2():
    (cpaUrl,clientid,password,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_cpa_info()
    get_value_by_cm_cli("DP-NotificationServer-Traffic/notification-server/3.0.0/rm.iam.cpa.url",cpaUrl)
    get_value_by_cm_cli("DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.clientid",clientid)
    get_value_by_cm_cli("DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.password",password)
    get_value_by_cm_cli("DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.truststore.type",trustStoreType)
    get_value_by_cm_cli("DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.truststore.file",trustStoreFile)
    get_value_by_cm_cli("DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.truststore.pass",trustStorePass)

def compare_cpm_configuration():
    (keyAlias,keyPass,keystorePass,keyStoreType,keyStoreFile,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_cpm_info()
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.key.alias",keyAlias)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.key.pass",keyPass)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.keystore.pass",keystorePass)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.keystore.type",keyStoreType)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.keystore.file",keyStoreFile)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.truststore.type",trustStoreType)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.truststore.file",trustStoreFile)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.truststore.pass",trustStorePass)

def compare_ums_configuration():
    (keyAlias,keyPass,keystorePass,keyStoreType,keyStoreFile,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_ums_info()
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.key.alias",keyAlias)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.key.pass",keyPass)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.keystore.pass",keystorePass)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.keystore.type",keyStoreType)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.keystore.file",keyStoreFile)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.truststore.type",trustStoreType)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.truststore.file",trustStoreFile)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.truststore.pass",trustStorePass)

def compare_idRepoConnector_configuration():
    (trustStoreFile,trustStoreType,trustStorePass)=yamlutil.get_idRepoConnector_info()
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.idRepoConnector.truststore.file",trustStoreFile)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.idRepoConnector.truststore.type",trustStoreType)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.idRepoConnector.truststore.pass",trustStorePass)

def compare_oidcConfig_configuration():
    (oauthPubilcUrl,sessionEnabled)=yamlutil.get_oidcConfig_info()
    get_cm_value("DP-OAuth-Traffic","oauth-server","oauth.server.public.url",oauthPubilcUrl)
    get_shared_cm_value("foundation-shared","iam.session.management.enabled",sessionEnabled)
    get_cm_value("DP-IdentityManagement-Traffic","identity-mgmt-server","iam.session.management.enabled",sessionEnabled)

def compare_captchaConfiguration_configuration():
    (siteKey,secretKey,siteVerifyApiUrl,showCaptchaThreshold)=yamlutil.get_captchaConfiguration_info()
    get_shared_cm_value("foundation-shared","iam.captcha.sitekey",siteKey)
    get_shared_cm_value("foundation-shared","iam.captcha.secretkey",secretKey)
    get_shared_cm_value("foundation-shared","iam.captcha.siteverify.api.url",siteVerifyApiUrl)
    get_cm_value("DP-Authentication-Traffic","authentication-server","iam.authn.showcaptcha.threshold",showCaptchaThreshold)


def compare_acr_amr_related_configuration():
    (amr,amrAcrMapping,acr)=yamlutil.get_acr_amr_info()
    get_shared_cm_value("foundation-shared","iam.supported.amr",amr)
    get_cm_value("DP-OAuth-Traffic","oauth-server","iam.acr.amr.mapping",amrAcrMapping)
    get_cm_value("DP-OAuth-Traffic","oauth-server","iam.default.acr",acr)
    get_cm_value("DP-Authentication-Traffic","authentication-server","iam.acr.amr.mapping",amrAcrMapping)
    get_cm_value("DP-Authentication-Traffic","authentication-server","iam.default.acr",acr)

def compare_other_configuration():
    (emailAged,supportLanguage,sqMinNum,anonymousRole)=yamlutil.get_other_info()
    get_cm_value("DP-IdentityManagement-Traffic","identity-mgmt-server","iam.email.min.age.second",emailAged)
    get_cm_value("DP-IdentityManagement-Traffic","identity-mgmt-server","iam.supported.language",supportLanguage)
    get_shared_cm_value("foundation-shared","iam.securityquestion.userset.min.number",sqMinNum)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.anonymous.defaultRoleName",anonymousRole)

def compare_systemuser_customize_header_configuration():
    (application,role,customizeHeader)=yamlutil.get_systemuser_customize_header()
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.systemuser.headerName.application",application)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.systemuser.headerName.role",role)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.customize.header",customizeHeader)
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.clientid",'IAM')
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.clientpass",'password')
    get_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.scope",'system_user')

def compare_IAMportal_configuration():
    get_cm_value("DP-IAM-Portal-Traffic","iam-portal","iam.portal.clientid",'IAMPortal')
    get_cm_value("DP-IAM-Portal-Traffic","iam-portal","iam.portal.scope",'portal')
    get_cm_value("DP-IAM-Portal-Traffic","iam-portal","iam.portal.secret ",'password')

def compare_customizedClientIdExtractor_configuration():
    get_shared_cm_value("foundation-shared","facility.authentication.customizedClientIdExtractor.cba",'rm-cba')
    get_shared_cm_value("foundation-shared","facility.authentication.customizedClientIdPattern.cba",'(?<osuser>[^#]+)@(?<address>[^.]*)\.(?<application>.+)')

def compare_sp():
    pass
    # SLAutil.provisionSP('RM_SP')

def compare_spss():
    pass
    # SLAutil.provisionSPSS('RM_SP','OAUTH','OAuth')

def compare_fe_apps():
    applist=yamlutil.get_fe_app_list()
    for app in applist:
        appName=app['appName']
        password=app['password']
        RedirectUris=app['RedirectUris']
        PostLogoutRedirectUris=app['PostLogoutRedirectUris']
        SLAutil.provisionAPP(appName, password, 'RM_SP','OAUTH')
        SLAutil.provisionASS(appName, 'RM_SP','OAUTH', RedirectUris, PostLogoutRedirectUris,'OAuth',"{&quot;openid&quot;: []}")

def compare_systemuser_apps():
    applist=yamlutil.get_systemuser_app_list()
    for app in applist:
        appName=app['appName']
        SLAutil.provisionAPP(appName, 'password', 'RM_SP','OAUTH')
        SLAutil.provisionSystemUserASS(appName,'RM_SP','OAUTH','OAuth',"{&quot;openid&quot;:[],&quot;system_user&quot;:[]}")

def compare_IAM_APP():
    SLAutil.provisionAPP('IAM', 'password', 'RM_SP','OAUTH')
    SLAutil.provisionSystemUserASS('IAM','RM_SP','OAUTH','OAuth',"{&quot;openid&quot;:[],&quot;system_user&quot;:[]}")

def compare_IAM_Portal():
    SLAutil.provisionAPP('IAMPortal', 'password', 'RM_SP','OAUTH')
    SLAutil.provisionASS('IAMPortal', 'RM_SP','OAUTH', 'https://www.example.com/','https://www.example.com/','OAuth',"{&quot;openid&quot;:[],&quot;portal&quot;:[]}") 

def check_cfg_main():
    compare_cpa_configuration()
    compare_cpa_configuration_2()
    compare_cpm_configuration()
    compare_ums_configuration()
    # compare_jwks_configuration()
    compare_oidcConfig_configuration()
    compare_captchaConfiguration_configuration()
    compare_acr_amr_related_configuration()
    compare_customizedClientIdExtractor_configuration()
    compare_other_configuration()
    # compare_sp()
    # compare_spss()
    # compare_IAM_APP()
    # compare_systemuser_customize_header_configuration()
    # compare_IAM_Portal()
    # compare_IAMportal_configuration()
    # compare_fe_apps()
    # compare_systemuser_apps()
    # compare_idRepoConnector_configuration()

if __name__ == '__main__':
    check_cfg_main()
