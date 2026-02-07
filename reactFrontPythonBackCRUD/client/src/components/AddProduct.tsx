import { useState, type ChangeEvent, type FormEvent, useEffect } from 'react'
import axios from 'axios'
import type { PRODUCT } from '../Types'


export default function AddProduct() {

    const [product, setProduct] = useState<PRODUCT>({
        name: "",
        price: 0,
        category: "",
        image: null,
        quantity: 0
    })
    const [loading, setLoading] = useState(false)

    const [preview, setPreview] = useState<string | null>(null)

    // ✅ Generate preview when image changes
    useEffect(() => {
        if (!product.image) {
            setPreview(null)
            return
        }

        const objectUrl = URL.createObjectURL(product.image)
        setPreview(objectUrl)

        return () => URL.revokeObjectURL(objectUrl)

    }, [product.image])


    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {

        const { name, value, files, type } = event.target

        // ✅ Handle file input
        if (files) {
            setProduct(prev => ({
                ...prev,
                [name]: files[0]
            }))
            return
        }

        // ✅ Handle number inputs
        if (type === "number") {
            setProduct(prev => ({
                ...prev,
                [name]: Number(value)
            }))
            return
        }

        // ✅ Handle text inputs
        setProduct(prev => ({
            ...prev,
            [name]: value
        }))
    }


  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)

    const RECEIVER_URL = "http://127.0.0.1:5000/products";

    const formData = new FormData()

    formData.append("name", product.name)
    formData.append("price", product.price.toString())
    formData.append("category", product.category)
    formData.append("quantity", product.quantity.toString())

    if (product.image) {
        formData.append("image", product.image)
    }

    try {
        const response = await axios.post(RECEIVER_URL, formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        })

        console.log("successfully added", response.data)
        setLoading(false)

    } catch (error) {
        console.log(error)
        setLoading(false)
    }
}



    return (
        <div>
            <form onSubmit={handleSubmit} className='flex flex-col justify-center items-center space-y-2'>

                <h1>ADD YOUR PRODUCT</h1>

                <div className='flex gap-2 items-center'>
                    <label htmlFor='name'>Product Name: </label>
                    <input className='p-2 rounded-lg border border-slate-900'
                        type='text'
                        name='name'
                        placeholder='Product Name'
                        value={product.name}
                        onChange={handleChange}
                        id='name'
                    />
                </div>


                <div className='flex gap-2 items-center'>
                    <label htmlFor='price'>Product Price: </label>
                    <input className='p-2 rounded-lg border border-slate-900'
                        type='number'
                        name='price'
                        placeholder='Product Price'
                        value={product.price}
                        onChange={handleChange}
                        id='price'
                    />
                </div>


                <div className='flex gap-2 items-center'>
                    <label htmlFor='category'>Product Category: </label>
                    <input className='p-2 rounded-lg border border-slate-900'
                        type='text'
                        name='category'
                        placeholder='Product Category'
                        value={product.category}
                        onChange={handleChange}
                        id='category'
                    />
                </div>


                {/* IMAGE SECTION */}
                <div className='flex flex-col gap-2'>

                    <div className='flex gap-2 items-center'>
                        <label htmlFor='image'>Product Image: </label>
                        <input className='p-2 rounded-lg border border-slate-900'
                            type='file'
                            name='image'
                            accept='image/*'
                            onChange={handleChange}
                            id='image'
                        />
                    </div>


                    <div className='flex flex-col justify-center items-center'>
                        <p className='opacity-50'>Image Preview</p>

                        <div className='h-32 w-32 rounded-lg border border-slate-950 bg-slate-700 overflow-hidden'>

                            {preview && (
                                <img
                                    src={preview}
                                    alt='Preview'
                                    className='w-full h-full object-cover'
                                />
                            )}

                        </div>
                    </div>

                </div>


                <div className='flex gap-2 items-center'>
                    <label htmlFor='quantity'>Product Quantity: </label>
                    <input className='p-2 rounded-lg border border-slate-900'
                        type='number'
                        name='quantity'
                        placeholder='How Many of it ?'
                        value={product.quantity}
                        onChange={handleChange}
                        id='quantity'
                    />
                </div>


                <button
                    disabled = {loading}
                    type='submit'
                    className='px-3 py-2 rounded-lg cursor-pointer opacity-85 hover:opacity-100 hover:scale-110 w-[50%] font-bold'
                >
                    {loading ? "Submitting ...": "Add Product"}
                </button>

            </form>
        </div>
    )
}
