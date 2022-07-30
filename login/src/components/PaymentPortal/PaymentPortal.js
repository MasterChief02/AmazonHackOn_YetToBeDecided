import React, {useRef, useEffect, useState} from 'react'
import styled from 'styled-components'
import Webcam from "react-webcam";


function PaymentPortal({mouseText}) {
    // Variables
    const [details,setDetails]=useState({card_number:"",expiry_month:"", name:"", cvv:"", image:null});
    const [showInvalid, setShowInvalid] = useState(false);
    const [showUserBlocked, setShowUserBlocked] = useState(false);
    const [paymentComplete, setPaymentComplete] = useState(false);

    const [image, setImage] = useState("");
    const webcamRef = React.useRef(null);

    // Functions
    const capture = React.useCallback(
        () => {
          setImage(webcamRef.current.getScreenshot());
        },
        [webcamRef]
      );

    const payHandler = () => {
        capture()
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              _card_number: details.card_number,
              _expiry_month: details.expiry_month,
              _name: details.name,
              _cvv: details.cvv,
              _mouse_text: mouseText,
              _image: image
            }),
          };
          fetch("http://localhost:4000/", requestOptions)
            .then((res) => res.json())
            .then((json) => {
                console.log(json.response);
                if (json.response==10) {
                setShowInvalid(true);
                setShowUserBlocked(false);
                } else if (json.response==20) {
                setShowInvalid(false);
                setShowUserBlocked(true);
                } else {
                setPaymentComplete(true);
                }
            });
    }

    // UI Designs
    const Form = styled.div`
        border: black sold 2px;
        background-color:rgba(0,0,0,0.3);
    `
    const InvalidMessage = styled.div`
        color: #FFCE00
    `
    const UserBlocked = styled.div`
        color: #FE4880
    `
    const FormEntry  = styled.div`
        label {
            display: block;
        }
        input {

        }
    `
    const PayButton = styled.button``
    const CancelButton = styled.button``


  return (
    <>
    <Form>
        {(showInvalid) ?
        <>
            <InvalidMessage>
                Details do not match
            </InvalidMessage>
        </>:<>
        </>}
        {(showUserBlocked) ?
        <>
            <UserBlocked>
                This card is blocked due to suspicious activities.
                Please check your e-mail for further details.
            </UserBlocked>
        </>:<>
        </>}
        <FormEntry>
            <label> Card Number </label>
            <input type="number" name="card_number" id="card_number" onChange={e => setDetails({...details,card_number:e.target.value})} value={details.card_number}/>
        </FormEntry>
        <FormEntry>
            <label> Expiry Date </label>
            <input type="month" name="expiry_month" id="expiry_month" onChange={e => setDetails({...details,expiry_month:e.target.value})} value={details.expiry_month}/>
        </FormEntry>
        <FormEntry>
            <label> Full Name </label>
            <input type="text" name="name" id="name" onChange={e => setDetails({...details,name:e.target.value})} value={details.name}/>
        </FormEntry>
        <FormEntry>
            <label> CVV </label>
            <input type="number" name="cvv" id="cvv" onChange={e => setDetails({...details,cvv:e.target.value})} value={details.cvv}/>
        </FormEntry>
        <PayButton onClick={payHandler} >Pay Now</PayButton>
        <CancelButton>Cancel</CancelButton>
    </Form>
    <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1080}
      />
    </>
  )
}

export default PaymentPortal