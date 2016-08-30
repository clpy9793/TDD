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
        self.fail('stop!.')           
    
