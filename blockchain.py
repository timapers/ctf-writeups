from web3 import Web3
import requests


class Blockchain:
    """
    Blockchain interface as defined by the json rpc api for the ethereum network
    https://ethereum.org/en/developers/docs/apis/json-rpc/
    """

    def __init__(self, url):
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.addr = None
        self.key = None
        self.session = requests.session()

    def _post(self, method, params):
        res = self.session.post(
            self.url,
            json={
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 0
            }
        ).json()
        if "result" in res:
            return res["result"]
        return res["error"]

    def set_account(self, addr, key):
        self.addr, self.key = addr, key

    def get_tx_count(self, addr=None):
        addr = addr if addr else self.addr
        return self._post("eth_getTransactionCount", [addr, "latest"])

    def sign_tx(self, data, to):
        return self.web3.eth.account.sign_transaction({
            "data": data,
            "from": self.addr,
            "to": Web3.to_checksum_address(to) if to else None,
            "gas": "0xfffff",
            "value": "0x0",
            "gasPrice": "0x0",
            "nonce": self.get_tx_count()
        }, self.key)

    def get_tx_receipt(self, tx_hash):
        return self._post("eth_getTransactionReceipt", [tx_hash])

    def call(self, data, to, block="latest"):
        return self._post("eth_call", [{
            "data": data,
            "from": self.addr,
            "to": Web3.to_checksum_address(to),
            "nonce": self.get_tx_count()
        }, block])

    def get_balance(self, addr):
        return self._post("eth_getBalance", [addr, "latest"])

    def send_tx(self, data, to):
        signed_tx = self.sign_tx(data, to)
        signed_tx = signed_tx.raw_transaction.hex()
        return self._post("eth_sendRawTransaction", [signed_tx])

    def get_block_by_number(self, block_number, full=True):
        block_number = block_number if isinstance(block_number, str) else hex(block_number)
        return self._post("eth_getBlockByNumber", [block_number, full])

    def get_signature(self, string):
        return self.web3.keccak(text=string).hex()[:8]

    def get_storage_at(self, addr, index, block="latest"):
        index = index if isinstance(index, str) else hex(index)
        return self._post("eth_getStorageAt", [addr, index, block])

    def get_code(self, addr):
        return self._post("eth_getCode", [addr, "latest"])

    def create_account(self):
        account = self.web3.eth.account.create("password")
        self.addr, self.key = account.address, account.key.hex()
        return self.addr, self.key
