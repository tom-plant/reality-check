import React from 'react';
import './gmailClone.css';
import { Header, Sidebar, Mail, EmailList, SendMail } from './gmailinfo';
import {BrowserRouter as Router, Route, Switch, } from 'react-router-dom';

function gmailClone() {

  return (
    <Router>
      {!user ? (
        <Login /> 
      ) : (
        <div className="clone">
          <Header/>
          <div className="clone__body">
              <Sidebar/> 
              <Switch>
                  <Route path="/mail">
                    <Mail/>
                  </Route>
                  <Route path="/">
                    <EmailList/>
                  </Route>
              </Switch>
          </div>
          <SendMail />
        </div>
      )
    }
    </Router>
  );
}

export default gmailClone;
