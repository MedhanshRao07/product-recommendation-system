import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const Cart = () => {
    const { cart, removeFromCart, updateQuantity, cartTotal } = useCart();
    const navigate = useNavigate();

    const taxRate = 0.05;
    const taxAmount = cartTotal * taxRate;
    const shippingThreshold = 100;
    const freeShipping = cartTotal >= shippingThreshold;
    const shippingCost = freeShipping ? 0 : 9.99;
    const finalTotal = cartTotal + taxAmount + shippingCost;

    return (
        <div className="min-h-screen bg-[#fafafa] pt-20 pb-16 text-black">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">

                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-black uppercase tracking-tight">Your Cart</h1>
                        <p className="text-sm text-gray-500 font-medium mt-1">{cart.length} {cart.length === 1 ? 'item' : 'items'}</p>
                    </div>
                    <button
                        onClick={() => navigate('/products')}
                        className="text-xs font-bold uppercase tracking-wider text-[#ed7844] hover:text-black transition-colors"
                    >
                        ← Continue Shopping
                    </button>
                </div>

                {/* Free Shipping Bar */}
                {cart.length > 0 && !freeShipping && (
                    <div className="mb-6 bg-white border-2 border-dashed border-gray-300 p-4">
                        <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-bold uppercase tracking-wider text-gray-500">
                                🚚 Add ${(shippingThreshold - cartTotal).toFixed(2)} more for free shipping!
                            </span>
                            <span className="text-xs font-bold text-gray-400">${cartTotal.toFixed(2)} / ${shippingThreshold.toFixed(2)}</span>
                        </div>
                        <div className="w-full bg-gray-200 h-1.5">
                            <div 
                                className="bg-[#ed7844] h-1.5 transition-all duration-500"
                                style={{ width: `${Math.min(100, (cartTotal / shippingThreshold) * 100)}%` }}
                            />
                        </div>
                    </div>
                )}
                {cart.length > 0 && freeShipping && (
                    <div className="mb-6 bg-green-50 border-2 border-green-200 p-3 text-center">
                        <span className="text-sm font-bold text-green-700">🎉 You qualify for FREE shipping!</span>
                    </div>
                )}

                {cart.length === 0 ? (
                    <div className="bg-white border-2 border-gray-200 p-16 text-center">
                        <div className="text-6xl mb-6">🛒</div>
                        <h2 className="text-2xl font-black uppercase tracking-tight mb-4">Your cart is empty</h2>
                        <p className="text-gray-500 mb-8 font-medium">Looks like you haven't added anything yet.</p>
                        <button
                            onClick={() => navigate('/products')}
                            className="px-8 py-3 bg-black text-white text-sm font-bold uppercase tracking-widest hover:bg-[#ed7844] transition-colors"
                        >
                            Start Shopping
                        </button>
                    </div>
                ) : (
                    <div className="flex flex-col lg:flex-row gap-8">
                        {/* Cart Items */}
                        <div className="flex-1 space-y-4">
                            {cart.map((item) => (
                                <div key={item.id} className="flex gap-4 bg-white border border-gray-200 p-4 hover:border-black transition-colors duration-200">
                                    {/* Image */}
                                    <div className="w-24 h-24 flex-shrink-0 bg-gray-100 overflow-hidden">
                                        {item.image_url && item.image_url !== 'url' ? (
                                            <img src={item.image_url} alt={item.name} className="w-full h-full object-cover" loading="lazy" />
                                        ) : (
                                            <div className="w-full h-full flex items-center justify-center text-gray-300 text-xs">No Image</div>
                                        )}
                                    </div>
                                    
                                    {/* Details */}
                                    <div className="flex-1 min-w-0">
                                        <div className="flex justify-between items-start gap-2">
                                            <div className="min-w-0">
                                                <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest">{item.brand}</p>
                                                <h3 className="text-sm font-bold text-black truncate">{item.name}</h3>
                                            </div>
                                            <button
                                                onClick={() => removeFromCart(item.id)}
                                                className="text-gray-300 hover:text-red-500 transition-colors flex-shrink-0"
                                                title="Remove"
                                            >
                                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                                </svg>
                                            </button>
                                        </div>
                                        
                                        <div className="flex items-end justify-between mt-3">
                                            {/* Quantity Controls */}
                                            <div className="flex items-center border border-gray-200">
                                                <button
                                                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                                    disabled={item.quantity <= 1}
                                                    className="w-8 h-8 flex items-center justify-center text-sm font-bold hover:bg-gray-100 disabled:opacity-30 transition-colors"
                                                >−</button>
                                                <span className="w-10 h-8 flex items-center justify-center text-sm font-bold border-x border-gray-200">{item.quantity}</span>
                                                <button
                                                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                                    className="w-8 h-8 flex items-center justify-center text-sm font-bold hover:bg-gray-100 transition-colors"
                                                >+</button>
                                            </div>
                                            {/* Price */}
                                            <div className="text-right">
                                                <p className="text-xs text-gray-400 font-medium">${item.price.toFixed(2)} × {item.quantity}</p>
                                                <p className="text-lg font-black">${(item.price * item.quantity).toFixed(2)}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Order Summary */}
                        <div className="w-full lg:w-80 flex-shrink-0">
                            <div className="bg-white border-2 border-black p-6 sticky top-24">
                                <h3 className="text-lg font-black uppercase tracking-tight mb-6 pb-4 border-b-2 border-gray-200">
                                    Order Summary
                                </h3>
                                <div className="space-y-3 mb-6 text-sm">
                                    <div className="flex justify-between font-medium text-gray-600">
                                        <span>Subtotal ({cart.reduce((s, i) => s + i.quantity, 0)} items)</span>
                                        <span>${cartTotal.toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between font-medium text-gray-600">
                                        <span>Tax (5%)</span>
                                        <span>${taxAmount.toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between font-medium text-gray-600">
                                        <span>Shipping</span>
                                        <span className={freeShipping ? 'text-green-600 font-bold' : ''}>{freeShipping ? 'FREE' : `$${shippingCost.toFixed(2)}`}</span>
                                    </div>
                                </div>
                                <div className="flex justify-between text-2xl font-black pt-4 border-t-2 border-black mb-6">
                                    <span>Total</span>
                                    <span>${finalTotal.toFixed(2)}</span>
                                </div>
                                <button
                                    onClick={() => navigate('/checkout')}
                                    className="w-full py-3.5 bg-[#ed7844] text-black text-sm font-bold uppercase tracking-widest border-2 border-black hover:bg-black hover:text-white transition-all duration-200"
                                >
                                    Checkout
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Cart;
