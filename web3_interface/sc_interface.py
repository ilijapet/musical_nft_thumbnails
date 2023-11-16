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
        self.nft_contract = self.w3Provider.eth.contract(address=self.musicNFT_address, abi=self.musicNFT)



class Interface(Contracts):
    
    def __init__(self, musicNFT):
        Contracts.__init__(self, musicNFT)
        
    
    def handle_event(self, event, event_template):
        try:
            result = get_event_data(self.codec, event_template._get_event_abi(), event)
            return result
        except:
            return False


    def event(self):
        try:
            
            event_template = self.nft_contract.events.newNFTMinted
            block_number = self.w3Provider.eth.block_number
            events = self.w3Provider.eth.get_logs(
                            {"fromBlock": block_number, "toBlock": "latest", "address": self.musicNFT_address}
                        )
            for event in events:
                result = self.handle_event(event=event, event_template=event_template)                
                return result
        except:
            return False

        


        
            

