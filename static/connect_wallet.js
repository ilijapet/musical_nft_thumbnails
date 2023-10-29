
connect = async () => {
  const address = await ethereum
  .request({
      method: 'eth_requestAccounts',
      params: [],
  })
  .then((res) => console.log('request accounts', res))
  .catch((e) => console.log('request accounts ERR', e));
  document_test = document.getElementById("connect");
  document_test.innerHTML = "Connected"  
}   

checkMetaMaskState = async () => {
  const account = await window.ethereum.request({method: 'eth_accounts'})
  const liElement = document.createElement("li");
  liElement.setAttribute("class", "nav-item")
  const aElement = document.createElement("a");
  aElement.setAttribute("class", "nav-link p-3")
  if (typeof account[0] == "undefined") {
      aElement.setAttribute("href", "javascript:connect()")
      aElement.setAttribute("id", "link")
      liElement.setAttribute("id", "connect")
      liElement.innerHTML = "Connect to MetaMask"
      aElement.appendChild(liElement);
      document.getElementById("logout").appendChild(aElement);
  } else if (account[0].includes("0x")) {
      aElement.setAttribute("id", "link")
      liElement.setAttribute("id", "connect")
      liElement.innerHTML = "Connected"
      aElement.appendChild(liElement);
      document.getElementById("logout").appendChild(aElement);
  } else {
      console.log("There is some problem with MetaMask")        
  }
}


window.ethereum.on('accountsChanged', async () => {
  let ilElement = document.getElementById("connect")
  const account = await window.ethereum.request({method: 'eth_accounts'})
  if (typeof account[0] == "undefined") {
      ilElement.innerHTML = "Connect to MetaMask"
  } else if (account[0].includes("0x")) {
      ilElement.innerHTML = "Connected"
  }
});
