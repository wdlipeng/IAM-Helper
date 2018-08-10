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

def set_cm_value(DPname,component,item,value):
    cmd="iam-dp-cli set-key -d "+DPname+" -c "+component+" -V all -k "+item+" -v '"+value+"' -y"
    cmdutil.run_cmd(cmd)

def set_shared_cm_value(component,item,value):
    cmd="iam-dp-cli set-key -c "+component+" -V all -k "+item+" -v '"+value+"' -y"
    cmdutil.run_cmd(cmd)

def generate_jwks_into_db():
    (keyStoreType,keyStoreFilePath,storePass,keyalias,keyPass,keyalg,keysize,validity,dname)=yamlutil.get_jwt_info()
    now=int(time.time())
    validTo=int(validity)*3600*24+now
    sql="INSERT INTO sigdb.JWK_INFO (KID,ALIAS,KEYPASS,STATUS,CURRENT_USE,VALID_FROM,VALID_TO) VALUES ('kid_"+keyalias+"','"+keyalias+"','"+keyPass+"','ACTIVE','Y','"+str(now)+"','"+str(validTo)+"');"
    cmd='mysqlclient -e "'+sql+'"'
    cmdutil.run_cmd(cmd)

def prepare_jwks_configuration():

    (keyStoreType,keyStoreFilePath,storePass,keyalias,keyPass,keyalg,keysize,validity,dname)=yamlutil.get_jwt_info()
    if os.path.exists(keyStoreFilePath):
        print keyStoreFilePath +" already exist,will not update jwks related configuration again!"
        return
    cmd='keytool -genkey -keystore '+keyStoreFilePath+' -storetype '+keyStoreType+' -storepass '+storePass+' -keypass '+keyPass+' -keyalg '+keyalg+' -alias '+keyalias+' -keysize '+keysize+'  -dname "CN=IAM, OU=IAM, O=Ericsson, C=CN" -noprompt'
    cmdutil.run_cmd(cmd)
    generate_jwks_into_db()
    set_shared_cm_value("foundation-shared","oauth.jwt.keyStoreType",keyStoreType)
    set_shared_cm_value("foundation-shared","oauth.jwt.keyStoreFilePath",' file:'+keyStoreFilePath)
    set_shared_cm_value("foundation-shared","oauth.jwt.storePass",storePass)
    set_shared_cm_value("foundation-shared","oauth.jwt.keyalias",keyalias)
    set_shared_cm_value("foundation-shared","oauth.jwt.keyPass",keyPass)


def prepare_cpa_configuration():
    (cpaUrl,clientid,password,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_cpa_info()
    set_cm_value("DP-NotificationServer-Traffic","notification-server","rm.iam.cpa.url",cpaUrl)
    set_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.clientid",clientid)
    set_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.password",password)
    set_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.truststore.type",trustStoreType)
    set_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.truststore.file",trustStoreFile)
    set_cm_value("DP-NotificationServer-Traffic","notification-server","iam.rm.adapter.cpa.truststore.pass",trustStorePass)

def prepare_cpa_configuration_2():
    (cpaUrl,clientid,password,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_cpa_info()

    cmd="cm-cli set -k SEP/ece/17.1/DP-NotificationServer-Traffic/notification-server/3.0.0/rm.iam.cpa.url -v '" + cpaUrl + "' -y"
    cmdutil.run_cmd(cmd)

    cmd="cm-cli set -k SEP/ece/17.1/DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.clientid -v '" + clientid + "' -y"
    cmdutil.run_cmd(cmd)

    cmd="cm-cli set -k SEP/ece/17.1/DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.password -v '" + password + "' -y"
    cmdutil.run_cmd(cmd)

    cmd="cm-cli set -k SEP/ece/17.1/DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.truststore.type -v '" + trustStoreType + "' -y"
    cmdutil.run_cmd(cmd)

    cmd="cm-cli set -k SEP/ece/17.1/DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.truststore.file -v '" + trustStoreFile + "' -y"
    cmdutil.run_cmd(cmd)

    cmd="cm-cli set -k SEP/ece/17.1/DP-NotificationServer-Traffic/notification-server/3.0.0/iam.rm.adapter.cpa.truststore.pass -v '" + trustStorePass + "' -y"
    cmdutil.run_cmd(cmd)

def prepare_cpm_configuration():
    (keyAlias,keyPass,keystorePass,keyStoreType,keyStoreFile,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_cpm_info()
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.key.alias",keyAlias)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.key.pass",keyPass)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.keystore.pass",keystorePass)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.keystore.type",keyStoreType)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.keystore.file",keyStoreFile)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.truststore.type",trustStoreType)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.truststore.file",trustStoreFile)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.cpm.truststore.pass",trustStorePass)

def prepare_ums_configuration():
    (keyAlias,keyPass,keystorePass,keyStoreType,keyStoreFile,trustStoreType,trustStoreFile,trustStorePass)=yamlutil.get_ums_info()
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.key.alias",keyAlias)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.key.pass",keyPass)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.keystore.pass",keystorePass)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.keystore.type",keyStoreType)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.keystore.file",keyStoreFile)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.truststore.type",trustStoreType)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.truststore.file",trustStoreFile)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.ums.truststore.pass",trustStorePass)

def prepare_idRepoConnector_configuration():
    (trustStoreFile,trustStoreType,trustStorePass)=yamlutil.get_idRepoConnector_info()
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.idRepoConnector.truststore.file",trustStoreFile)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.idRepoConnector.truststore.type",trustStoreType)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.idRepoConnector.truststore.pass",trustStorePass)

def prepare_oidcConfig_configuration():
    (oauthPubilcUrl,sessionEnabled)=yamlutil.get_oidcConfig_info()
    set_cm_value("DP-OAuth-Traffic","oauth-server","oauth.server.public.url",oauthPubilcUrl)
    set_shared_cm_value("foundation-shared","iam.session.management.enabled",sessionEnabled)
    set_cm_value("DP-IdentityManagement-Traffic","identity-mgmt-server","iam.session.management.enabled",sessionEnabled)

def prepare_captchaConfiguration_configuration():
    (siteKey,secretKey,siteVerifyApiUrl,showCaptchaThreshold)=yamlutil.get_captchaConfiguration_info()
    set_shared_cm_value("foundation-shared","iam.captcha.sitekey",siteKey)
    set_shared_cm_value("foundation-shared","iam.captcha.secretkey",secretKey)
    set_shared_cm_value("foundation-shared","iam.captcha.siteverify.api.url",siteVerifyApiUrl)
    set_cm_value("DP-Authentication-Traffic","authentication-server","iam.authn.showcaptcha.threshold",showCaptchaThreshold)


def prepare_acr_amr_related_configuration():
    (amr,amrAcrMapping,acr)=yamlutil.get_acr_amr_info()
    set_shared_cm_value("foundation-shared","iam.supported.amr",amr)
    set_cm_value("DP-OAuth-Traffic","oauth-server","iam.acr.amr.mapping",amrAcrMapping)
    set_cm_value("DP-OAuth-Traffic","oauth-server","iam.default.acr",acr)
    set_cm_value("DP-Authentication-Traffic","authentication-server","iam.acr.amr.mapping",amrAcrMapping)
    set_cm_value("DP-Authentication-Traffic","authentication-server","iam.default.acr",acr)

def prepare_other_configuration():
    (emailAged,supportLanguage,sqMinNum,anonymousRole)=yamlutil.get_other_info()
    set_cm_value("DP-IdentityManagement-Traffic","identity-mgmt-server","iam.email.min.age.second",emailAged)
    set_cm_value("DP-IdentityManagement-Traffic","identity-mgmt-server","iam.supported.language",supportLanguage)
    set_shared_cm_value("foundation-shared","iam.securityquestion.userset.min.number",sqMinNum)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.anonymous.defaultRoleName",anonymousRole)

def prepare_systemuser_customize_header_configuration():
    (application,role,customizeHeader)=yamlutil.get_systemuser_customize_header()
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.systemuser.headerName.application",application)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.systemuser.headerName.role",role)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.customize.header",customizeHeader)
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.clientid",'IAM')
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.clientpass",'password')
    set_cm_value("DP-RMAdapter-Traffic","rm-adapter","iam.rm.adapter.oauth.scope",'system_user')

def prepare_IAMportal_configuration():
    set_cm_value("DP-IAM-Portal-Traffic","iam-portal","iam.portal.clientid",'IAMPortal')
    set_cm_value("DP-IAM-Portal-Traffic","iam-portal","iam.portal.scope",'portal')
    set_cm_value("DP-IAM-Portal-Traffic","iam-portal","iam.portal.secret ",'password')

def prepare_customizedClientIdExtractor_configuration():
    set_shared_cm_value("foundation-shared","facility.authentication.customizedClientIdExtractor.cba",'rm-cba')
    set_shared_cm_value("foundation-shared","facility.authentication.customizedClientIdPattern.cba",'(?<osuser>[^#]+)@(?<address>[^.]*)\.(?<application>.+)')

def prepare_sp():
    SLAutil.provisionSP('RM_SP')

def prepare_spss():
    SLAutil.provisionSPSS('RM_SP','OAUTH','OAuth')

def prepare_fe_apps():
    applist=yamlutil.get_fe_app_list()
    for app in applist:
        appName=app['appName']
        password=app['password']
        RedirectUris=app['RedirectUris']
        PostLogoutRedirectUris=app['PostLogoutRedirectUris']
        SLAutil.provisionAPP(appName, password, 'RM_SP','OAUTH')
        SLAutil.provisionASS(appName, 'RM_SP','OAUTH', RedirectUris, PostLogoutRedirectUris,'OAuth',"{&quot;openid&quot;: []}")

def prepare_systemuser_apps():
    applist=yamlutil.get_systemuser_app_list()
    for app in applist:
        appName=app['appName']
        SLAutil.provisionAPP(appName, 'password', 'RM_SP','OAUTH')
        SLAutil.provisionSystemUserASS(appName,'RM_SP','OAUTH','OAuth',"{&quot;openid&quot;:[],&quot;system_user&quot;:[]}")

def prepare_IAM_APP():
    SLAutil.provisionAPP('IAM', 'password', 'RM_SP','OAUTH')
    SLAutil.provisionSystemUserASS('IAM','RM_SP','OAUTH','OAuth',"{&quot;openid&quot;:[],&quot;system_user&quot;:[]}")

def prepare_IAM_Portal():
    SLAutil.provisionAPP('IAMPortal', 'password', 'RM_SP','OAUTH')
    SLAutil.provisionASS('IAMPortal', 'RM_SP','OAUTH', 'https://www.example.com/','https://www.example.com/','OAuth',"{&quot;openid&quot;:[],&quot;portal&quot;:[]}") 

if __name__ == '__main__':
    #prepare_cpa_configuration()
    prepare_cpa_configuration_2()
    # prepare_cpm_configuration()
    # prepare_ums_configuration()
    # prepare_jwks_configuration()
    # prepare_oidcConfig_configuration()
    # prepare_captchaConfiguration_configuration()
    # prepare_acr_amr_related_configuration()
    # prepare_customizedClientIdExtractor_configuration()
    # prepare_other_configuration()
    # prepare_sp()
    # prepare_spss()
    # prepare_IAM_APP()
    # prepare_systemuser_customize_header_configuration()
    # prepare_IAM_Portal()
    # prepare_IAMportal_configuration()
    # prepare_fe_apps()
    # prepare_systemuser_apps()
    # prepare_idRepoConnector_configuration()
