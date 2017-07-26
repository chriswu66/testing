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
        #self.driver = webdriver.Chrome()
        config = TCinit()
        self.driver = config.getDriver()
        self.driver.maximize_window()
        self.base_url = config.getBase_url()
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Workflow(self):

        driver = self.driver
        fd = FindElement(driver)
        driver.get(self.base_url + "/JADModelStoreFront/standardList")
        time.sleep(3)
        if fd.getElementByName('H_main1_td_save'):
            fd.getElementByName('H_main1_btn_delete2').click()
            time.sleep(2)
            fd.getElementByName('H_main1_div_cancel1').click()
        else:
            print "不存在已保存状态的工作流"
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


