# !usr/bin/python3

from brownie import MusicNFT, MockUSDC

from scripts.helpers import get_account


def main():
    initial_supply = 1000
    accountOne, accountTwo = get_account()
    print(accountOne,accountTwo)
    mockDeployed = MockUSDC.deploy(initial_supply, {"from": accountOne})
    musciNFTdeployed = MusicNFT.deploy(mockDeployed, 1000, {"from": accountOne})
