import React, { useState, useEffect } from 'react'
import { API_BASE_LOCAL_URL } from './config'
import Blockchain from './Components/Blockchain';

function BCApp() {
    const [walletInfo, setWalletInfo] = useState({})

    useEffect(() => {
        fetch(`${API_BASE_LOCAL_URL}/wallet/info`)
            .then(response => response.json())
            .then(json => setWalletInfo(json))
    }, []);

    const {address, balance} = walletInfo

    return (
      <div className="App">
        <h1>Blockchain Stimulator Project</h1>
        <br />
        <div className="WalletInfo">
          <div>Address: {address}</div>
          <div>Balance: {balance}</div>
        </div>
        <br/>
        <Blockchain/>
      </div>
    );
}

export default BCApp;