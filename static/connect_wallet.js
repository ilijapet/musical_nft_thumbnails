connect = async () => {
    const address = await ethereum
      .request({
        method: 'eth_requestAccounts',
        params: [],
      })
      .then((res) => console.log('request accounts', res))
      .catch((e) => console.log('request accounts ERR', e));
      document.getElementById("connect").innerHTML = "Connected";
    }     
    
    
    checkMetaMaskState = async () => {
      // alert("pocetka")
      let account = await window.ethereum.selectedAddress
      const liElement = document.createElement("li");
      liElement.setAttribute("class", "nav-item")
      const aElement = document.createElement("a");
      aElement.setAttribute("class", "nav-link p-3")
      aElement.setAttribute("href", "javascript:connect()")
      aElement.setAttribute("id", "connect")

      if (account.includes("0x")) {
        alert("proba")
        liElement.innerHTML = "Connected"
        liElement.appendChild(aElement);
        document.getElementById("logout").appendChild(liElement);
      } else {
        liElement.appendChild(aElement);
        document.getElementById("logout").appendChild(liElement);
        liElement.innerHTML = "Connect to MetaMask"
      }

    }
