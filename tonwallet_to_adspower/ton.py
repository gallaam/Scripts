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
import pyperclip
from _utils import send_boc, get_seqno, run_get_method, fetch_items_by_collection

from tonsdk.contract.wallet import WalletVersionEnum, Wallets
from tonsdk.utils import bytes_to_b64str
from tonsdk.crypto import mnemonic_new
from tonsdk.utils import to_nano, bytes_to_b64str, Address
from tonsdk.contract.token.ft import JettonWallet

xpath_start_import="//button[@id='start_importBtn']"
xpath_start_confirm="//button[@id='connectConfirm_okBtn']"
xpath_import_input="//input[@id='importsInput0']"
xpath_import_continue="//button[@id='import_continueBtn']"
xpath_import_create="//button[@id='createPassword_continueBtn']"
xpath_go="//button[@id='readyToGo_continueBtn']"
xpath_go_connect="//div[contains(text(), 'Connect Wallet')]"
xpath_go_all="//div[contains(text(), 'View all')]"
xpath_go_wallet="//div[contains(text(), 'TON Wallet')]"


open_url = 'http://local.adspower.net:50325/api/v1/browser/start?user_id='
close_url = 'http://local.adspower.net:50325/api/v1/browser/stop?user_id='
driver: WebDriver
debug_on = False
OWNER_SEED = ''
OWNER_WALLET_VERSION = 'v4r2'
TOP_UP=False
amount_topup=0.1
password='password'

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

def start_task(ads_id):
	debug(f'start_task')

	global driver
	if driver_init(ads_id):
		close_other_handles()
		driver.get('chrome-extension://nphplpgoakhhjchkkhmiggakijnkhfnd/index.html')
		try_task(ads_id)
		driver.quit()
		debug('task 0001 driver.quit')
		requests.get(f'{close_url}{ads_id}')
	else:
		debug('start_task 0001 driver_init FALSE')
		driver.quit()
		requests.get(f'{close_url}{ads_id}')


def try_xpath(xpath, click=False, str='', sec=3):
	try:
		if click:
			debug(f'try_xpath click {xpath}')
			element = WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
			if xpath!="//button[@class='ant-btn main-btn !h-11 !min-w-auto !w-37']":
				driver.execute_script("return arguments[0].scrollIntoView();", element)
			element.click()
		else:
			debug(f'try_xpath: {xpath}')
			WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, xpath)))
		
		if str:
			h=0
			for word in str:
				print(word)
				# Здесь вы можете выполнить любое действие для каждого слова в мнемонической фразе
				#print(word)  # Например, выведем каждое слово на экран
				debug(f'try_xpath: {xpath} input data')
				element = WebDriverWait(driver, sec).until(ec.presence_of_element_located((By.XPATH, "//input[@id='importsInput{}']".format(h))))
				#element.click()
				#actions = ActionChains(driver)
				#actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
				#for char in str:
				element.send_keys(word)
					#time.sleep(0.1)
				h=h+1
		debug("True")
		return True
	except Exception as ex:
		debug(ex)
		return False


def try_task(ads_id):
	
	
	
	if try_xpath(xpath_start_import,True):
		#timer(15)
		wallet_workchain = 0
		wallet_version = WalletVersionEnum.v4r2
		wallet_mnemonics = mnemonic_new()

		_mnemonics, _pub_k, _priv_k, wallet = Wallets.from_mnemonics(
			wallet_mnemonics, wallet_version, wallet_workchain)
		query = wallet.create_init_external_message()
		base64_boc = bytes_to_b64str(query["message"].to_boc(False))

		mnemonics_string = ' '.join(wallet_mnemonics)
		wallets_info("{};{};{};{}".format(ads_id,wallet.address.to_string(),wallet.address.to_string(True, True, True),mnemonics_string))
		if TOP_UP:
			_, pk, sk, wallet0 = Wallets.from_mnemonics(OWNER_SEED.split(' '), OWNER_WALLET_VERSION)
			wallet_address0 = wallet0.address.to_string(1, 1, 1)
			wallet_seqno0 = get_seqno(wallet_address0)
			wallet_seqno = get_seqno(wallet)
			"""transfer"""
			query = wallet0.create_transfer_message(to_addr=wallet.address.to_string(),
											  amount=to_nano(float(amount_topup), 'ton'),
											  payload='message',
											  seqno=int(wallet_seqno0))


			"""then send boc to blockchain"""
			send_boc(query['message'].to_boc(False))
			
			timer(10)
		
		if try_xpath(xpath_import_input,False,wallet_mnemonics):
			timer(2)
		if try_xpath(xpath_import_continue,True):
			timer(12)
			element = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, "//input[@id='createPassword_input']")))
			element.send_keys(password)
			element = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, "//input[@id='createPassword_repeatInput']")))
			element.send_keys(password)
		if try_xpath(xpath_import_create,True):
			timer(2)
		if try_xpath(xpath_go,True):
			timer(2)
	else:
		print(ads_id,"already created")
		timer(2)

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

def wallets_info(txt):
    file = open("log_wallets_info.txt", "a")  # append mode
    file.write(f"{txt}\n")
    file.close()
	
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