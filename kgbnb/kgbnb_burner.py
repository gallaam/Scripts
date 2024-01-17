from web3 import Web3
import requests
import time

# Подключение к BSC (Binance Smart Chain) с использованием Infura
bsc_rpc_endpoint = "https://bsc-dataseed.bnbchain.org"
web3 = Web3(Web3.HTTPProvider(bsc_rpc_endpoint))

# Приватный ключ вашего кошелька BSC
private_key = ""

# Адрес вашего кошелька
wallet_address = web3.to_checksum_address("")

# Адрес получателя
recipient_address = web3.to_checksum_address("0x6f70e2F0F0f73E79Ef810781Eee1273EF17eC5Aa")

api_url = "https://api.bscscan.com/api"
bscscan_api_key = "V1EK86W24MDJFURAEHJXUDEZYVJDB6Z6E7"

# Эндпоинт для получения транзакций токенов по контракту на BSC
token_tx_endpoint = f'https://api.bscscan.com/api?module=account&action=tokennfttx&address={wallet_address}&contractaddress={recipient_address}&apikey={bscscan_api_key}'

response = requests.get(token_tx_endpoint)
#print(response.json())

# Отправка запроса к API BscScan
response = requests.get(token_tx_endpoint)
data = response.json()
amount_bnb = 0
amount_wei = Web3.to_wei(amount_bnb, 'ether')
burned=[]
token_ids = []
# Проверка успешности запроса
if data['status'] == '1':
	token_transactions = data['result']

	# Вывод информации о транзакциях
	for tx in token_transactions:
		try:
			print(tx['tokenID'])
			token_ids.append(tx['tokenID'])
			
		except:
			pass
else:
	print(f'Error: {data["message"]}')
print(token_ids)


filtered_array = [item for item in token_ids if item not in burned]
print(filtered_array)
new_burn=[]
for item in filtered_array:
	print(item)
	new_burn.append(item)
	gas_price=web3.eth.gas_price
	function_signature = '0x42966c68'
	inputData = f'{function_signature}' + web3.to_hex(int(item)).lstrip('0x').rjust(64, '0')
	print(function_signature)
	print(inputData)
	transaction = {
		'to': recipient_address,
		'value': amount_wei,
		'gas': 160000,  # Устанавливаем газовый лимит
		'gasPrice': gas_price,  # Устанавливаем цену газа
		'nonce': web3.eth.get_transaction_count(wallet_address),
		'data': inputData,
		'chainId': 56  # 56 для BSC
	}

	# Подписываем транзакцию
	signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

	# Отправляем транзакцию
	transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
	print(f'Transaction Hash: {transaction_hash.hex()}')
	time.sleep(5)
	print("***")
	print(new_burn)



