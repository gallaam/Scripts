from base64 import b64encode, b64decode
import httpx
import time

TESTNET = False
TONCENTER_API_KEY = {
    True: 'e3bd9f0a1dfa8274126c5f45e9596c3f8445665013fb46ee551b1ac5027a020b',
    False: 'a1b8896456723973ad86cbe45d21a5e88427565be3b2f8b6ec6fb0072199e8ac'
}[TESTNET]
TONCENTER_ENDPOINT = f"https://{'testnet.' if TESTNET else ''}toncenter.com/api/v2/"


def send_boc(src: bytes):
    res = httpx.post(
        TONCENTER_ENDPOINT + 'sendBoc',
        headers={
            'X-API-Key': TONCENTER_API_KEY,
        },
        json={
            'boc': b64encode(src).decode(),
        }
    ).json()
    print(res)
    return res


def get_account(addr: str):
    try:
        res = httpx.get(
            TONCENTER_ENDPOINT + 'getAddressInformation',
            headers={
                'X-API-Key': TONCENTER_API_KEY,
            },
            params={
                'address': addr
            }
        ).json()
        return res.get('result', {})
    except Exception as e:
        print(f"Error: {e}")
        return {}


def get_seqno(addr: str):
    try:
        res = httpx.get(
            TONCENTER_ENDPOINT + 'getWalletInformation',
            headers={
                'X-API-Key': TONCENTER_API_KEY,
            },
            params={
                'address': addr
            }
        ).json()
        if res['result']['account_state'] == 'uninitialized':
            return 0
        return res['result'].get('seqno', 0)
    except Exception as e:
        print(f"Error: {e}")
        return 0


def run_get_method(addr, method, stack=[]):
    try:
        return httpx.post(
            TONCENTER_ENDPOINT + 'runGetMethod',
            headers={
                'X-API-Key': TONCENTER_API_KEY,
            },
            json={
                'address': addr,
                'method': method,
                'stack': stack,
            }
        ).json()['result']
    except Exception as e:
        print(f"Error: {e}")
        return run_get_method(addr, method, stack)


def fetch_items_by_collection(addr: str, offset: int = 0, limit: int = 100):
    count_items = int(run_get_method(
        addr, 'get_collection_data'
    )['stack'][0][1], 16)
    items = []
    for i in range(0 or offset, count_items, limit):
        res = httpx.get(
            f"https://{'testnet.' if TESTNET else ''}tonapi.io/v1/nft/searchItems",
            params={
                'collection': addr,
                'limit': limit,
                'include_on_sale': 'false',
                'offset': i,
            }
        ).json()
        if not res['nft_items']:
            break

        for item in res['nft_items']:
            items.append(item['address'])

        time.sleep(2)
        break

    print(f"Fetched {len(items)} items")
    return count_items, items
