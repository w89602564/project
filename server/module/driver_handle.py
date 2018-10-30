# -*- coding: utf-8 -*-
import os
import time
import random
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from module import const

USR = None
PWD = None
g_handle = None

def _get_default_pwd():
	global USR
	global PWD
	path = 'data/pwd'
	if os.path.exists(path):
		with open(path, 'rb') as f:
			data = f.read().decode('utf-8')
			USR, _, PWD = data.partition(',')

_get_default_pwd()

def wait():
	sleep(0.2)

class Handle(object):
	def __init__(self, driver):
		super(Handle, self).__init__()
		self.driver = driver

	def exit(self):
		self.driver.close()
		self.driver.quit()

	def get_cookie_dict(self):
		return self.driver.get_cookies()

	def auto_slider(self, slider, refresh):
		while True:
			try:
				# 定位滑块元素,如果不存在，则跳出循环
				source = self.driver.find_element_by_xpath(slider)
				if not source.is_displayed():
					break
			except NoSuchElementException:
				try:
					a = self.driver.find_element_by_xpath(refresh)
				except NoSuchElementException:
					break
				else:
					if a and a.is_displayed():
						a.click()
						wait()
						continue
			except StaleElementReferenceException:
				break
			else:
				try:
					# 定义鼠标拖放动作
					action = ActionChains(self.driver)
					# self.driver.implicitly_wait(200)
					sleep(1)
					# action.click_and_hold(source).perform()
					try:
						# action.move_by_offset(2, 0).perform()  # 平行移动鼠标
						# print '333333333'
						action.drag_and_drop_by_offset(source, 400, 0).perform()
						# return self.driver.execute_script("return _n")
					except Exception:
						break

					# 查看是否认证成功，获取text值 //*[@id="nc_1__scale_text"]/span
					text = self.driver.find_element_by_xpath("//*[@id='nc_1__scale_text']/span")
					if text.text.startswith(u'验证通过'):
						print ('成功滑动')
						break
					if text.text.startswith(u'请点击'):
						print ('成功滑动')
						break
				except Exception:
					pass

	def login(self, usr=None, pwd=None):
		self.driver.get("https://login.taobao.com/member/login.jhtml")
		wait()
		for idx in range(3):
			# load the switch
			try:
				i = random.randint(10, 30)
				element = self.driver.find_element_by_xpath("//*[@id='J_Quick2Static']")
				actions = ActionChains(self.driver)
				actions.move_to_element_with_offset(element, -i, 0).click().perform()
				element.click()
			except ElementNotVisibleException:
				pass
			wait()
			if idx == 0:
				username = self.driver.find_element_by_name("TPL_username")
				# if not username.is_displayed:
				# 	self.driver.implicitly_wait(20)
				# 	self.driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
				for a in usr or USR:
					wait()
					username.send_keys(a)
				wait()
			username.send_keys(Keys.TAB)
			wait()
			pwc = self.driver.find_element_by_name("TPL_password")

			for a in pwd or PWD:
				wait()
				pwc.send_keys(a)

			self.auto_slider("//*[@id='nc_1_n1z']", "//*[@id='nocaptcha']")
			self.driver.find_element_by_id("J_SubmitStatic").click()
			wait()
			if 'login.taobao.com' not in self.driver.current_url:
				break
		return self.get_cookie_dict()

def login():
	global g_handle
	if g_handle is None:
		option = webdriver.ChromeOptions()
		option.add_argument('log-level=3')
		driver = webdriver.Chrome(executable_path=const.CHROME_PATH, chrome_options=option)
		driver.delete_all_cookies()
		driver.maximize_window()
		g_handle = Handle(driver)
	g_handle.login()
