import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import {BrowserRouter as Router} from "react-router-dom"
import Navbar from './components/Navbar.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <Router>
      <div className="flex flex-col items-center min-w-screen min-h-screen bg-slate-800 text-white font-bold">
        <Navbar/>
        <App />
      </div>
    </Router>
  </StrictMode>,
)
