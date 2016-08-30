#-*- coding:utf-8 -*-
import sys
import time
import unittest


from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from .base import FunctionalTest




#global
path = '/Users/qs/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'

    

class LayoutAndStylingTest(FunctionalTest):


    def test_layout_and_styling(self):
        #edith 访问首页
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

        #输入框居中显示
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x']+input_box.size['width']/2,
            512,
            delta=5
        )

        input_box.send_keys("testint\n")
        input_box = self.get_item_input_box()
        self.assertAlmostEqual(
            input_box.location['x']+input_box.size['width']/2,
            512,
            delta=5,
        )







    