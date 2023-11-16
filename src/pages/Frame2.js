import { useNavigate } from 'react-router-dom';
import styles from './Frame2.module.css';

const Frame2 = () => {
  const navigate = useNavigate();

  const handleBackClick = () => {
    navigate(-2);
  };

  return (
    <div className={styles.vectorParent}>
      <img className={styles.frameChild} alt="" src="/rectangle-8@2x.png" />
      <div className={styles.scanToPurchase}>Scan to purchase</div>
      <img className={styles.QR} alt="" src="/qrcode.png" />
      <button className={styles.backButton} onClick={handleBackClick}>
        Back
      </button>
    </div>
  );
};
export default Frame2;
