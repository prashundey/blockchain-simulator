import React, {useState, useEffect} from 'react'
import { Link } from 'react-router-dom'
import { FormGroup, FormControl, Button } from 'react-bootstrap'
import { API_BASE_LOCAL_URL } from '../config'
import history from '../history'

function CondcutTransaction() {
    const [amount, setAmount] = useState(0)
    const [recipient, setRecipient] = useState('')
    const [addresses, setAddresses] = useState([])

    useEffect(() => {
        fetch(`${API_BASE_LOCAL_URL}/known-addresses`)
            .then(response => response.json())
            .then(json => setAddresses(json))
    }, [])

    const updateRecipient = event => {
        setRecipient(event.target.value)
    }

    const updateAmount = event => {
        setAmount(Number(event.target.value))
    }
    
    const submitTransaction = () => {
        fetch(`${API_BASE_LOCAL_URL}/wallet/transact`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({recipient, amount})
        }).then(response => {
            let json = response.json()
            console.log('submitTransaction', json)
            alert('Success. Directing to Transaction Channel')
            history.push('/transaction-pool')
        })
    }

    return (
        <div className='ConductTransaction'>
            <Link to='/'>Home</Link>
            <br/>
            <h3>Conduct a Transaction</h3>
            <br/>

            <FormGroup>
                <FormControl 
                    input='text'
                    placeholder='recipient'
                    value={recipient}
                    onChange={updateRecipient}
                />
            </FormGroup>
            <FormGroup>
                <FormControl
                    input='text'
                    placeholder='amount'
                    value={amount}
                    onChange={updateAmount}
                />
            </FormGroup>
            <div>
                <Button
                    variant='danger'
                    onClick={submitTransaction}
                >
                    Send
                </Button>
            </div>

            <br/>
            <h4>Addresses on Network</h4>

            <div>
                {
                    addresses.map((address, i) => (
                        <span key={address}>
                            <u> {address} </u> {i !== addresses.length - 1 ? ' | ' : ''} 
                        </span>
                    ))
                }
            </div>
        </div>
    )
}

export default CondcutTransaction