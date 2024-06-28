import React from 'react';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';
import './SkeletonWrapper.css';

const SkeletonWrapper = ({ type, lines = 0, squares = 0, image = false }) => {
  return (
    <div className={`skeleton ${type}`}>
      {type === 'news-article' && (
        <>
          <Skeleton height={20} className="skeleton-line" />
          <div className="news-header">
            <Skeleton height={113} width={100} className="skeleton-square" />
            <div className="text">
              {Array(lines).fill().map((_, index) => (
                <Skeleton key={index} height={20} className="skeleton-line" />
              ))}
            </div>
          </div>
          <div className="footer">
            {Array(3).fill().map((_, index) => (
              <Skeleton key={index} height={20} className="skeleton-line" />
            ))}
          </div>
        </>
      )}
      {type !== 'news-article' && image && (
        <Skeleton
          height={type === 'youtube' ? 100 : 400}
          width="100%"
          className="skeleton-image"
        />
      )}
      {type !== 'news-article' && !image && Array(lines).fill().map((_, index) => (
        <Skeleton key={index} height={20} className="skeleton-line" />
      ))}
    </div>
  );
};

export default SkeletonWrapper;
