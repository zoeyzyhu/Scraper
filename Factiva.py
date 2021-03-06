#!/usr/bin/env python3.6

# ===============================================
# purpose: check # presence of brands in Factiva
# usage: ./scraper.py -u username -p password
# date: Nov. 03, 2019
# author: Zoey Hu
# contact: zyhu@gatech.edu
# ===============================================


from pylab import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import datetime
import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-u', 
	help = 'username'
	)
parser.add_argument('-p', 
	help = 'password'
	)
parser.add_argument('-nb', 
	help = 'index of brand to start',
	default = -999
	)
args = vars(parser.parse_args())


def LoadInput(filename):
	data = genfromtxt(filename, delimiter=',', dtype = str)
	nrow, ncol = data.shape
	brandid = data[1:,0]
	brand = data[1:,1]
	pbrand = data[1:,2]
	return nrow, ncol, brandid, brand, pbrand

def LoadOutput(filename):
	try:
		data=genfromtxt(filename, delimiter='\t')
		n = int(data[-1,0])
	except OSError:
		n = 0
	return n

def WaitUntil(xpath, s):
	wait = WebDriverWait(driver, s)
	element = wait.until(
		EC.element_to_be_clickable((By.XPATH, xpath))
	)

def Click(xpath):
	WaitUntil(xpath, 50)
	elem = driver.find_element_by_xpath(xpath)
	elem.click()

def SendKey(xpath, key):
	WaitUntil(xpath, 50)
	elem = driver.find_element_by_xpath(xpath)
	elem.send_keys(key)

def SelectOption(xpath, value):
	WaitUntil(xpath, 50)
	select = Select(driver.find_element_by_xpath(xpath))
	select.select_by_value(value)

def GetValue(xpath):
	WaitUntil(xpath, 50)
	elem = driver.find_element_by_xpath(xpath)
	value = elem.text
	return value

def Login(url, username, password, xpath_username, xpath_password,
	xpath_submit, xpath):
	driver.get(url)
	try: 
		WaitUntil(xpath_username, 50)
		SendKey(xpath_username, username)
		SendKey(xpath_password, password)
		Click(xpath_submit)
		WaitUntil(xpath, 32400)
	except TimeoutException:
		print('No need to login from start. Refreshed!')


def SearchOrRestart(xpath, url, username, password, xpath_username,
	xpath_password, xpath_submit):
	try:
		Click(xpath)
	except TimeoutException:
		print('Out of time. Refresh!')
		try:
			driver.get(url)
			Click(xpath)
		except TimeoutException:
			print('Refresh not successful. Re-login!')
			try:
				Login(url, username, password, xpath_username,
				 xpath_password, xpath_submit, xpath)
			except:
				print('Stucked. Help me Restart:)')

def ScrapeOrSwitch(xpath1, xpath2, url, signal):
	try:
		count = GetValue(xpath1)
	except TimeoutException:
		print('No publications found. Switch to "All".')
		try:
			count = GetValue(xpath2)
		except TimeoutException:
			print ('No result for publications. Something weired. Do it over!')
			driver.get(url)
			signal = False
			count = -999
	return count, signal



if __name__ == '__main__':

	# - load data
	filename1 = 'brands.csv'
	filename2 = 'count.csv'
	nrow, ncol, brandid, brand, pbrand = LoadInput(filename1)
	n = LoadOutput(filename2)

	# set initiating point
	nb = int('%s' % args['nb'])
	if nb != -999:
		n = nb
	print('Start from %d-th brand.' % n)

	# - set year range
	yy = list(range(2001, 2012))

	# - set driver
	driver = webdriver.Firefox()

	# - login
	url = 'http://libguides.gatech.edu/go.php?c=22546503'
	username = '%s' % args['u']
	password = '%s' % args['p']
	xpath_username = '//*[@id="username"]'
	xpath_password = '//*[@id="password"]'
	xpath_submit = '//*[@id="login"]/div[5]/input[4]'
	xpath_enter = '//*[@id="navmbm0"]/a'
	Login(url, username, password, xpath_username, xpath_password,
		xpath_submit, xpath_enter)
	# !!!!!! manual two-factor login required here

	# - get results
	for i in range(n,nrow):
		print(datetime.datetime.now())
		print(i)
		print(brand[i], pbrand[i])
		for y in yy:
			print(y)
			m = 1
			while m <= 12:
				try:
					signal = True
					f = open(filename2, 'a')
					# - 1. click on search in the navigation menu
					xpath_navi = '//*[@id="navmbm0"]/a'
					SearchOrRestart(xpath_navi, url, username, password, 
						xpath_username, xpath_password, xpath_submit)				

					# - 2. click on "search form"
					xpath_sform = '//*[@id="sfs"]/a'
					SearchOrRestart(xpath_sform, url, username, password, 
						xpath_username, xpath_password, xpath_submit)

					# - 3. enter search values
					# -- 3.1 input brand to 'This exact phrase'
					xpath_brand = '//*[@id="htx"]'
					key_brand = "'"+brand[i]+"'"
					SendKey(xpath_brand, key_brand)

					# -- 3.2 input parent brand to 'At least one of these words'
					xpath_pbrand = '//*[@id="otx"]'
					if pbrand[i] == 'P&G':
						key_pbrand = "'"+pbrand[i]+"', "+"'"+"Procter & Gamble"+"'"
					if pbrand[i] == 'JOHNSON AND JOHNSON':
						key_pbrand = "'"+pbrand[i]+"', "+"'"+"JOHNSON & JOHNSON"+"'"
					else:
						key_pbrand = "'"+pbrand[i]+"'"
					SendKey(xpath_pbrand, key_pbrand)

					# -- 3.3 input dates to 'Date -> Enter date range'
					# --- click and drop options of 'Date'
					xpath_date = '//*[@id="dr"]'
					Click(xpath_date)

					# --- select 'Enter date range'
					xpath_sdate = '//*[@id="dr"]'
					value_sdate = 'Custom'
					SelectOption(xpath_sdate, value_sdate)

					# --- enter values for 'from' and 'to'
					xpath_frmonth= '//*[@id="frm"]'
					xpath_frday = '//*[@id="frd"]'
					xpath_fryear = '//*[@id="fry"]'
					key_frmonth = str(m)
					key_frday = '1'
					key_fryear = str(y)
					xpath_tomonth= '//*[@id="tom"]'
					xpath_today = '//*[@id="tod"]'
					xpath_toyear = '//*[@id="toy"]'
					if m == 12:
						key_tomonth = str(1)
						key_today = '1'
						key_toyear = str(y+1)
					else:
						key_tomonth = str(m+1)
						key_today = '1'
						key_toyear = str(y)					
					SendKey(xpath_frmonth, key_frmonth)
					SendKey(xpath_frday, key_frday)
					SendKey(xpath_fryear, key_fryear)
					SendKey(xpath_tomonth, key_tomonth)
					SendKey(xpath_today, key_today)
					SendKey(xpath_toyear, key_toyear)

					# - 4. submit
					xpath_search = '//*[@id="btnSearchBottom"]'
					elem = driver.find_element_by_xpath(xpath_search)
					elem.click()

					# - 5. get # publications
					xpath1 = '//*[@id="headlineTabs"]/table[1]/tbody/tr/td/span[3]/a/span'
					xpath2 = '//*[@id="headlineTabs"]/table[1]/tbody/tr/td/span[2]/a/span'
					count, signal = ScrapeOrSwitch(xpath1, xpath2, url, signal)
					if signal == True:
						print(m, count)
						# - 6. write data
						f.write('%d\t' % i)
						f.write('%s\t' % brandid[i])
						f.write('%s\t' % brand[i])
						f.write('%s\t' % pbrand[i])
						f.write('%d\t' % m)
						f.write('%d\t' % y)
						f.write('%s\n' % count)
						f.close()
						sleep(random.randint(1, 4))	
						m += 1
				except TimeoutException:
					print(m)
					print('Time out. Do it over!')		

	# driver.close()
