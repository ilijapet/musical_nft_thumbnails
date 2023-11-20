import os
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3._utils.events import get_event_data
from eth_abi.codec import ABICodec
from dotenv import load_dotenv


load_dotenv()


class Contracts:
    def __init__(self, musicNFT):
        self.musicNFT = musicNFT
        self.musicNFT_address = os.environ.get("MUSIC_NFT_ADDRESS")
        self.private_key = os.environ.get("SIGNER_PRIVATE_KEY")
        self.w3Provider = Web3(Web3.HTTPProvider(os.environ.get("INFURA_PROVIDER")))
        self.codec: ABICodec = self.w3Provider.codec
        self.w3Provider.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.nft_contract = self.w3Provider.eth.contract(
            address=self.musicNFT_address, abi=self.musicNFT
        )
        self.owner = os.environ.get("OWNER")    


class Interface(Contracts):
    def __init__(self, musicNFT):
        Contracts.__init__(self, musicNFT)
        self.event_template = self.nft_contract.events.newNFTMinted
        
        
    def handle_event(self, event, event_template):
        try:
            result = get_event_data(
                self.codec, event_template._get_event_abi(), event
            )
            return True, result
        except Exception as e:
            print(e)
            return False, None

    def event(self):
        block_number = self.w3Provider.eth.block_number
        events = self.w3Provider.eth.get_logs(
            {
                "fromBlock": block_number - 5,
                "toBlock": "latest",
                "address": self.musicNFT_address,
            }
        )

        try:
            for event in events:
                suc, result = self.handle_event(
                    event=event, event_template=self.event_template
                )
                if suc:
                    return (True, result)
            return False, False
        except:
            return (False, None)


    def mint_nft(self, tokenURI):
        nonce = self.w3Provider.eth.get_transaction_count(
            Web3.to_checksum_address(self.owner)
        )
        print(nonce, "nonce")
        txn_dict = self.nft_contract.functions.createNFT(self.owner, tokenURI).build_transaction(
            {

                "from": self.owner, 
                "chainId": 80001,
                "nonce": nonce,
            }
        )
        print("txn_dict")
        signed_txn = self.w3Provider.eth.account.sign_transaction(
            txn_dict, private_key=self.private_key
        )
        print("signed_txn")
        txn_hash = self.w3Provider.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = self.w3Provider.eth.wait_for_transaction_receipt(txn_hash)
        print(txn_dict)
        # return txn_receipt