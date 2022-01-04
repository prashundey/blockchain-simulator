import React, {useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Transaction from './Transaction'
import { API_BASE_LOCAL_URL } from '../config'
import { SECONDS_JS } from '../config'
import { Button } from 'react-bootstrap'
import history from '../history'

const SHORT_PULLING_INTERVAL = 10 * SECONDS_JS

function TransactionPool() {
    const [transactions, setTransactions] = useState([])

    const fetchTransactions = () => {
        fetch(`${API_BASE_LOCAL_URL}/transactions`)
            .then(response => response.json())
            .then(json => {
                console.log('transaction-chanel update:', json)
                setTransactions(json)
            })
    }

    useEffect(() => {
        fetchTransactions()
        const intervalID = setInterval(fetchTransactions, SHORT_PULLING_INTERVAL)
        return () => clearInterval(intervalID)
    }, [])

    const fetchMineBlock = () => {
        if (transactions.length === 0) {
            alert('No transactions to mine')
            history.push('/conduct-transaction')
            return
        }
        
        fetch(`${API_BASE_LOCAL_URL}/blockchain/mine`)
            .then(() => {
                alert('Succesfully Mined New Block')
                history.push('/blockchain')
            })
    }

    return (
        <div className='TransactionPool'>
             <Link to='/'>Home</Link>
             <h3>Transaction Pool Channel</h3>
             <div>
                {
                    transactions.map(transaction => (
                        <div key={transaction.id}> 
                            <hr/>
                            <Transaction transaction={transaction}/>
                        </div>
                    ))
                
                }
             </div>

             <br/>
             <hr/>
             <Button
                variant='danger'
                onClick={fetchMineBlock}
             >
                Mine Transactions
            </Button>
        </div>
    )
}

export default TransactionPool
