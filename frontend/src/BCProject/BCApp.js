import React, { useState, useEffect } from 'react'

function BCApp() {
    const [walletInfo, setWalletInfo] = useState({})

    useEffect(() => {
        fetch('http://localhost:5000/wallet/info')
            .then(response => response.json())
            .then(json => setWalletInfo(json))
    }, []);

    const {address, balance} = walletInfo

    return (
        <div className='App'>
            <h1>Blockchain Stimulator</h1>
            <br/>
            <div className="WalletInfo">
                <div>Address: {address}</div>
                <div>Balance: {balance}</div>
            </div>
        </div>
    )
}

export default BCApp;