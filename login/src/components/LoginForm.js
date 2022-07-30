import React, {useRef,useState} from 'react'
import Web from './Web';
function LoginForm({Login,error}) {
    const [details,setDetails]=useState({userid:"",password:"",photoref:""});
    const submitHandler = e =>{
        e.preventDefault();
        
        if(e.nativeEvent.submitter.value==="LOGIN"){
        Login(details);
        }
    }
    const Photo=(Photo)=>{
        if(Photo){
        details.photoref=Photo;
        }
        console.log(Photo);
    }
  return (
    <>
    <form onSubmit={submitHandler}>
       <div className="form-inner">
            
            <h2>Net Banking</h2>
            {(error === "match") ? (<div style={{color: "#FFCE00", fontSize:"12px"}}className="error">{"Details do not match"}</div>):""}
            {(error === "invalid") ? (<div style={{color: "#FE4880", fontSize:"12px"}}className="error">{"Invalid user Warning!"}</div>):""}
            {(error === "blocked") ? (<div style={{color: "#FE4880", fontSize:"12px"}}className="error">{"User Blocked!"}</div>):""}
            {(error === "nophoto") ? (<div style={{color: "#FFCE00", fontSize:"12px"}}className="error">{"Please add your photo"}</div>):""}
            <div className="form-group">
            
                <label htmlFor="userid"> User Id: </label>
                <input type="text" name="userid" id="userid" onChange={e => setDetails({...details,userid:e.target.value})} value={details.userid}/>
            </div>
            
            <div className="form-group">
                <label htmlFor="password"> Password: </label>
                <input type="password" name="password" id="password" onChange={e => setDetails({...details,password:e.target.value})} value={details.password}/>
            </div>
            <div className="webcam-form">
                <Web Photo={Photo}/>
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