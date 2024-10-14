from blockchain import Blockchain

# Set up blockchain connection
blockchain = Blockchain("http://45.32.119.201:44555/6df9f3e7-fa4f-48d8-9983-d116df6c1d91")

# Initialize address and key
blockchain.set_account(
    "0x39dD6F988CFEe5FE0431de5236B64f693d63a549",
    "0xf55787264cfe5b9863bcbc34409dde5fa95f481eb5d5c3ad7ce1dd578d4589c6"
)

# Define setup contract and get byte code
contract = "0x655C116773Cb923a32F48aB7B37733Ce2186D449"
print(blockchain.get_code(contract))

# Get other contract
fishy = blockchain.get_storage_at(contract, 0)[-40:]
print(fishy)
print(blockchain.get_code(fishy))

# Iterate through blocks
for nr in range(2, 9):
    block = blockchain.get_block_by_number(nr, True)
    print(block)

    # Extract input from the transactions
    sentence_1 = block["transactions"][0]["input"][100:]
    sentence_1 = bytes.fromhex(sentence_1).decode('utf-8')
    print(sentence_1)
