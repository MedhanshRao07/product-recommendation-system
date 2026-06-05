import React, { useState, useEffect, useRef } from 'react';

const SafeImage = ({ src, alt, className = '' }) => {
    const [imageState, setImageState] = useState('loading');
    const imgRef = useRef(null);

    useEffect(() => {
        if (!src || src === 'url' || src === 'url_here' || (!src.startsWith('http') && !src.startsWith('/'))) {
            setImageState('error');
            return;
        }
        
        setImageState('loading');
        
        // If the image is instantly loaded from cache before onLoad can fire
        if (imgRef.current && imgRef.current.complete) {
            if (imgRef.current.naturalWidth > 0) {
                setImageState('loaded');
            }
        }
    }, [src]);

    const handleLoad = () => {
        setImageState('loaded');
    };

    const handleError = () => {
        setImageState('error');
        console.warn(`[SafeImage] Failed to load image asset: ${src}`);
    };

    return (
        <div className={`relative overflow-hidden bg-white flex-shrink-0 ${className}`}>
            {imageState === 'loading' && (
                <div className="absolute inset-0 animate-pulse bg-gray-200"></div>
            )}
            
            {imageState !== 'error' ? (
                <img
                    ref={imgRef}
                    src={src}
                    alt={alt}
                    loading="lazy"
                    onLoad={handleLoad}
                    onError={handleError}
                    className={`absolute inset-0 h-full w-full object-contain object-center transition-all duration-500 bg-white ${
                        imageState === 'loaded' ? 'opacity-100 group-hover:scale-105' : 'opacity-0'
                    }`}
                />
            ) : (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-100 text-gray-400 border-b-2 border-black">
                    <svg className="h-10 w-10 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span className="text-[10px] font-bold uppercase tracking-widest text-center px-2">No Image</span>
                </div>
            )}
        </div>
    );
};

export default SafeImage;
