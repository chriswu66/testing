# -*- coding: utf-8 -*-
# 折中方案
# 在main.py文件中调用此文件加载TestCaseScript文件来执行
import unittest
def execFunc(s):
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
# def main(s):
#     print "main()"
#     suite = unittest.TestLoader().loadTestsFromTestCase(s)
#     test_result = unittest.TextTestRunner(verbosity=2).run(suite)
#     return test_result # 返回测试结果