# -*- coding: utf-8 -*-
import re,os,sys

class FindElementTemp():
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
