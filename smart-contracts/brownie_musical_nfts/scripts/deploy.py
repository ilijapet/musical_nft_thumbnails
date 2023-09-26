# !usr/bin/python3

from brownie import MusicNFT, MockUSDC

from scripts.helpers import get_account


def main():
    accountOne, accountTwo = get_account()
    mockDeployed = MockUSDC.deploy({"from": accountOne})
    musciNFTdeployed = MusicNFT.deploy(mockDeployed, 5, {"from": accountOne})
