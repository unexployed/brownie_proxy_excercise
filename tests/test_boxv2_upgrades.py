from scripts.utils import get_account, encode_function_data, upgrade
from brownie import Boxv2, ProxyAdmin, TransparentUpgradeableProxy, Box, exceptions, Contract, accounts
import pytest

def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from":account})
    proxy_admin = ProxyAdmin.deploy({"from":account})
    box_encoded_initializer = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer, {"from":account, "gas_limit":1000000})

    #deploy boxv2 and upgrade
    box_v2 = Boxv2.deploy({"from":account})
    proxy_box = Contract.from_abi("Boxv2", proxy.address, Boxv2.abi)
    # this test passes if an error is thrown
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from":account})
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from":account})
    assert proxy_box.retrieve() == 1
    

