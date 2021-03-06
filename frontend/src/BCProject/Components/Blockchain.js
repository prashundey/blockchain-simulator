import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "react-bootstrap";
import { API_BASE_LOCAL_URL } from "../config";
import Block from "./Block";

const PAGE_RANGE = 3


function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [chainLength, setChainLength] = useState(0)

    const fetchBlockchainPage = ({start, end}) => {
        fetch(`${API_BASE_LOCAL_URL}/blockchain/range?start=${start}&end=${end}`)
            .then(response => response.json())
            .then(json => setBlockchain(json))
    }

    useEffect(() => {
        fetchBlockchainPage({start: 0, end: PAGE_RANGE})

        fetch(`${API_BASE_LOCAL_URL}/blockchain/length`)
            .then(response => response.json())
            .then(length => setChainLength(length))
    }, [])

    const buttonNumbers = []
    for (let i = 0; i < Math.ceil(chainLength / PAGE_RANGE); i++) {
        buttonNumbers.push(i)
    }

    return (
        <div className="Blockchain">
            <Link to='/'>Home</Link>
            <br/>
            <h3>Blockchain</h3>
            <div>
                {blockchain.map(block => (
                    <Block key={block.hash} block={block}/>
                ))}
            </div>
            
            <div>
                {buttonNumbers.map(num => {
                    const start = num * PAGE_RANGE
                    const end = (num + 1) * PAGE_RANGE
                    return (
                        <span key={num} onClick={() => fetchBlockchainPage({start, end})}>
                            <Button size="sm" variant="danger">{num+1}</Button>{' '}
                        </span>
                    )
                })}
            </div>

        </div>
    );
}

export default Blockchain;
