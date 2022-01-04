import React, {useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Transaction from './Transaction'
import { API_BASE_LOCAL_URL } from '../config'

function TransactionPool() {
    const [transactions, setTransactions] = useState([])

    useEffect(() => {
        fetch(`${API_BASE_LOCAL_URL}/transactions`)
            .then(response => response.json())
            .then(json => setTransactions(json))
    }, [])

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
        </div>
    )
}

export default TransactionPool
