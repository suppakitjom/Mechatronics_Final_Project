import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Frame1.module.css';

const Frame1 = () => {
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate(-2);
  };

  return (
    <div className={styles.ellipseParent}>
      <img className={styles.frameChild} alt="" src="/ellipse-5@2x.png" />
      <div className={styles.thankYou}>THANK YOU!</div>
      <img className={styles.image2Icon} alt="" src="/image-2@2x.png" />
      <button className={styles.backButton} onClick={handleBackClick}>
        Back
      </button>
    </div>
  );
};

export default Frame1;
