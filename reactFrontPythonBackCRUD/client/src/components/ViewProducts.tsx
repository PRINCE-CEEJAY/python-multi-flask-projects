import React, {useState, useEffect } from 'react'
import axios from 'axios'
import type { PRODUCT } from '../Types'
import { Plus } from 'lucide-react'
export default function ViewProducts() {
  const [products, setProducts] = useState<PRODUCT[]>([])

  useEffect(()=> {
    const RECEIVER_URL = "http://127.0.0.1:5000/products";
    async function fetchProducts () {
      const response = await axios.get(RECEIVER_URL);
      setProducts(response.data.data);
    }
    fetchProducts()
  }, [])


  return (
    <div className='grid grid-cols-3 h-full p-2 w-full'>
      {products.map(item =>(
          <div className='flex flex-col justify-center items-center m-1 p-2 rounded-md border border-slate-950 cursor-pointer hover:scale-102 transition-all duration-300 ease' key={item.id} >
            <img src={`${item.image}`} width={100} height={100} className='rounded-lg hover:animate-pulse' />
            <h2 className='font-bold text-black'>{item.name}</h2>

            <div className='grid grid-cols-2'>             
              <div className='flex gap-2'> 
                <label>Price: </label>
                <h4 className='text-gray-400'>{item.price}</h4>
              </div>

              <div className='flex gap-2'> 
                <label>Category: </label>
                <h4 className='text-gray-400'>{item.category}</h4>
              </div>

              <div className='flex gap-2'> 
                <label>Quantity: </label>
                <h4 className='text-gray-400'>{item.quantity}</h4>
              </div>

              <div className='flex items-center bg-green-800 rounded-md cursor-pointer opacity-85 hover:opacity-100 py-0.5'> 
                <Plus/>
                <p>Add to Cart</p>
              </div>
            </div>
          </div>
        ))}
    </div>
  )
}
