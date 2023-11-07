const { ethers } = require("ethers");
require("dotenv").config()  

const network = process.env.ETHEREUM_NETWORK
const infura = process.env.INFURA_API_KEY
const private_key = process.env.SIGNER_PRIVATE_KEY
const mockJsonFile = "./static/MockUSDC.json";
const nftJsonFile = "./static/MusicNFT.json";
const mockAbi=JSON.parse(fs.readFileSync(mockJsonFile));
const nftAbi=JSON.parse(fs.readFileSync(nftJsonFile));

const nft_contract_address = "0x1D33a553541606E98c74a61D1B8d9fff9E0fa138"
const mock_usdc_address = "0xCeD9Fe6C4851acea6833DB0B7A0d2b892E4BBD5f"


// Configuring the connection to an Ethereum node
const provider = new ethers.providers.InfuraProvider(
      network,
      infura);

// Creating a signing account from a private key
const signer = new ethers.Wallet(private_key, provider);

// contracts instancies
const mock_usdc_contract = new ethers.Contract(mock_usdc_address, mockAbi.abi, signer);
const nft_contract = new ethers.Contract(nft_contract_address, nftAbi.abi, signer);

// test getting name of nft contract
getNftName = async () => {
      let result = await nft_contract.name();
      console.log(result);
}

// setting nft price
setNftPrice = async (arg) => {
      let result = await nft_contract.setNFTPrice(arg);
}

var assert = require('assert');

// For this to work you need to wait for few seconds
checkNFTPrice = async (price) => {
      let nft_price = await nft_contract.NFTPriceInUSDC();
      console.log(Number(nft_price));
      assert(Number(nft_price) == price, "Price was not updated!");
}

// sending MockTokens to the customer 
const buyer = "0xB4A5D329e35F83a2e6AB5a74d56f5bD67EaB8d83"
// send 10 MockTokens to user
const amount = BigInt(10e18)

sendTokenToBuyer = async (buyer, amount) => {
      await mock_usdc_contract.transfer(buyer, amount)
}

