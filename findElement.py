# -*- coding: utf-8 -*-
import re,os,sys
import ConfigParser
from selenium import webdriver

class FindElement():
    def __init__(self,driver):
        self.driver = driver
        f = open('Element1.csv', 'rb')
        self.linelist = f.readlines()
        f.close()

    def getElementByName(self,eleName):
        driver = self.driver
        linelist = self.linelist
        for i in range(len(linelist)):
            a = re.split('#', linelist[i])
            if eleName in a[0]:
                b = re.split(',', a[0])
                return self.transByType(b)
                # print 'line:', i + 1
                # print 'content:', linelist[i]

    def transByType(self,arr):
        driver = self.driver
        # print arr
        arr[2] = arr[2].decode(encoding='utf-8')
        try:
            if(arr[1]=='xpath'):
                return driver.find_element_by_xpath(arr[2])
            elif(arr[1]=='id'):
                return driver.find_element_by_id(arr[2])
            elif(arr[1]=='css'):
                return driver.find_element_by_css_selector(arr[2])
            elif(arr[1]=='name'):
                return driver.find_element_by_name(arr[2])
            elif(arr[1]=='linktext'):
                return driver.find_element_by_link_text(arr[2])
            elif(arr[1]=='plinktext'):
                return driver.find_element_by_partial_link_text(arr[2])
            elif(arr[1]=='tagname'):
                return driver.find_element_by_tag_name(arr[2])
            elif(arr[1]=='classname'):
                return driver.find_element_by_class_name(arr[2])
        except Exception,e:
            print e
            return None
class TCinit():
    def __init__(self,):
        config = ConfigParser.ConfigParser()
        config.readfp(open('TC.ini', "rb"))
        # 赋值
        self.browser = config.get("global", "browser")
        self.base_url = config.get("global", "base_url")
        sub_url=[]
        for i in range(1,10):
            try:
                sub_url[i] = config.get("global", "sub_url"+str(i))
            except:
                print "Exception in get Sub url"
                for j in (i,10):
                    sub_url[j] = ""
                break
        self.sub_url = sub_url
    def getDriver(self):
        if(self.browser == 'chrome'):
            return webdriver.Chrome()
        elif(self.browser == 'firefox'):
            return webdriver.Firefox()
        elif(self.browser == 'IE'):
            return webdriver.Ie()
    def getBase_url(self):
        return self.base_url
    def getSub_url(self):
        return self.sub_url

