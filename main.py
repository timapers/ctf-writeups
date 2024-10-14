from blockchain import Blockchain
import requests

# Set up blockchain connection
blockchain = Blockchain("http://ctf.tcp1p.team:44555/02cf2760-7ef4-4fb9-bb12-f501320f8049")

# Initialize address and key
blockchain.set_account(
    "0x411cb5a52DaAd63D2328eBEec3803c1F4b3ac348",
    "0xe9fbeadb03f522d913c9772ec415594907a49fe0b9d9899b2cef0d048a87905b"
)

# Define setup contract
contract = "0x30513990A000e1E5C72ba3F43F4CaCad1EEc6e1e"
print(blockchain.get_code(contract))

# Get other contract
fishy = blockchain.get_storage_at(contract, 0)[-40:]
print(blockchain.get_code(fishy))

# Iterate through blocks
for block in range(9):
    block = hex(block)
    sentence_1 = blockchain.get_storage_at(fishy, 0, block)
    sentence_2 = blockchain.call("0x729acff4", fishy, block)

    # hex to char
    sentence_1 = bytes.fromhex(sentence_1[2:]).decode('utf-8')
    sentence_2 = bytes.fromhex(sentence_2[2:]).decode('utf-8')
    print(sentence_1, sentence_2)