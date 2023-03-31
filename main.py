import json
from web3 import Web3
from web3.middleware import geth_poa_middleware


CELO_NODE_URL = 'https://alfajores-forno.celo-testnet.org'
PRIVATE_KEY='4b5142ac2fda7684ff95b19266ce0b7ac27397ace6cb29bd1a03aa3cf2f0b933'
GOVERNANCE_CONTRACT_ADDRESS = '0x88CdC239B61c5E5e1aCF31ca35AE015FF1a1706f'

GOVERNANCE_ABI_PATH = 'governance_abi.json'


with open(GOVERNANCE_ABI_PATH) as f:
    governance_abi = json.load(f)


w3 = Web3(Web3.HTTPProvider(CELO_NODE_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if connected to Celo network
if not w3.is_connected():
    print("Not connected to the Celo network.")
    exit(1)

# Set up the account and contract instances
account = w3.eth.account.from_key(PRIVATE_KEY)
governance_contract = w3.eth.contract(
    address=Web3.to_checksum_address(GOVERNANCE_CONTRACT_ADDRESS),
    abi=governance_abi
)




# Get the details of a specific proposal (e.g., proposal ID 1)
proposal_id = 123456
proposal = governance_contract.functions.getProposal(proposal_id).call()
print(f"Proposal details: {proposal}")

# get proposal stage
proposal_id = 123456
stage = governance_contract.functions.getProposalStage(proposal_id).call()

# print proposal stage
print(f"Proposal stage: {stage}")



# vote on proposal
index = 0
vote_value = 1  # vote in favor of the proposal
tx = governance_contract.functions.vote(proposal_id, index, vote_value).build_transaction({
    'from': account.address,
    'gas': 1000000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'nonce': w3.eth.get_transaction_count(account.address)
})

# sign and send transaction
signed_tx = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# print transaction hash
print(f"Transaction hash: {tx_hash.hex()}")



# set up proposal parameters
values = [100, 200, 300]
destinations = ['0x8BdDeC1b7841bF9eb680bE911bd22051f6a00815', '0xcdd1151b2bC256103FA2565475e686346CeFd813', '0xCD1117Ca9f96F9837a28C473B35C2b49EEd72973']
data = '0xabcdef123456'
data_lengths = [32, 64, 16]
description_url = 'https://my-proposal.com'

deposit_amount = 10000000

# Get the current nonce for the account
nonce = w3.eth.get_transaction_count(account.address)

# Increment the nonce by one to ensure it is higher than the previous nonce
nonce += 1

# create proposal transaction
tx = governance_contract.functions.propose(
    values,
    destinations,
    data,
    data_lengths,
    description_url
).build_transaction({
    'from': account.address,
    'value': deposit_amount,
    'gas': 1000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce
})

# sign and send proposal transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# print transaction hash for the proposal
print(f"Proposal submitted. Transaction hash: {tx_hash.hex()}")





# Get the number of proposals
proposal_count = governance_contract.functions.proposalCount().call()

print(f'There are currently {proposal_count} proposals.')