import styles from "./Frame2.module.css";

const Frame2 = () => {
  return (
    <div className={styles.vectorParent}>
      <img className={styles.frameChild} alt="" src="/rectangle-8@2x.png" />
      <div className={styles.scanToPurchase}>Scan to purchase</div>
    </div>
  );
};

export default Frame2;
