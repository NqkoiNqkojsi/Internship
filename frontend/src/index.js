import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.css';
import './index.css';
import { BrowserRouter, Routes, Route, } from "react-router-dom";
import App from './App';
import Article from './Article'
import EntityOverv from './EntityOverv'
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="" element={<App />} />
      <Route path="article" element={<Article />} >
        <Route path=":artID" element={<Article />} />
      </Route>
      <Route path="entity" element={<EntityOverv/>} >
        <Route path=":entID" element={<EntityOverv/>} />
      </Route>
      <Route
        path="*"
        element={
          <main style={{ padding: "1rem" }}>
            <p>There's nothing here!</p>
          </main>
        }
      />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
