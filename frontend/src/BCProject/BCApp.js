import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { API_BASE_LOCAL_URL } from "./config";

function BCApp() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_LOCAL_URL}/wallet/info`)
      .then((response) => response.json())
      .then((json) => setWalletInfo(json));
  }, []);

  const { address, balance } = walletInfo;

  return (
    <div className="App">
      <h1>Blockchain Project</h1>
      <br/>
      <Link to='/blockchain'>Blockchain</Link>
      <Link to='conduct-transaction'>Conduct Transaction</Link>
      <br/>
      <div className="WalletInfo">
        <div>Address: {address}</div>
        <div>Balance: {balance}</div>
      </div>
    </div>
  );
}

export default BCApp;
