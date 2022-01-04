import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {Router, Switch, Route} from 'react-router-dom'
import {createBrowserHistory} from 'history'
import BCApp from './BCProject/BCApp';
import Blockchain from './BCProject/Components/Blockchain'
import ConductTransaction from './BCProject/Components/ConductTransaction'
import TransactionPool from './BCProject/Components/TransactionPool'

ReactDOM.render(
  <Router history={createBrowserHistory()}>
    <Switch>
      <Route path='/' exact component={BCApp}/>
      <Route path='/blockchain' component={Blockchain}/>
      <Route path='/conduct-transaction' component={ConductTransaction}/>
      <Route path='/transaction-pool' component={TransactionPool}/>
    </Switch>

  </Router>,
  document.getElementById('root')
);

