from scripts.utils import get_account, encode_function_data, upgrade
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, Boxv2


def main():
    account = get_account()
    print(f"deploy to {network.show_active()}")
    box = Box.deploy({"from":account})
    print(box.retrieve())
    proxy_admin = ProxyAdmin.deploy({"from":account})
    # initializer = Box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from":account})
    print(f"proxy deployed to {proxy} you can now upgrade to V2")
    # typically you would call functions by box.<function>
    # box contract is always the same
    # proxy can change

    # assigning proxy address, the abi from Box. 
    # works because proxy is delegating all calls to box contract.
    # normally this would result in error as the functions are missing in the contract. 
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from":account})
    print(proxy_box.retrieve())
    # now lets upgrade the box contract
    box_v2 = Boxv2.deploy({"from":account})
    upgrade_transaction = upgrade(account, proxy, box_v2.address,  proxy_admin_contract=proxy_admin)
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded")

    proxy_box = Contract.from_abi("Boxv2", proxy.address, Boxv2.abi)
    
    # do not forget that the proxy stores any variable data in its own storage and eventhough implementation is upgraded
    # it keeps its data that has occured prior
    proxy_box.increment({"from":account})
    print(proxy_box.retrieve())