'use client';

import { useEffect, useRef } from 'react';

const ReadingProgress = () => {
  const progressRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let ticking = false;

    const updateProgress = () => {
      if (!progressRef.current) return;

      const scrollTop = window.scrollY;
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;

      // Avoid division by zero
      if (scrollHeight <= 0) {
        progressRef.current.style.width = '0%';
        progressRef.current.classList.add('opacity-0');
        return;
      }

      const scrollPercent = (scrollTop / scrollHeight) * 100;
      progressRef.current.style.width = `${scrollPercent}%`;

      // Only show when user has scrolled past the top
      if (scrollTop > 0) {
        progressRef.current.classList.remove('opacity-0');
      } else {
        progressRef.current.classList.add('opacity-0');
      }

      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateProgress);
        ticking = true;
      }
    };

    // Add scroll event listener
    window.addEventListener('scroll', requestTick, { passive: true });

    // Initial update
    updateProgress();

    // Cleanup on unmount
    return () => {
      window.removeEventListener('scroll', requestTick);
    };
  }, []);

  return (
    <div className="fixed top-0 left-0 right-0 z-50 h-1 bg-gray-200 opacity-0 transition-opacity duration-200">
      <div
        ref={progressRef}
        className="h-full bg-blue-600 transition-all duration-100 ease-out"
        style={{ width: '0%' }}
      />
    </div>
  );
};

export default ReadingProgress;