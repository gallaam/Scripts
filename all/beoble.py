
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

metamask_password=''
xpath_check_step_one = "//div[@class='sc-afdafdb-0 clwYnU' and text()='Start chatting in beoble.']"
xpath_check_step_two = "//button[@class='sc-5f5dcad5-0 esQpMx']"



xpath_login = "//button[text()='Connect Wallet']"
xpath_connect = "//div[@class='iekbcc0' and text()='MetaMask']"
xpath_verify = "//div[text()='Verify Wallet']"
xpath_retrieve = "//div[text()='Retrieve Account']"
xpath_active = "//span[contains(@class, 'planetHeader_address__XJvdd')]"


xpath_password = "//*[@id='password']"
xpath_enter_button = "//button[@class='button btn--rounded btn-default']"
xpath_btn_primary = "//button[contains(@class, 'btn-primary')]"
xpath_signature = "//div[contains(@class, 'signature-request-siwe-message')]"
open_url = 'http://local.adspower.net:50325/api/v1/browser/start?user_id='
close_url = 'http://local.adspower.net:50325/api/v1/browser/stop?user_id='
driver: WebDriver
debug_on = False

			
def driver_init(ads_id):
	global driver
	try:
		resp = requests.get(f'{open_url}{ads_id}').json()
		chrome_driver = resp["data"]["webdriver"]
		chrome_options = Options()
		chrome_options.add_argument("--disable-notifications")
		chrome_options.add_argument("allow-file-access-from-files")
		chrome_options.add_argument("use-fake-device-for-media-stream")
		chrome_options.add_argument("use-fake-ui-for-media-stream")
		chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
		driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
		driver.set_window_size(1300, 1000)
		return True
	except Exception as ex:
		log(f'ERROR {ex}')
		return False


def problem_start(ads_id):

	if not try_xpath("//input[@placeholder='Search Address, ENS, Lens, name...']"):
		driver.refresh()
		if try_xpath("//input[@placeholder='Search Address, ENS, Lens, name...']"):
			return False;
		driver.quit()
		timer(5)
		
		driver_init(ads_id)
		driver.quit()
		timer(10)

		start_task(ads_id)
		return True
	else:
		return False


def start_task(ads_id):
	debug(f'start_task')

	global driver
	if driver_init(ads_id):
		close_other_handles()
		driver.get('https://beoble.app/')
		try_task()
		if not problem_start(ads_id):
			debug('start_daily')
			driver.get('https://beoble.app/?id=27ef1535-538d-4081-96d5-eb3048d88a7e')
			try_daily()
		driver.quit()
		debug('start_task 0002 driver.quit')
		requests.get(f'{close_url}{ads_id}')
		debug('start_task 0003 requests.get')
	else:
		debug('start_task 0004 driver_init FALSE')
		driver.quit()
		requests.get(f'{close_url}{ads_id}')


def try_xpath(xpath, click=False, str='', sec=5):
	try:
		if click:
			debug('try_xpath click')
			debug(xpath)
			element = WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
			element = WebDriverWait(driver, sec).until(ec.element_to_be_clickable((By.XPATH, xpath)))
			driver.execute_script("return arguments[0].scrollIntoView();", element)
			debug(element.text)
			element.click()
		else:
			debug(f'try_xpath: {xpath}')
			WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
		if str>'':
			debug(f'try_xpath: {xpath} input data')
			element = WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
			for char in str:
				element.send_keys(char)
				time.sleep(0.1)

		return True
	except Exception as ex:
		return False


def try_task():
	try:
		if try_xpath(xpath_check_step_two):
			log(f'~ already authorized')
		else:
			log(f'~ no authorized')
			metamask_login()
			timer(10)
			#while True:
				#if not try_xpath("//button[@class='sc-5f5dcad5-0 sc-f5094359-0 eFrzre ggsDqA' and @disabled]", False):
					#break
				#else:
					#debug("wait")

			if try_xpath(xpath_verify, True):
				metamask_request()
				timer(3)
			if try_xpath(xpath_retrieve, True):
				metamask_request()
				timer(3)
			if len(driver.window_handles) > 1:
				metamask_request()
				timer(3)
		timer(3)
		if not try_xpath("//input[@placeholder='Search Address, ENS, Lens, name...']"):

			timer(3)
			if try_xpath("//input[@placeholder='Invitation code']", True, code(),5):
				timer(3)
			if try_xpath("//div[text()='Next']", True):
				log(f'~ invite code approved')
				timer(3)
			elements = WebDriverWait(driver, 5).until(
				ec.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'vFPdb')]"))
			)
			random.choice(elements).click()
			try_xpath("//div[text()='Next']", True)
			x=0
			while x!=1:
				try_xpath("//input[@placeholder='beoble']", True, name(),5)
				timer(3)
				if try_xpath("//div[@class='sc-afdafdb-0 bnpYjZ']", False):
					x+=1
					log(f'~ username selected')
				else:
					element = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH, "//input[@placeholder='beoble']")))
					element.send_keys(Keys.CONTROL + 'a')
					element.send_keys(Keys.BACKSPACE)
					time.sleep(3)
			if try_xpath("//div[text()='Next']", True):
				log(f'~ register complete')
				timer(3)
	except Exception as ex:
		log(ex)

def try_daily():

	try:
		
		timer(3)
		follow=0
		react=0
		sreact=0
		msg=0
		
		
		while True:
		
			if msg<1:
				if try_xpath("//div[@placeholder='Type a message...']", True, message(),5):
					if try_xpath("//button[@class='sc-5f5dcad5-0 sc-7cd36905-2 esQpMx bMeyzI']", True):
						msg+=1
						log(f'~ Daily {msg} GM')

			try:
				el = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.XPATH,"//div[@class='sc-f3c65d15-8 bKHeJr']")))
				actions = ActionChains(driver)
				actions.move_to_element(el).perform()
				el.send_keys(Keys.PAGE_UP * 1)
			except:
				pass
			timer(3)
			if len(driver.window_handles) > 1:
				driver.switch_to.window(driver.window_handles[0])
			if follow==0:
				if try_xpath("//div[@class='sc-2862f7fd-0 fwDGet']", True):
					if try_xpath("//button[text()='Follow']", True):
						log(f'~ Follow 1 accounts')
						follow+=1
						#break
						driver.refresh()
			
			#Super reaction block
			try:
				
				if sreact==0:
					s_element = driver.find_element(By.XPATH, "//button[@class='sc-5f5dcad5-0 sc-f85573f7-0 bSdNtl dnYQmd sc-81ed977b-0 eRKUXg']")
					actions = ActionChains(driver)
					actions.move_to_element(s_element).perform()
				
					s_element = driver.find_element(By.XPATH, "//button[@class='sc-5f5dcad5-0 sc-f85573f7-0 bSdNtl dnYQmd sc-81ed977b-0 eRKUXg']")
					actions = ActionChains(driver)
					actions.move_to_element(s_element).perform()
					timer(1)
					if try_xpath("//div[text()='Send 1 pts']", True):
						timer(1)
						if try_xpath("//button[text()='Confirm and send']", True):
							log(f'~ Super reaction complete')
							sreact+=1
							driver.refresh()
				
							
					

			except Exception as ex:
				pass
				
			#Reactions block
			try:
				if react<15:
					r_elements = driver.find_elements(By.XPATH, "//div[@class='sc-c0ef3df3-1 bQFwLu']")
					for r_element in r_elements:
						react+=1
						r_element.click()
						log(f'~ React to {react} messages')
						timer(1)
						if react>15:
							break
						
			except Exception as ex:
				pass
			#check
			if react>14 and sreact>0 and msg>0:
				log(f'~ React to 15 messages complete')
				break

		timer(3)
		elements = WebDriverWait(driver, 5).until(
			ec.presence_of_all_elements_located((By.XPATH, "//button[@class='sc-c58f69d7-0 dOgfhc']"))
		)
		elements[2].click()
		timer(3)
		try_xpath("//button[@class='sc-5f5dcad5-0 kIkdgQ']", True)
		timer(3)
		elements = WebDriverWait(driver, 5).until(
			ec.presence_of_all_elements_located((By.XPATH, "//button[@class='sc-5f5dcad5-0 sc-5d501f2f-1 jkoYvF jYKNzE']"))
		)
		for element in elements:
			element.click()
			timer(1)
		log(f'~ Rewards collect complete')
	except Exception as ex:
		log(ex)
		
def code():
	with open("_invites.txt", "r") as f:
		ids = [row.strip() for row in f]
	random.shuffle(ids)
	return ids[0]
	
def name():
	with open("_names.txt", "r") as f:
		ids = [row.strip() for row in f]
	random.shuffle(ids)
	return ids[0]

def message():
	with open("_messages.txt", "r") as f:
		ids = [row.strip() for row in f]
	random.shuffle(ids)
	return ids[0]


def metamask_request():
	timer(10)
	while True:
		driver.switch_to.window(driver.window_handles[1])
		if try_xpath(xpath_password, True, metamask_password,5):
			log(f'+ password entered')
			timer(3)
			if try_xpath(xpath_enter_button, True):
				log(f'+ login click')
		else:
			timer(3)
			log(f'+ 211')
			try_xpath(xpath_btn_primary, True)
			
		if len(driver.window_handles) == 1:
			driver.switch_to.window(driver.window_handles[0])
			break
		
def metamask_login():
	
	while True:
		
		if len(driver.window_handles) == 1:
			#click connect & click metamask
			if try_xpath(xpath_login, True):
				log(f'+ modal open')
				timer(3)
				if try_xpath(xpath_connect, True,'',10):
					log(f'+ metamask open')
				else:
					reload_page()
			
			timer(3)
			if len(driver.window_handles) > 1:
					log(f'+ metamask tab select')
					driver.switch_to.window(driver.window_handles[1])
			
			timer(3)
		else:
			driver.switch_to.window(driver.window_handles[1])
			if try_xpath(xpath_password, True, metamask_password,5):
				log(f'+ password entered')
				timer(3)
				if try_xpath(xpath_enter_button, True):
					log(f'+ login click')
				
			else:
				timer(3)
				log(f'+ 111')
				try_xpath(xpath_btn_primary, True)
				timer(6)
				if len(driver.window_handles) == 1:
					driver.switch_to.window(driver.window_handles[0])
					break


def reload_page():
	log(f'reload page')
	try:
		driver.refresh()
	except:
		pass
	try_task()


def close_other_handles():
    curr = driver.current_window_handle
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != curr:
            driver.close()


def log(txt):
    print(txt)
    file = open("log_task_beoble.txt", "a")  # append mode
    file.write(f"{txt} \n")
    file.close()


def debug(txt):
    if debug_on:
        log(txt)



def timer(sec):
    if sec >= 0:
        print(f'wait: {sec} sec.   ', end='')
        time.sleep(1)
        print('\r', end='')
        sec -= 1
        timer(sec)


if __name__ == '__main__':
	with open("_ids.txt", "r") as f:
		ids = [row.strip() for row in f]

	#random.shuffle(ids)
	log(datetime.now())

	for index, item in enumerate(ids, start=0):
		log(f'========= {index+1}/{len(ids)} =========')
		log(f'start profile {item}')

		start_task(item)

		log(f'finish profile {item}')
		if (index+1) < len(ids):
			t = random.randint(5, 15)
			timer(t)
		time.sleep(1)
	log('*************************')
	log(f'ALL PROFILES COMPLETED')
	log('*************************')
	log(datetime.now())