import React, {useState} from 'react'

function LoginForm({Login,error}) {
    const [details,setDetails]=useState({userid:"",password:""});
    const submitHandler = e =>{
        e.preventDefault();
        Login(details);
    }
  return (
   <form onSubmit={submitHandler}>
       <div className="form-inner">
            <h2>Login</h2>
            {(error !== "") ? (<div style={{color: "#FFCE00"}}className="error">{error}</div>):""}
            <div className="form-group">
                <label htmlFor="userid"> User Id: </label>
                <input type="text" name="userid" id="userid" onChange={e => setDetails({...details,userid:e.target.value})} value={details.userid}/>
            </div>
            <div className="form-group">
                <label htmlFor="password"> Password: </label>
                <input type="password" name="password" id="password" onChange={e => setDetails({...details,password:e.target.value})} value={details.password}/>
            </div>
            <input type="submit" value="LOGIN"/>
       </div>
   </form>
  )
}
 
export default LoginForm