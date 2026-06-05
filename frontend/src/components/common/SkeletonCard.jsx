import React from 'react';

const SkeletonCard = () => {
    return (
        <div className="border-2 border-gray-100 bg-white flex flex-col h-full animate-pulse shadow-sm">
            {/* Image Placeholder */}
            <div className="aspect-square w-full bg-gray-100 border-b border-gray-50"></div>
            
            {/* Content Placeholder */}
            <div className="p-5 flex flex-col flex-grow">
                {/* Brand */}
                <div className="h-2 bg-gray-200 w-1/3 mb-4 rounded-sm"></div>
                
                {/* Title */}
                <div className="h-3.5 bg-gray-200 w-full mb-2 rounded-sm"></div>
                <div className="h-3.5 bg-gray-200 w-4/5 mb-5 rounded-sm"></div>
                
                {/* Rating */}
                <div className="h-2.5 bg-gray-200 w-1/4 mb-5 rounded-sm"></div>
                
                {/* Footer */}
                <div className="mt-auto pt-4 border-t border-gray-50 flex flex-col gap-3">
                    {/* Price */}
                    <div className="h-5 bg-gray-200 w-1/4 rounded-sm"></div>
                    {/* Buttons */}
                    <div className="flex gap-2 h-10 mt-1">
                        <div className="flex-1 bg-gray-200 rounded-sm"></div>
                        <div className="w-10 bg-gray-200 rounded-sm"></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SkeletonCard;
