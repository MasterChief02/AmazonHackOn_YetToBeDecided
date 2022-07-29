import React, {useState} from 'react'
import Webcam from './Webcam';
function LoginForm({Login,error}) {
    const [details,setDetails]=useState({userid:"",password:""});
    const submitHandler = e =>{
        e.preventDefault();
        
        if(e.nativeEvent.submitter.value==="LOGIN"){
        Login(details);
        }
    }
    
  return (
    <>
    <form onSubmit={submitHandler}>
       <div className="form-inner">
            
            <h2>Net Banking</h2>
            {(error === "match") ? (<div style={{color: "#FFCE00", fontSize:"12px"}}className="error">{"Details do not match"}</div>):""}
            {(error === "invalid") ? (<div style={{color: "#FE4880", fontSize:"12px"}}className="error">{"Invalid user Warning!"}</div>):""}
            {(error === "blocked") ? (<div style={{color: "#FE4880", fontSize:"12px"}}className="error">{"User Blocked!"}</div>):""}
            <div className="form-group">
            
                <label htmlFor="userid"> User Id: </label>
                <input type="text" name="userid" id="userid" onChange={e => setDetails({...details,userid:e.target.value})} value={details.userid}/>
            </div>
            
            <div className="form-group">
                <label htmlFor="password"> Password: </label>
                <input type="password" name="password" id="password" onChange={e => setDetails({...details,password:e.target.value})} value={details.password}/>
            </div>
            <div className="webcam-form">
                <Webcam/>
                <div className='lab'>
                    Your Image
                </div>
            </div>

            <input type="submit" value="LOGIN" e="LOGIN"/>
       </div>
       
   </form>
   
   </>
  )
}
 
export default LoginForm