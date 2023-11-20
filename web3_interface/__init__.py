from .sc_interface import Interface
import os
import json

abidir = os.path.dirname(os.path.abspath(__file__))


def load_abi(name):
    # filename = os.path.join(abidir, f"web3_interface/{name}.json")
    filename = os.path.join(abidir, f"{name}.json")
    return json.load(open(filename))


# mockUSDC = load_abi("MockUSDC")
musicNFT = load_abi("MusicNFT")

contract_interface = Interface(musicNFT["abi"])
