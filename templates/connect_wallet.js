async function connect() {
    const address = await ethereum
      .request({
        method: 'eth_requestAccounts',
        params: [],
      })
      .then((res) => console.log('request accounts', res))
      .catch((e) => console.log('request accounts ERR', e));
      document.getElementById("connect").innerHTML = "Connected";
    }


export {connect};