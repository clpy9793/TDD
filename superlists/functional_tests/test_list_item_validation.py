#-*- coding:utf-8 -*-
import sys
import time
import unittest

from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from django.core.exceptions import ValidationError
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from .base import FunctionalTest
from lists.models import List,Item


   

class ItemValidationTest(FunctionalTest):

    @skip
    def test_can_not_add_empty_list_items(self):
        '不能提交为空的事项'
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.RETURN)

        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text,"You can't have an empty list item")

        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys('\n')

        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has_error')
        self.assertEqual(error.text,"You can't have an empty list item")


        self.get_item_input_box().send_keys('Mike tea\n')

        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Mike tea')
        
    def test_can_not_add_duplicate_items(self):
        #输入一个待办事项
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')

        #输入一个重复的代办事项
        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table("1: Buy wellies")
        
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text,"You've already got this in your list")

    

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text='text',list=list1)
        item = Item(text='text',list=list2)
        item.full_clean()   #不该抛出异常







    
