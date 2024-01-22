from web3 import Web3
import csv
import requests

# Адрес ноды
bsc_rpc_endpoint = "https://opbnb-mainnet-rpc.bnbchain.org"
web3 = Web3(Web3.HTTPProvider(bsc_rpc_endpoint))

# Указываем сумму транзакции
amount_bnb = 0.0001
# Переводим ее в нужный формат
amount_wei = Web3.to_wei(amount_bnb, 'ether')

# Адрес получателя
recipient_address = web3.to_checksum_address("0x3c76649cbae809e18bb577a9e291935f81a00195")

csv_file_path = 'pk.txt'

with open(csv_file_path, 'r') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=';')

	for row in csv_reader:
		# Получаем адрес кошелька
		wallet_address = web3.eth.account.from_key(row[0]).address
		
		# Создание транзакции
		transaction = {
			'to': recipient_address,
			'value': amount_wei,
			'gas': 80000,  # Устанавливаем газовый лимит
			'gasPrice': web3.eth.gas_price,  # Устанавливаем цену газа
			'nonce': web3.eth.get_transaction_count(wallet_address),
			'data': '0x2ae3594a',
			'chainId': 204  # 56 для BSC
		}

		# Подписываем транзакцию
		signed_transaction = web3.eth.account.sign_transaction(transaction, row[0])

		# Отправляем транзакцию
		transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
		# Выводим на экран результат
		print(f'Account {wallet_address} Transaction: {transaction_hash.hex()}')
print('Task completed')