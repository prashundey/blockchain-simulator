import React, {useState} from 'react'
import { FormGroup, FormControl, Button } from 'react-bootstrap'
import { API_BASE_LOCAL_URL } from '../config'

function CondcutTransaction() {
    const [amount, setAmount] = useState(0)
    const [recipient, setRecipient] = useState('')

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
            alert('Success')
        })
    }

    return (
        <div className='ConductTransaction'>
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
        </div>
    )
}

export default CondcutTransaction