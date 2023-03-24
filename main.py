from web3 import Web3
import json


CELO_NODE_URL = 'https://alfajores-forno.celo-testnet.org'
PRIVATE_KEY = 'your-private-key'

web3 = Web3(Web3.HTTPProvider(CELO_NODE_URL))
web3.eth.default_account = web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address

GOVERNANCE_CONTRACT_ADDRESS = '0x88CdC239B61c5E5e1aCF31ca35AE015FF1a1706f'
GOVERNANCE_ABI_PATH = 'governance_abi.json'


with open(GOVERNANCE_ABI_PATH) as f:
    governance_abi = json.load(f)

governance_contract = web3.eth.contract(
    address=web3.toChecksumAddress(GOVERNANCE_CONTRACT_ADDRESS),
    abi=governance_abi
)

proposal_count = governance_contract.functions.getProposalCount().call()
print(f"Proposal count: {proposal_count}")

# Get the details of a specific proposal (e.g., proposal ID 1)
proposal_id = 1
proposal = governance_contract.functions.getProposal(proposal_id).call()
print(f"Proposal details: {proposal}")


required_deposit = governance_contract.functions.proposalDeposit().call()
print(f"Required deposit: {required_deposit} CELO")

target_address = '0x123...'
function_signature = 'functionName(uint256,address)'
function_args = [arg1, arg2]
deposit_amount = required_deposit

transaction = governance_contract.functions.propose(
    [web3.toChecksumAddress(target_address)],
    [web3.sha3(text=function_signature)],
    [web3.toBytes(function_args)],
    deposit_amount,
    "Description of the proposal"
).buildTransaction({
    'gas': 500000,
    'gasPrice': web3.eth.gasPrice,
    'nonce': web3.eth.getTransactionCount(web3.eth.default_account)
})

signed_transaction = web3.eth.account.signTransaction(transaction, PRIVATE_KEY)
transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

print(f"Submitted proposal with transaction hash: {transaction_hash.hex()}")

proposal_status = governance_contract.functions.getProposalStage(proposal_id).call()
print(f"Proposal status: {proposal_status}")

vote_choice = 1  # 1 for Yes, 2 for No, and 3 for Abstain

transaction = governance_contract.functions.vote(
    proposal_id,
    vote_choice
).buildTransaction({
    'gas': 200000,
    'gasPrice': web3.eth.gasPrice,
    'nonce': web3.eth.getTransactionCount(web3.eth.default_account)
})

signed_transaction = web3.eth.account.signTransaction(transaction, PRIVATE_KEY)
transaction_hash = web3.eth.sendRawTransaction(signed_transaction.rawTransaction)

print(f"Voted with transaction hash: {transaction_hash.hex()}")