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


class Interface(Contracts):
    def __init__(self, musicNFT):
        Contracts.__init__(self, musicNFT)
        self.event_template = self.nft_contract.events.newNFTMinted
        
        
    def handle_event(self, event, event_template):
        print("unutar handle eventa si")
        try:
            result = get_event_data(
                self.codec, event_template._get_event_abi(), event
            )
            print("ovo mora")
            return True, result
        except Exception as e:
            print(e)
            print("bila je greska")
            return False, None

    def event(self):
        self.block_number = self.w3Provider.eth.block_number
        self.events = self.w3Provider.eth.get_logs(
            {
                "fromBlock": self.block_number - 5,
                "toBlock": "latest",
                "address": self.musicNFT_address,
            }
        )

        try:
            for event in self.events:
                suc, result = self.handle_event(
                    event=event, event_template=self.event_template
                )
                if suc:
                    return (True, result)
            return False, False
        except:
            return (False, None)
