import styles from "./Frame1.module.css";

const Frame1 = () => {
  return (
    <div className={styles.ellipseParent}>
      <img className={styles.frameChild} alt="" src="/ellipse-5@2x.png" />
      <div className={styles.thankYou}>THANK YOU!</div>
      <img className={styles.image2Icon} alt="" src="/image-2@2x.png" />
    </div>
  );
};

export default Frame1;
