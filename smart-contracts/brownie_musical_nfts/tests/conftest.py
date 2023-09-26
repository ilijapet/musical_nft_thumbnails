#!/usr/bin/python3

import pytest

from scripts.helpers import get_account

initial_supply = 1000
max_nft = 100

"""
Defining a Shared Initial State for this test. A common pattern in testing is to include one or more module-scoped setup fixtures that define the 
initial test conditions, and then use fn_isolation (next step) to revert to this base state at the start of each test. 
"""


@pytest.fixture(scope="module", autouse=True)
def initial_supply_of_mock_tokens():
    return initial_supply



@pytest.fixture(scope="module", autouse=True)
def smartContract_deploy(MusicNFT, MockUSDC):
    account = get_account()
    mock_token = MockUSDC.deploy(initial_supply, {"from": account[0]})
    musicNFTtoken = MusicNFT.deploy(mock_token, 10, {"from": account[0]})
    return mock_token, musicNFTtoken


"""
In many cases we want to isolate our tests from one another by resetting the local environment. Without isolation, it is possible that the outcome of 
a test will be dependent on actions performed in a previous test. This is done by following function. 
"""


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    # https://eth-brownie.readthedocs.io/en/v1.10.3/tests-pytest-intro.html #isolation-fixtures
    pass


@pytest.fixture(scope="module")
def test_accounts():
    account_1, account_2 = get_account()
    return account_1, account_2
