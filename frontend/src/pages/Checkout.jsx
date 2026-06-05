import React, { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const Checkout = () => {
    const { cart, cartTotal, clearCart } = useCart();
    const navigate = useNavigate();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isConfirmed, setIsConfirmed] = useState(false);

    const taxRate = 0.05;
    const taxAmount = cartTotal * taxRate;
    const finalTotal = cartTotal + taxAmount;

    const [formData, setFormData] = useState({
        name: '',
        address: '',
        phone: '',
        paymentMethod: 'credit_card'
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handlePlaceOrder = (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        // Simulating API call
        setTimeout(() => {
            setIsSubmitting(false);
            setIsConfirmed(true);
            clearCart();
        }, 1500);
    };

    if (isConfirmed) {
        return (
            <div className="min-h-screen bg-[#f4f4f4] py-24 px-8 md:px-16 flex flex-col items-center justify-center text-black selection:bg-black selection:text-white">
                <div className="max-w-2xl w-full bg-white border-4 border-black p-12 text-center shadow-[12px_12px_0px_0px_rgba(237,120,68,1)]">
                    <div className="w-24 h-24 bg-[#ed7844] rounded-full mx-auto mb-8 flex items-center justify-center border-4 border-black">
                        <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path>
                        </svg>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-extrabold uppercase tracking-tight text-black mb-6">
                        Order Confirmed
                    </h1>
                    <p className="text-xl font-bold text-gray-500 mb-10">
                        Thank you for your purchase. Your order is being processed.
                    </p>
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="inline-block bg-[#ed7844] border-2 border-black px-8 py-4 text-sm font-extrabold uppercase tracking-widest text-black hover:text-white hover:bg-black transition-all duration-200"
                    >
                        Back to Dashboard
                    </button>
                </div>
            </div>
        );
    }

    // Redirect to cart if empty
    if (cart.length === 0 && !isConfirmed) {
        return (
            <div className="min-h-screen bg-[#f4f4f4] py-24 px-8 md:px-16 flex flex-col items-center justify-center text-black">
                <h1 className="text-3xl font-extrabold uppercase tracking-tight text-black mb-6">Your Cart is Empty</h1>
                <button
                    onClick={() => navigate('/products')}
                    className="inline-block bg-[#ed7844] border-2 border-black px-8 py-4 text-sm font-extrabold uppercase tracking-widest text-black hover:text-white hover:bg-black transition-all duration-200"
                >
                    Return to Products
                </button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-[#f4f4f4] py-24 px-8 md:px-16 text-black selection:bg-black selection:text-white">
            <div className="max-w-6xl mx-auto mt-16">

                <h1 className="text-4xl md:text-5xl font-extrabold uppercase tracking-tight text-black mb-12 border-b-4 border-black pb-4">
                    Checkout
                </h1>

                <div className="flex flex-col lg:flex-row gap-12">
                    {/* User Details Form */}
                    <div className="w-full lg:w-2/3">
                        <div className="bg-white border-4 border-black p-8 md:p-12 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
                            <h2 className="text-3xl font-extrabold uppercase tracking-tight mb-8">Shipping Information</h2>

                            <form onSubmit={handlePlaceOrder} className="space-y-6">
                                <div>
                                    <label className="block text-sm font-bold leading-6 text-black mb-2 uppercase tracking-wide">
                                        Full Name
                                    </label>
                                    <input
                                        name="name"
                                        type="text"
                                        required
                                        value={formData.name}
                                        onChange={handleChange}
                                        className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-lg font-medium transition-colors duration-200"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-bold leading-6 text-black mb-2 uppercase tracking-wide">
                                        Shipping Address
                                    </label>
                                    <textarea
                                        name="address"
                                        required
                                        rows={3}
                                        value={formData.address}
                                        onChange={handleChange}
                                        className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-lg font-medium transition-colors duration-200 resize-none"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-bold leading-6 text-black mb-2 uppercase tracking-wide">
                                        Phone Number
                                    </label>
                                    <input
                                        name="phone"
                                        type="tel"
                                        required
                                        value={formData.phone}
                                        onChange={handleChange}
                                        className="block w-full border-2 border-black py-3 px-4 text-black outline-none focus:ring-0 focus:border-[#ed7844] sm:text-lg font-medium transition-colors duration-200"
                                    />
                                </div>

                                <div className="pt-8 border-t-4 border-black mt-8">
                                    <h2 className="text-3xl font-extrabold uppercase tracking-tight mb-6 mt-4">Payment Method</h2>
                                    <div className="space-y-4">
                                        {['credit_card', 'upi', 'cod'].map((method) => (
                                            <div key={method} className="flex items-center">
                                                <input
                                                    id={method}
                                                    name="paymentMethod"
                                                    type="radio"
                                                    value={method}
                                                    checked={formData.paymentMethod === method}
                                                    onChange={handleChange}
                                                    className="h-6 w-6 border-2 border-black text-[#ed7844] focus:ring-black accent-black focus:ring-2"
                                                />
                                                <label htmlFor={method} className="ml-4 block text-lg font-bold text-gray-900 uppercase tracking-wide">
                                                    {method === 'credit_card' && 'Credit Card'}
                                                    {method === 'upi' && 'UPI'}
                                                    {method === 'cod' && 'Cash on Delivery'}
                                                </label>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                <button
                                    type="submit"
                                    disabled={isSubmitting}
                                    className="w-full mt-10 bg-[#ed7844] border-4 border-black px-6 py-5 text-xl font-black uppercase tracking-widest text-black hover:text-white hover:bg-black transition-all duration-300 disabled:opacity-50 flex justify-center items-center"
                                >
                                    {isSubmitting ? (
                                        <div className="animate-spin rounded-full h-8 w-8 border-b-4 border-black border-t-white"></div>
                                    ) : (
                                        'Place Order'
                                    )}
                                </button>
                            </form>
                        </div>
                    </div>

                    {/* Order Summary */}
                    <div className="w-full lg:w-1/3">
                        <div className="bg-white border-4 border-black p-8 shadow-[8px_8px_0px_0px_rgba(237,120,68,1)] sticky top-32">
                            <h3 className="text-2xl font-extrabold uppercase tracking-tight mb-8 border-b-2 border-dashed border-gray-300 pb-4">Order Summary</h3>

                            <div className="space-y-4 mb-8 max-h-64 overflow-y-auto pr-2">
                                {cart.map((item) => (
                                    <div key={item.id} className="flex justify-between items-start font-bold border-b border-gray-200 pb-2">
                                        <div className="flex-1 pr-4">
                                            <span className="text-black block line-clamp-1">{item.name}</span>
                                            <span className="text-sm text-gray-500">Qty: {item.quantity}</span>
                                        </div>
                                        <span className="text-black">${(item.price * item.quantity).toFixed(2)}</span>
                                    </div>
                                ))}
                            </div>

                            <div className="space-y-4 mb-8">
                                <div className="flex justify-between font-bold text-gray-600 text-lg">
                                    <span>Subtotal</span>
                                    <span>${cartTotal.toFixed(2)}</span>
                                </div>
                                <div className="flex justify-between font-bold text-gray-600 text-lg">
                                    <span>Tax (5%)</span>
                                    <span>${taxAmount.toFixed(2)}</span>
                                </div>
                            </div>
                            <div className="flex justify-between font-black text-3xl pt-6 border-t-4 border-black">
                                <span>Total</span>
                                <span>${finalTotal.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Checkout;
