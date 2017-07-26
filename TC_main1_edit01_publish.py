# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time, re
import unittest, re
import os
import findElement
from findElement import *

class Workflow(unittest.TestCase):
    def setUp(self):
        config = TCinit()
        self.driver = config.getDriver()
        self.driver.maximize_window()
        self.base_url = config.getBase_url()
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Workflow(self):

        driver = self.driver
        driver.get(self.base_url + "/JADModelStoreFront/standardList")
        time.sleep(1)
        fd = FindElement(driver)
        time.sleep(2)
        #fd.getElementByName("H_main1_ipt_query").clear()  # 清空查询输入框
        # time.sleep(2)
        # fd.getElementByName('H_main1_ipt_query').send_keys('oo')  # 输入英文项目名“哦哦”
        # fd.getElementByName('H_main1_btn_query').click()  # 点击查询
        # time.sleep(2)
        #str = fd.getElementByName('H_main1_txt_result').text
        #str = str.split('/')
        #str1 = str[0]
        #str2 = str[1]
        #print str1     #oo
        #print str2     #噢噢
        if fd.getElementByName('H_main1_td_save'):
            fd.getElementByName('H_main1_btn_edit1').click()
            time.sleep(3)
        else:
            print "不存在已保存状态的工作流"
        self.assertIsNotNone(fd.getElementByName('H_workflow1_ipt_Cname'))
        self.assertIsNotNone(fd.getElementByName('H_workflow1_ipt_Ename'))

        fd.getElementByName('H_workflow1_ipt_Cname').clear()
        time.sleep(2)
        fd.getElementByName('H_workflow1_ipt_Cname').send_keys(u'啊啊')
        time.sleep(2)
        fd.getElementByName('H_workflow1_ipt_Ename').clear()
        fd.getElementByName('H_workflow1_ipt_Ename').send_keys('aa')
        time.sleep(2)
        #self.assertIsNone(fd.getElementByName('H_workflow1_slt_type'))
        #txt = fd.getElementByName('H_workflow1_ipt_nameEn').text
        #print txt
        #self.assertEqual(txt,str1)
        time.sleep(3)    #手动进行编辑

        fd.getElementByName('H_workflow1_btn_publish').click()
        time.sleep(3)

    def is_alert_present(self):  # 对弹窗异常的处理
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):  # 关闭警告以及对得到文本框的处理
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(Workflow)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    return test_result  # 返回测试结果

