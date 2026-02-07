import {Routes, Route} from "react-router-dom"
import Homepage from "./components/Homepage"
import Login from "./components/Login"
import ViewProducts from "./components/ViewProducts"
import AddProduct from "./components/AddProduct"
export default function App(){
  return (
    <Routes>
      <Route path= "/" element = {<Homepage/>} />
      <Route path= "/login" element = {<Login/>} />
      <Route path= "/products" element = {<AddProduct/>} />
      <Route path= "/shop" element = {<ViewProducts/>} />

    </Routes>
  )
}