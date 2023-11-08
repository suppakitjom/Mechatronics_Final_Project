import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Frame.module.css";

const Frame = () => {
  const navigate = useNavigate();

  const onCashTextClick = useCallback(() => {
    navigate("/frame-5");
  }, [navigate]);

  const onQRCodeTextClick = useCallback(() => {
    navigate("/frame-3");
  }, [navigate]);

  return (
    <div className={styles.rectangleParent}>
      <img className={styles.frameChild} alt="" src="/rectangle-7@2x.png" />
      <div className={styles.howWouldYou}>How would you like to pay?</div>
      <img className={styles.frameItem} alt="" src="/rectangle-12@2x.png" />
      <img className={styles.frameInner} alt="" src="/rectangle-13@2x.png" />
      <div className={styles.cash} onClick={onCashTextClick}>
        Cash
      </div>
      <div className={styles.qrCode} onClick={onQRCodeTextClick}>
        QR Code
      </div>
    </div>
  );
};

export default Frame;
