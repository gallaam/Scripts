
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

ref_code=''
metamask_password=''
xpath_login = "//div[contains(@class, 'CustomBtn_primary__su8cB')]"
xpath_active = "//span[contains(@class, 'planetHeader_address__XJvdd')]"
xpath_check = "//div[contains(@class, 'planetHeader_hLeft__2ZEW8')]"
xpath_connect = "//div[contains(@class, 'style_connectWalletLabel__xAI78')]"
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
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        driver = webdriver.Chrome(service=Service(chrome_driver), options=chrome_options)
        return True
    except Exception as ex:
        log(f'ERROR {ex}')
        return False


def problem_start(ads_id):
	if not try_xpath(xpath_check):
		driver.refresh()
		driver.quit()
		timer(15)

		driver_init(ads_id)
		try_xpath(xpath_check)
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
		driver.get('https://reiki.web3go.xyz?ref={}'.format(ref_code))
		if not problem_start(ads_id):
			try_task()
		debug('start_task 0001')
		driver.quit()
		debug('start_task 0002 driver.quit')
		requests.get(f'{close_url}{ads_id}')
		debug('start_task 0003 requests.get')
	else:
		debug('start_task 0004 driver_init FALSE')
		driver.quit()
		requests.get(f'{close_url}{ads_id}')


def try_xpath(xpath, click=False, str='', sec=3):
	try:
		if click:
			debug('try_xpath click')
			element = WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
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
		if try_xpath(xpath_active):
			log(f'~ already authorized')
		else:
			metamask_login()
		time.sleep(10)
		driver.get('https://reiki.web3go.xyz/taskboard')
		time.sleep(10)
		if try_xpath("//span[text()='Mint']", True):
			metamask_request()
			log(f'+ passport mint')
		driver.get('https://reiki.web3go.xyz/taskboard')
		time.sleep(10)
		if try_xpath("//span[@class='style_title__mogbs' and text()='Welcome Gift']", False, '', 5):
			if try_xpath("//a[@class='style_button__+mLEr' and text()='Open ']", True):
				log(f'+ welcome gift take')
		if try_xpath("//a[@class='CheckInComponent_style_collectBtn__ZYOOg' and text()='Collect']", True, '', 5):
			log(f'+ collect')
		else:
			log(f'+ already collected')
		t=0
		while t!=1:
			if try_xpath("//a[@class='MoreTasksComponent_style_actionBtn__122z7']", True):
				
				while True:
					elements = WebDriverWait(driver, 5).until(
						ec.presence_of_all_elements_located((By.XPATH, "//span[@class='style_text__JS9Hv']"))
					)
					# Проходим по списку элементов и сохраняем текст в массив
					y=0
					for element in elements:
						log(element.text)
						log(elements[y-1].text=='Lifeform token airdrop in the future' and element.text=='All of the above')
						log(elements[y-1].text)
						log(element.text)
						
						#Yuliverse Fundamentals Quiz
						if element.text=='Purification of Terra  with Yuli common or above NFT (LV50)':
							element.click()
							log(f'+ Yuliverse Fundamentals Quiz begin')
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='https://special-event.yuliverse.com/' and elements[y+1].text=='https://special-event.yuliverse.com/sales/SkyTree':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='Yuliverse must have NFT to play':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='NFT from partners project':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='https://metalab-1.gitbook.io/the-white-paper-of-yuliverse/':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							log(f'+ Yuliverse Fundamentals Quiz end')
							break
						
						#Manta Network Fundamentals Quiz
						if element.text=='By using OP Stack, which is almost fully compatible with EVM and Solidity. It utilizes Celestia as the data availability layer, significantly reducing Gas costs, and includes a general ZK circuit. This allows direct calling of SDK or API to implement ZK functionality within the EVM environment.':
							element.click()
							log(f'+ Manta Network Fundamentals Quiz begin')
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if elements[y-1].text=='GameFi' and element.text=='All of the above':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=="Manta's Universal Circuits offer ZK-as-a-Service, allowing any Solidity developer to call Manta Pacific contracts through APIs to enable ZK features.":
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='Manta Atlantic is the canary network of Manta Pacific':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='Andreessen Horowitz':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							log(f'+ Manta Network Fundamentals Quiz end')
							break
							
						#Lifeform Fundamentals Quiz
						if element.text=='Korea':
							element.click()
							log(f'+ Lifeform Fundamentals Quiz begin')
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if elements[y-1].text=='Lifeform token airdrop in the future' and element.text=='All of the above':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='3000000':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if elements[y-1].text=='Metaverse' and element.text=='All of the above':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='Visual DID':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							log(f'+ Lifeform Fundamentals Quiz end')
							break
							
						#SecondLive Fundamentals Quiz
						if element.text=='Earn-bounty':
							element.click()
							log(f'+ SecondLive Fundamentals Quiz begin')
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='https://secondlive.world/creator':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=="SecondLive doesn't support NFT transactions for creators":
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='Earn by creating costumes, Spaces, dance shows':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='https://docs.secondlive.world/':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							log(f'+ SecondLive Fundamentals Quiz end')
							break
						
						#Map Protocol Fundamentals Quiz
						if element.text=='light client, ZK, Nakamoto Style, privileged roles':
							element.click()
							log(f'+ Map Protocol Fundamentals Quiz begin')
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if elements[y-1].text=='Anyone who wish to contribute and build together' and element.text=='All of the above':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='Decentralized security (Light-Client & zk)':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if element.text=='3':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							break
						if elements[y-1].text=='On-chain Governance' and element.text=='All of the above':
							element.click()
							try_xpath("//div[@class='style_right__qTLXR hover-item']", True)
							log(f'+ Map Protocol Fundamentals Quiz end')
							break
						y+=1
					
					if try_xpath("//div[@class='style_btn__CFfII hover-item']", True):
						break
				log(f'+ test end')
			else:
				t+=1
			time.sleep(10)
	except Exception as ex:
		log(ex)
def metamask_request():


	log(f'+ metamask open')
	time.sleep(10)
	driver.switch_to.window(driver.window_handles[-1])
	if try_xpath(xpath_password, True, 'pnwMY59O',5):
		log(f'+ password entered')
		time.sleep(5)
		if try_xpath(xpath_enter_button, True, '',5):
			log(f'+ login')
			time.sleep(5)
	driver.switch_to.window(driver.window_handles[-1])
	i=0
	while i!=1:
		if not try_xpath(xpath_btn_primary, True):
		#if len(driver.window_handles) == 1:
			#log(f'+ success')
			i+=1
		#else:
			
				#time.sleep(5)
	time.sleep(5)
	driver.switch_to.window(driver.window_handles[0])
		
def metamask_login():
	if try_xpath(xpath_login, True):
		time.sleep(5)
		if try_xpath(xpath_connect, True, '',5):
			log(f'+ metamask open')
			time.sleep(5)
			driver.switch_to.window(driver.window_handles[-1])
			if try_xpath(xpath_password, True, metamask_password,5):
				log(f'+ password entered')
				time.sleep(5)
				if try_xpath(xpath_enter_button, True, '',5):
					log(f'+ login')
					time.sleep(5)
					driver.switch_to.window(driver.window_handles[-1])
					i=0
					time.sleep(5)
					while i!=1:
						if len(driver.window_handles) == 1:
							log(f'+ metamask window closed')
							i+=1
						else:
							if try_xpath(xpath_btn_primary, True, '',5):
								time.sleep(5)
					time.sleep(10)
					if len(driver.window_handles) > 1:
						driver.switch_to.window(driver.window_handles[-1])
						i=0
						while i!=1:
							if len(driver.window_handles) == 1:
								log(f'+ metamask window closed')
								i+=1
							else:
								if try_xpath(xpath_btn_primary, True, '',5):
									time.sleep(5)
					driver.switch_to.window(driver.window_handles[0])
		else:
			reload_page()
	else:
		reload_page()


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
    file = open("log_task.txt", "a")  # append mode
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