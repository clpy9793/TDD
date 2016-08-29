#-*- coding:utf-8 -*-
import unittest
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

#功能测试

class NewVisitorTest(StaticLiveServerTestCase):


    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        #edith 访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)

        #输入框居中显示
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x']+input_box.size['width']/2,
            512,
            delta=5
        )

        input_box.send_keys("testint\n")
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x']+input_box.size['width']/2,
            512,
            delta=5,
        )

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        
        #网页的标题和头部都有To-Do
        self.assertIn('To-Do',self.browser.title)
        head_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',head_text)
        

        #代办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                input_box.get_attribute('placeholder'),
                'Enter a to-do item'
            )

        #第一次更新
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)

        #点击回车后带到一个新的URL 
        #该页面显示了待办清单

        #用户Edith的待办清单url
        edith_list_url = self.browser.current_url    
        self.assertRegex(edith_list_url,'/lists/.+')    
        self.check_for_row_in_list_table("1: Buy peacock feathers")        

        #第二次更新
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        #第二次更新待办清单
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        ##使用新会话  切换用户francis
        ##确保用户信息不会泄漏

        self.browser.quit()
        self.browser = webdriver.Firefox()

        #francis访问首页 不出现Edith的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        #用户输入一个待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                input_box.get_attribute('placeholder'),
                'Enter a to-do item'
            )

        #文本框输入事项 回车提交
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        #获得唯一URL Edith和Francis的清单不同
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)

        #当前页面仍然没有Edith的清单

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)



        
        
    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows =  table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])






#global
path = '/Users/qs/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'




    