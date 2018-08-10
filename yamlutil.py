'''
Created on Jul 28, 2017

@author: ezhonho
'''
import yaml
import logging


def load_config(config_file='./config.yaml'):
    config = {} 
    try:
        config = yaml.load(file(config_file, 'r'))
    except yaml.YAMLError, exc:
        print "Error in configuration file:", exc
    return config

def get_ece_base_path():
    config = load_config()
    eceBasePath = config['ECEBasePath']
    return eceBasePath

def get_jwt_info():
    config = load_config()
    JWT = config['JWT']
    keyStoreType = JWT['oauth.jwt.keyStoreType']
    keyStoreFilePath = JWT['oauth.jwt.keyStoreFilePath']
    storePass = JWT['oauth.jwt.storePass']
    keyalias = JWT['oauth.jwt.keyalias']
    keyPass = JWT['oauth.jwt.keyPass']
    keyalg = JWT['keyalg']
    keysize = JWT['keysize']
    validity = JWT['validity']
    dname = JWT['dname']
    return (keyStoreType, keyStoreFilePath, storePass, keyalias, keyPass, keyalg, keysize, validity, dname)

def get_cpa_info():
    config = load_config()
    CPA = config['CPA']
    cpaUrl = CPA['rm.iam.cpa.url']
    clientid = CPA['iam.rm.adapter.cpa.clientid']
    password = CPA['iam.rm.adapter.cpa.password']
    trustStoreType = CPA['iam.rm.adapter.cpa.truststore.type']
    trustStoreFile = CPA['iam.rm.adapter.cpa.truststore.file']
    trustStorePass = CPA['iam.rm.adapter.cpa.truststore.pass']
    return (cpaUrl, clientid, password, trustStoreType, trustStoreFile, trustStorePass)

def get_cpm_info():
    config = load_config()
    CPM = config['CPM']
    keyAlias = CPM['iam.rm.adapter.cpm.key.alias']
    keyPass = CPM['iam.rm.adapter.cpm.key.pass']
    keyStoreType = CPM['iam.rm.adapter.cpm.keystore.type']
    keyStoreFile = CPM['iam.rm.adapter.cpm.keystore.file']
    keystorePass = CPM['iam.rm.adapter.cpm.keystore.pass']
    trustStoreType = CPM['iam.rm.adapter.cpm.truststore.type']
    trustStoreFile = CPM['iam.rm.adapter.cpm.truststore.file']
    trustStorePass = CPM['iam.rm.adapter.cpm.truststore.pass']
    return (keyAlias, keyPass, keystorePass, keyStoreType, keyStoreFile, trustStoreType, trustStoreFile, trustStorePass)

def get_ums_info():
    config = load_config()
    UMS = config['UMS']
    keyAlias = UMS['iam.rm.adapter.ums.key.alias']
    keyPass = UMS['iam.rm.adapter.ums.key.pass']
    keystorePass = UMS['iam.rm.adapter.ums.keystore.pass']
    keyStoreType = UMS['iam.rm.adapter.ums.keystore.type']
    keyStoreFile = UMS['iam.rm.adapter.ums.keystore.file']
    trustStoreType = UMS['iam.rm.adapter.ums.truststore.type']
    trustStoreFile = UMS['iam.rm.adapter.ums.truststore.file']
    trustStorePass = UMS['iam.rm.adapter.ums.truststore.pass']
    return (keyAlias, keyPass, keystorePass, keyStoreType, keyStoreFile, trustStoreType, trustStoreFile, trustStorePass)

def get_idRepoConnector_info():
    config = load_config()
    IRC = config['idRepoConnector']
    trustStoreFile = IRC['iam.rm.adapter.idRepoConnector.truststore.file']
    trustStoreType = IRC['iam.rm.adapter.idRepoConnector.truststore.type']
    trustStorePass = IRC['iam.rm.adapter.idRepoConnector.truststore.pass']
    return (trustStoreFile, trustStoreType, trustStorePass)

def get_oidcConfig_info():
    config = load_config()
    OIDC = config['OIDCProviderConfiguration']
    oauthPubilcUrl = OIDC['oauth.server.public.url']
    sessionEnabled = OIDC['iam.session.management.enabled']
    return (oauthPubilcUrl, sessionEnabled)

def get_captchaConfiguration_info():
    config = load_config()
    CaptchaConfiguration = config['CaptchaConfiguration']
    siteKey = CaptchaConfiguration['iam.captcha.sitekey']
    secretKey = CaptchaConfiguration['iam.captcha.secretkey']
    siteVerifyApiUrl = CaptchaConfiguration['iam.captcha.siteverify.api.url']
    showCaptchaThreshold = CaptchaConfiguration['iam.authn.showcaptcha.threshold']
    return (siteKey, secretKey, siteVerifyApiUrl, showCaptchaThreshold)


def get_acr_amr_info():
    config = load_config()
    AMRAndACR = config['AMRAndACR']
    amr = AMRAndACR['iam.supported.amr']
    amrAcrMapping = AMRAndACR['iam.acr.amr.mapping']
    acr = AMRAndACR['iam.default.acr']
    return (amr, amrAcrMapping, acr)

def get_other_info():
    config = load_config()
    Other = config['Other'] 
    emailAged = Other['iam.email.min.age.second']
    supportLanguage = Other['iam.supported.language']
    sqMinNum = Other['iam.securityquestion.userset.min.number']  
    anonymousRole = Other['iam.rm.anonymous.defaultRoleName']
    return (emailAged, supportLanguage, sqMinNum, anonymousRole)    

def get_provision_endpoint_info():
    config = load_config()
    CLUSTERINFO = config['CLUSTERINFO'] 
    provisionEndpoint = CLUSTERINFO['provision_endpoint']
    (ip, port) = provisionEndpoint.split(':')
    return (ip, port)
    
def get_systemuser_app_list():
    config = load_config()
    appList = config['SYSTEMUSERApplication'] 
    return appList

def get_fe_app_list():
    config = load_config()
    appList = config['FEApplication'] 
    return appList

def get_systemuser_customize_header():
    config = load_config()
    IAMAsSystemUser = config['IAMAsSystemUser'] 
    application = IAMAsSystemUser['iam.rm.systemuser.headerName.application']
    role = IAMAsSystemUser['iam.rm.systemuser.headerName.role']
    customizeHeader = IAMAsSystemUser['iam.rm.adapter.oauth.customize.header']
    return (application, role, customizeHeader)  

if __name__ == '__main__':
    config = load_config()
    
    print "get_cpm_info"
    print "(keyAlias, keyPass, keystorePass, keyStoreType, keyStoreFile, trustStoreType, trustStoreFile, trustStorePass)"
    print get_cpm_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_ums_info"
    print "(keyAlias, keyPass, keystorePass, keyStoreType, keyStoreFile, trustStoreType, trustStoreFile, trustStorePass)"
    print get_ums_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_cpa_info"
    print "(cpaUrl, clientid, password, trustStoreType, trustStoreFile, trustStorePass)"
    print get_cpa_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_idRepoConnector_info"
    print "(trustStoreFile, trustStoreType, trustStorePass)"
    print get_idRepoConnector_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_acr_amr_info"
    print "(amr, amrAcrMapping, acr)"
    print get_acr_amr_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_systemuser_customize_header"
    print "(application, role, customizeHeader)"
    print get_systemuser_customize_header()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_systemuser_app_list"
    print "(appList)"
    print get_systemuser_app_list()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_jwt_info"
    print "(keyStoreType, keyStoreFilePath, storePass, keyalias, keyPass, keyalg, keysize, validity, dname)"
    print get_jwt_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_oidcConfig_info"
    print "(oauthPubilcUrl, sessionEnabled)"
    print get_oidcConfig_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_captchaConfiguration_info"
    print "(siteKey, secretKey, siteVerifyApiUrl, showCaptchaThreshold)"
    print get_captchaConfiguration_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    
    print "get_other_info"
    print "(emailAged, supportLanguage, sqMinNum, anonymousRole) "
    print get_other_info()
    print "-------------------------------------------------------------------------------------------------------------"
    
    print "get_provision_endpoint_info"
    print "(ip, port)"
    print get_provision_endpoint_info()    

