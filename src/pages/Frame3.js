import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Frame3.module.css";

const Frame3 = () => {
  const navigate = useNavigate();
  const onRectangleImage3Click = useCallback(() => {
    navigate("/frame-6");
  }, [navigate]);
  const onCHECKOUTTextClick = useCallback(() => {
    navigate("/frame-6");
  }, [navigate]);

  const [orderData, setOrderData] = useState([]);
  const [currentDate, setCurrentDate] = useState('');
  const [totalPrice, setTotalPrice] = useState(0);

  useEffect(() => {
    // Function to fetch order data from the server
    const fetchOrderData = () => {
      fetch('http://127.0.0.1:6969/order') // Replace with your server's API endpoint
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          console.log(data)
          setOrderData(data);
          const total = data.reduce((acc, order) => acc + (order.quantity * order.price), 0);
          setTotalPrice(total);
        })
        .catch((error) => {
          console.error('Error fetching orders:', error);
        });
    };

    // Fetch data initially and set the current date
    fetchOrderData();
    updateCurrentDate();

    // Fetch data every second
    const intervalId = setInterval(() => {
      fetchOrderData();
      updateCurrentDate();
    }, 1000);

    // Clear the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []);

  const updateCurrentDate = () => {
    const now = new Date();
    const day = now.getDate().toString().padStart(2, '0');
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const year = now.getFullYear().toString().slice(-2);
    setCurrentDate(`${day}/${month}/${year}`);
  };

  return (
    <div className={styles.rectangleParent}>
      <img className={styles.frameChild} alt="" src="/rectangle-9@2x.png" />
      <img className={styles.frameItem} alt="" src="/rectangle-5@2x.png" />
      <div className={styles.date}>{`Date: ${currentDate}`}</div>
      <img className={styles.frameInner} alt="" src="/rectangle-11@2x.png" />
      <img
        className={styles.rectangleIcon}
        alt=""
        src="/rectangle-10@2x.png"
        onClick={onRectangleImage3Click}
      />
      <div className={styles.orderSummary}>Order Summary</div>
      <div className={styles.checkout} onClick={onCHECKOUTTextClick}>CHECKOUT</div>
      <div className={styles.subtotal}>Subtotal: ฿{totalPrice}</div> 
      <div className={styles.lineDiv} />
     

      <div className={styles.frameChild}>
        <table className={styles.scrollableTableContainer }>
          <thead>
            <tr class="head">
              <th>Name</th>
              <th>Quantity</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {orderData.map((order, index) => (
              <tr key={index} className={styles.trow}>
                <td>{order.name}</td>
                <td>{order.quantity}</td>
                <td>{order.price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Frame3;