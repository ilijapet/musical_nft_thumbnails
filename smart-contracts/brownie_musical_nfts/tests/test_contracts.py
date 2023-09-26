#!/usr/bin/python3


# Test if deployment whent well and if address pf deployed contracts starts with 0x
def test_initial_supplay_account_alice(smartContract_deploy):
    mock_token, musicNFTtoken = smartContract_deploy
    assert mock_token.address.startswith("0x") 
    assert musicNFTtoken.address.startswith("0x") 


# Test if right ammount of MockTokens are minted to deployer/owner address
def test_mock_token(initial_supply_of_mock_tokens, smartContract_deploy, test_accounts):
    mock_token, musicNFTtoken =  smartContract_deploy
    deployer_account, user_account = test_accounts
    initial_supply = initial_supply_of_mock_tokens
    mock_token_balance = mock_token.balanceOf(deployer_account)
    assert mock_token_balance == 1000_000_000_000_000_000_000 


# Test approve & allowance functionality. Reason for this is fact that when we have crypto buyers for NFTs we will need to transfer from our user to our smart contract certain 
# amount of USDC tokens. And because we will call USDC contract from our MusicNFT contract we will need to have rights to spend user USDC by transfering from his account to 
# our account. 
def test_mock_token_approve_allow(smartContract_deploy, test_accounts):
    accountOne, accountTwo = test_accounts
    mock_token, musicNFTtoken =  smartContract_deploy
    mock_token.approve(musicNFTtoken.address, 1000)
    result = mock_token.allowance(accountOne, musicNFTtoken.address)
    assert result == 1000


# And now finally let's test our NFT contract. And here in this test we will check whole buy with crypto flow. And this includes: buyer approve our NFT contract to spend USDC 
# for NFT in this name. 
def test_NFT_buy_with_crypto(smartContract_deploy, test_accounts):
    mock_token, musicNFTtoken =  smartContract_deploy
    deployer_account, user_account = test_accounts
    mock_token.approve(musicNFTtoken.address, 1000)
    result = mock_token.allowance(deployer_account, musicNFTtoken.address)
    assert result == 1000
    mock_token.transfer(musicNFTtoken.address, 1000)
    mock_token_balance = mock_token.balanceOf(musicNFTtoken.address)
    assert mock_token_balance == 1000

