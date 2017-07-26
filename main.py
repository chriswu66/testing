# -*- coding: utf-8 -*-
import os
import urllib,urllib2,cookielib
import json,re,ConfigParser
import sys
import time

reload(sys)
sys.setdefaultencoding( "utf-8" )

j_username = None
j_password = None
jk_username = None
jk_password = None
loginUrl = None
opener= None
projectId = None
projectUrl = None
BaseUrl = None
cycleId = None
jenkins_logUrl=None
jenkins_loginUrl=None
# print BaseUrl


# 读取配置文件初始化变量
def init():
    global j_username
    global j_password
    global jk_username
    global jk_password
    global loginUrl
    global opener
    global projectId
    global projectUrl
    global BaseUrl
    global cycleId
    global jenkins_logUrl
    global jenkins_loginUrl
    try:
        config = ConfigParser.ConfigParser()
        config.readfp(open('main.ini', "rb"))
        # 赋值
        j_username = configUtil(config.get("global","j_username"))
        j_password = configUtil(config.get("global","j_password"))
        jk_username = configUtil(config.get("global", "jk_username"))
        jk_password = configUtil(config.get("global", "jk_password"))
        loginUrl = configUtil(config.get("global","loginUrl"))
        opener = configUtil(config.get("global","opener"))
        projectId = configUtil(config.get("global","projectId"))
        projectUrl = configUtil(config.get("global","projectUrl"))
        BaseUrl = configUtil(config.get("global","BaseUrl"))
        cycleId = configUtil(config.get("global","cycleId"))
        jenkins_loginUrl = configUtil(config.get("global","jenkins_loginUrl"))
        jenkins_logUrl = configUtil(config.get("global","jenkins_logUrl"))

        return True;
    except Exception,e:
        print e
        print u"初始化失败"
        return False;
# 配置读取处理
def configUtil(str):
    if(str=='None'):
        return None
    else:
        return str
# 通过url获取数据
def getDataByUrl(url,dataArgu,methodType=None):
    print 'getDataByUrl'
    global opener
    try:
        if(opener==None):
            print 'none'
            cj = cookielib.CookieJar()
            # cookieJar作为参数，获得一个opener的实例
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            # 伪装成一个正常的浏览器，避免有些web服务器拒绝访问。此处伪装的火狐
            opener.addheaders = [('User-agent',
                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]
            # 构造请求数据
            data_post = urllib.urlencode({
                'os_username':j_username,
                'os_password':j_password,
                'os_destination':'',
                'user_role':'',
                'atl_token':'',
                'login':'登录'
            })  # every data should be contained
            # 以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
            # op = opener.open(url,data_post,timeout=1000)
            op = opener.open(loginUrl, data_post)

        # 以带cookie的方式访问页面
        if (methodType != None):
            if(methodType=='PUT'):
                # print methodType
                header = {
                    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
                    'Content-Type': 'application/json'}
                request = urllib2.Request(url, dataArgu,header)
                # print dataArgu
                request.get_method = lambda:"PUT"
                # op = urllib2.urlopen(request)
                op = opener.open(request)
                print 'this'
                data = op.read()
                return data
        else:
            op = opener.open(url)
            data = op.read()
            return data
        # if(methodType!=None):

        # print op.read()
        # 读取页面源码
        data = op.read()
        return data
    except Exception,e:
        print e
        print 'getData Failure'
        return '{}'

def doCycle(cycle,cycleData):
    print 'doCycle'
    getExecUrl = BaseUrl + '/execution?cycleId='+str(cycle)+'&projectId='+str(projectId)+'&versionId='+str(cycleData['versionId'])
    # print getExecUrl
    execRes = json.loads(getDataByUrl(getExecUrl, []))
    # print execRes
    doExecution(execRes)

def doExecution(execRes):
    print 'doExecution'
    statuss  = execRes['status']
    executions = execRes['executions']
    # print executions
    for execution in executions:
        # print execution
        print execution['summary']
        result = execTestcase(execution['summary'])
        print result
        resCode = None
        execstatus = None
        if(result!='Failure'):
            resCode =  len(result.failures)+len(result.errors)
            print resCode
            if(resCode>0):
                execstatus = '2'
            else:
                execstatus = '1'
        else:
            resCode =  '1'
            execstatus = '4'

        changeExecutionUrl = BaseUrl+'/execution/'+str(execution['id'])+'/execute'
        print changeExecutionUrl
        data = '{"status": '+execstatus+'}'
        print data
        result = json.loads(getDataByUrl(changeExecutionUrl, data,'PUT'))
        # print result


# http://10.52.12.44:8080/rest/zapi/latest/execution/4/execute
def execTestcase(s):
    # print 'execTestcase'
    try:
        # stringmodule = __import__('TestCase.'+s)  # 动态加载模块
        stringmodule = __import__(s)  # 动态加载模块
        # print stringmodule
        # print '\n'.join(['%s:%s' % item for item in stringmodule.__dict__.items()])
        return stringmodule.main()
        # return main(stringmodule)

    except Exception, e:
        print e
        # print 'Failure'
        return 'Failure'
    # try:
    # os.system('dir')
    # os.chdir('TestCase')
    # cmd = 'python '+s+'.py >log.txt'
    # # outp =  os.popen(cmd)
    # os.system(cmd)
    # # print '\n'.join(['%s:%s' % item for item in outp.__dict__.items()])
    # os.chdir('..')

            # output = os.popen('python TestCase/'+s+'.py')
        # output  = os.popen('dir')
        # print output
        # print output.read()
    # except Exception,e:
    #     print e
    #     print '666'

if __name__ == '__main__':
    # global projectId
    print 'main'
    if(not init()):
        exit()
    try:
        if(cycleId!=''):
            cycleArr = re.split(',', cycleId)# 分割出id数组
            for item in cycleArr:
                getCycleDataUrl = BaseUrl+'/cycle/'+item
                # print getCycleDataUrl
                cyclesres = json.loads(getDataByUrl(getCycleDataUrl,[]))
                doCycle(item,cyclesres)

        else:
            projectRes = json.loads(getDataByUrl(projectUrl,[]))
            for project in projectRes:
                projectId = project['id']
                cycleurl = BaseUrl + '/cycle?projectId='+project['id']
                cyclesres = json.loads(getDataByUrl(cycleurl,[]))

                for project in cyclesres:
                    # print project #projectId
                    # print cyclesres[project]#projectData
                    projectData = cyclesres[project]
                    for cycles in projectData:
                        # print cycles #all cycle data
                        for cycle in cycles:
                            if (cycle != 'recordsCount' and int(cycle) >= 0):
                                print cycle
                                cycleData = cycles[cycle]
                                doCycle(cycle,cycleData)

        #TODO

    except Exception,e:
        print e
        print 'error'

    #catch log
    try:
        print ("getXmlFile start")
        cj = cookielib.CookieJar()
        # cookieJar作为参数，获得一个opener的实例
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        # 伪装成一个正常的浏览器，避免有些web服务器拒绝访问。此处伪装的火狐
        opener.addheaders = [('User-agent',
                              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]
        # 构造请求数据
        data_post = urllib.urlencode({
            'j_username': jk_username,
            'j_password': jk_password,
            'from': '',
            'json': '{"j_username": ' + jk_username + ', "j_password": ' + jk_password + ', "remember_me": false, "from": "", "Jenkins-Crumb": "8e439d95ff2208df6993fc4d3f900031"}',
            'Jenkins-Crumb': '8e439d95ff2208df6993fc4d3f900031',
            'Submit': '登录'
        })  # every data should be contained
        # 以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
        # op = opener.open(url,data_post,timeout=1000)
        op = opener.open(jenkins_loginUrl, data_post)
        # 以带cookie的方式访问页面
        op = opener.open(jenkins_logUrl)
        # print "mid"
        # 读取页面源码
        datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        data = op.read()
        f = open('log/JenkinsLog_' + datetime + '.log', 'w')
        f.write(data)
        f.close()
    except Exception, e:
        print e
        print "catch log failed"
        # doCycle(cyclesres)
        # cycleurl = BaseUrl + '/cycle?projectId=10000';
        # url = BaseUrl + '/execution?cycleId=1&projectId=10000&versionId=10000'
        # cyclesres = json.loads(getDataByUrl(cycleurl,[]))
