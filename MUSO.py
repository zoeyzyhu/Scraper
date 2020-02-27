#!/usr/bin/env python3.6

# ===============================================
# purpose: download all data available at MUSO

# date: Dec. 08, 2019
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
import os 
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--index', 
	default = '-999',
	help = 'index of the country to be continued'
  )
parser.add_argument('--num', 
	default = '-999',
	help = 'index of items processed'
  )
args = vars(parser.parse_args())



def WaitUntil(xpath, s):
	wait = WebDriverWait(driver, s)
	element = wait.until(
		EC.element_to_be_clickable((By.XPATH, xpath))
	)

def Click(xpath):
	WaitUntil(xpath, 500)
	elem = driver.find_element_by_xpath(xpath)
	elem.click()

def SendKey(xpath, key):
	WaitUntil(xpath, 500)
	elem = driver.find_element_by_xpath(xpath)
	elem.send_keys(key)


def Login(url, username, password, xpath_username, xpath_password,
	xpath_submit):
	driver.get(url)
	try: 
		WaitUntil(xpath_username, 500)
		sleep(5)
		SendKey(xpath_username, username)
		SendKey(xpath_password, password)
		Click(xpath_submit)
	except NoSuchElementException:
		print('Login failed.')


if __name__ == '__main__':

	# input
	index = '%s' % args['index']
	if index == '-999':
		nstart = 0
	else:
		nstart = int(index) 

	printn = '%s' % args['num']
	if printn == '-999':
		n = 0
	else:
		n = int(printn)

	print(nstart, n)


	# Set driver and Firefox preferences for auto-download
	fp = webdriver.FirefoxProfile()
	fp.set_preference('browser.preferences.instantApply',True)
	fp.set_preference('browser.download.folderList',2)
	fp.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
	fp.set_preference('browser.helperApps.alwaysAsk.force',False)
	fp.set_preference('browser.download.manager.showWhenStarting',False)
	driver = webdriver.Firefox(firefox_profile=fp)

	# login
	url = 'https://login.muso.com/login?state=g6Fo2SAwTDdERm51NVRqeE9CWHZodlEydTdRYTlIcXlzX09sZKN0aWTZIDZsRk9uT29FYkVZZ2QzQ3IyX0o1bXZwVmtVdGd4RW1Ko2NpZNkgbmVra3p4NUtSbTFmYVY2N2F6cFF4OWhEVkZ0MVpROVY&client=nekkzx5KRm1faV67azpQx9hDVFt1ZQ9V&protocol=oauth2&response_type=id_token&redirect_uri=https%3A%2F%2Fdashboard.muso.com&nonce=NONCE'
	username = 'koushyar.rajavi@scheller.gatech.edu'
	password = 'BbQc`j4p!S{D'
	xpath_username = '/html/body/div/div/div[2]/form/div/div/div[3]/span/div/div/div/div/div/div/div/div/div/div[1]/div/input'
	xpath_password = '/html/body/div/div/div[2]/form/div/div/div[3]/span/div/div/div/div/div/div/div/div/div/div[2]/div/div/input'
	xpath_submit = '/html/body/div/div/div[2]/form/div/div/button'
	xpath_login = '//*[@id="support"]'
	for replicate in range(2): # - first machine login won't be successful
		Login(url, username, password, xpath_username, xpath_password, xpath_submit)
		sleep(10)



	# set query variables
	# - industries
	industry = ['Music', 'Film', 'TV', 'Software', 'Publishing']
	industry_path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-type/div/div/button/span[1]'
	industry_option_path = ['/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-type/div/div/div/ul/li[1]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-type/div/div/div/ul/li[2]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-type/div/div/div/ul/li[3]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-type/div/div/div/ul/li[4]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-type/div/div/div/ul/li[5]/a']

	# - regions
	region = ['European Union', 'MENA', 'APAC', 'LATAM', 'Africa', 'BRIICS', 'Southeast Asia', 'Caribbean', 
	'Southern Europe', 'Western Europe', 'OECD Regions', 'Afghanistan', 'Aland Islands', 'Albania', 'Algeria',
	'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 
	'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 
	'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire Sint Eustatius and Saba',
	'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 
	'British Virgin Islands', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 
	'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 
	'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo, Democratic Republic of the',
	'Congo&nbsp;(Brazzaville)', 'Cook Islands', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus',
	'Czech Republic', 'Côte d\'Ivoire', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador',
	'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 
	'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories',
	'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 
	'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 
	'Heard Island and Mcdonald Islands', 'Holy See&nbsp;(Vatican City State)', 'Honduras', 
	'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 
	'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 
	'Kyrgyzstan', 'Lao PDR', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 
	'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 
	'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 
	'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 
	'Nauru', 'Nepal', 'Netherlands', 'Netherlands Antilles', 'New Caledonia', 'New Zealand', 'Nicaragua', 
	'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea', 'Northern Mariana Islands', 'Norway', 
	'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 
	'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russian Federation', 'Rwanda', 
	'Réunion', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Pierre and Miquelon', 
	'Saint Vincent and Grenadines', 'Saint-Barthélemy', 'Saint-Martin (French part)', 'Samoa', 'San Marino', 
	'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 
	'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 
	'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'State of Palestine', 'Sudan', 'Suriname', 
	'Svalbard and Jan Mayen Islands', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan, Republic of China', 
	'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 
	'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 
	'United Arab Emirates', 'United Kingdom', 'United States Minor Outlying Islands', 'United States of America', 
	'Unknown', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 'Viet Nam', 'Virgin Islands, US', 
	'Wallis and Futuna Islands', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
	region_path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-region-country/div/div/button/span[1]'
	region_option_path = []
	for i in range(1,263):
		if i == 12:
			continue
		else:
			path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-region-country/div/div/div/ul/li[' + str(i) + ']/a'
			region_option_path.append(path)


	# - delivery methods
	delivery = ['Download', 'Private Torrent', 'Public Torrent', 'Stream Ripper', 'Web Download', 'Streaming']
	delivery_path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/button/span[1]'
	delivery_option_path = ['/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/div/ul/li[1]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/div/ul/li[2]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/div/ul/li[3]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/div/ul/li[4]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/div/ul/li[5]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-site-classification/div/div/div/ul/li[6]/a']

	# - traffic sources
	traffic = ['Referrals', 'Display Ads', 'Search', 'Social', 'Mail', 'Direct']
	traffic_path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/button/span[1]'
	traffic_option_path = ['/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/div/ul/li[1]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/div/ul/li[2]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/div/ul/li[3]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/div/ul/li[4]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/div/ul/li[5]/a',
	'/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-source-type/div/div/div/ul/li[6]/a']


	# - date
	date_path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-period-piracy-by-industry/div/div/button/span[1]'
	date_pageup = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-period-piracy-by-industry/div/div/div/div/div[1]/div[2]/table/thead/tr/th[1]'
	date_jan2017 = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-period-piracy-by-industry/div/div/div/div/div[1]/div[2]/table/tbody/tr[1]/td[1]'
	date_pagedown = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-period-piracy-by-industry/div/div/div/div/div[2]/div[2]/table/thead/tr/th[3]'
	date_oct2019 = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-period-piracy-by-industry/div/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[1]'
	date_apply = '/html/body/muso-root/div/div[1]/div[1]/div/muso-filter-period-piracy-by-industry/div/div/div/div/div[3]/div/button[1]'

	# - download
	dwld_path = '/html/body/muso-root/div/div[1]/div[1]/muso-line-chart-piracy-by-industry/div/div[1]/div[2]/muso-csv-export/a/span[2]'
	file_path =  '/home/zhiying/Downloads/piracy_by_industry-piracy_site_visits_over_time.csv'
	refile_path = '/home/zhiying/Dropbox (GaTech)/Projects/materials/'

	# - clear filters
	clear_path = '/html/body/muso-root/div/div[1]/div[1]/div/muso-clear-filters/div/a'

	# selection and download
	for a in range(nstart,261): # - region
		print(datetime.datetime.now())
		print('country ' + str(a))
		for b in range(5): # - industry
			for c in range(6): # - delivery method
				for d in range(6): # - traffic
					Click(industry_path)
					Click(industry_option_path[b])
					Click(region_path)
					Click(region_option_path[a])

					Click(date_path)
					Click(date_pageup)
					Click(date_jan2017)
					Click(date_pagedown)
					Click(date_oct2019)
					Click(date_apply)

					Click(delivery_path)
					Click(delivery_option_path[c])
					Click(traffic_path)
					Click(traffic_option_path[d])

					Click(dwld_path)
					Click(clear_path)
					sleep(3)

					filename = region[a] + industry[b] + delivery[c] + traffic[d]
					os.rename(file_path, refile_path + '%s.csv' % filename)
					n += 1
					print(str(n) + ':' + filename)
					sleep(3)

# driver.close()
