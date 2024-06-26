// Modal.js
import React from 'react';
import './Modal.css';

const Modal = ({ show, onClose, children }) => {
  if (!show) {
    return null;
  }

  const handleClickOutside = (e) => {
    if (e.target.className === 'modal-overlay') {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleClickOutside}>
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          &times;
        </button>
        <div className="modal-children">{children}</div>
      </div>
    </div>
  );
};

export default Modal;
