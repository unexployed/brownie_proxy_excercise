from brownie import accounts, network, config, Contract
from web3 import Web3
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
TESTNET =["goerli"]
OPENSEA_URL = "https://testnets.opensea.io/assets/goerli/{}/{}"

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in TESTNET:
        return accounts.load("goerli_dev_1")
    if network.show_active() in FORKED_LOCAL_ENVIRONMENTS or LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]


# initializer =  <smartcontract.function>, 1, 2, 3, 4, 5 <can be multiple arguements>
# encoding needed to let our smart contract know what to call and with what params. 
# in case it is blank, empty hexstring is returned
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)

def upgrade(account, proxy, new_implementation_address, proxy_admin_contract=None, initializer=None, *args):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(proxy.address, new_implementation_address, encoded_function_call, {"from":account})
        else:
            transaction = proxy_admin_contract.upgrade(proxy.address, new_implementation_address, {"from":account})
    # admin is wallet
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(new_implementation_address, encoded_function_call, {"from":account})
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from":account})

    return transaction



