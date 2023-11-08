import styles from "./Frame4.module.css";

const Frame4 = () => {
  return (
    <div className={styles.ellipseParent}>
      <img className={styles.frameChild} alt="" src="/ellipse-4@2x.png" />
      <div className={styles.pleaseInsertYour}>Please insert your card</div>
      <img className={styles.image1Icon} alt="" src="/image-1@2x.png" />
    </div>
  );
};

export default Frame4;
