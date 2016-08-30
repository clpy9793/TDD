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

   

class ItemValidationTest(FunctionalTest):


    def test_can_not_add_empty_list_items(self):
        '不能提交为空的事项'
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.RETURN)

        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text,"You can't have an empty list item")

        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        self.browser.find_element_by_id('id_new_item').send_keys('\n')

        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text,"You can't have an empty list item")


        self.browser.find_element_by_id('id_new_item').send_keys('Mike tea\n')

        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Mike tea')









    
