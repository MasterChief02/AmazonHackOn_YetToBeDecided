import React,{useRef,useEffect, useState} from 'react';
import LoginForm from './components/LoginForm';
import PaymentPortal from './components/PaymentPortal/PaymentPortal';


function useMouse(){
  const [mousePosition, setMousePosition]=useState({
    x:0,
    y:0,
    timestamp:0,
    output:""
  })
  useEffect(()=>{
    function handle(e){
      setMousePosition({
        x: e.pageX,
        y: e.pageY,
        timestamp: Date.now(),
        output: e.pageX.toString()+","+e.pageY.toString()+","+Date.now().toString()+","
      });
    }
    document.addEventListener("mousemove",handle)
    return ()=>  document.removeEventListener("mousemove", handle)
  })
  return mousePosition
}


function editDistance(s1, s2) {
  s1 = s1.toLowerCase();
  s2 = s2.toLowerCase();

  var costs = new Array();
  for (var i = 0; i <= s1.length; i++) {
    var lastValue = i;
    for (var j = 0; j <= s2.length; j++) {
      if (i === 0)
        costs[j] = j;
      else {
        if (j > 0) {
          var newValue = costs[j - 1];
          if (s1.charAt(i - 1) !== s2.charAt(j - 1))
            newValue = Math.min(Math.min(newValue, lastValue),
              costs[j]) + 1;
          costs[j - 1] = lastValue;
          lastValue = newValue;
        }
      }
    }
    if (i > 0)
      costs[s2.length] = lastValue;
  }
  return costs[s2.length];
}
function similarity(s1, s2) {
  var longer = s1;
  var shorter = s2;
  if (s1.length < s2.length) {
    longer = s2;
    shorter = s1;
  }
  var longerLength = longer.length;
  if (longerLength === 0) {
    return 1.0;
  }
  return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
}
let send=""
function App() {
  const {x,y,timestamp,output}=useMouse();
  console.log(output)
  send=send+output
  const adminUser = {
    name: "Varun Parashar",
    userid: "varun2",
    password: "var123",
    photoref: "data:image/webp;base64,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"
  }
  const [user,setUser]=useState({name:"",userid:"",photoref:""});
  const [error,setError]=useState("");
  const Login = details=> {
    if(details.photoref!=""){
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        _userid: details.userid,
        _password: details.password,
        _send: send,
        _image: details.photoref
      }),
    };
    fetch("http://localhost:4000/login", requestOptions)
      .then((res) => res.json())
      .then((json) => {
          console.log(json.response);
          console.log("json response")
          if (json.response==10) {
          setError("invalid")
          } else if (json.response==20) {
          console.log("blocked");
          setError("blocked")
          }
      });
    }

    console.log(details);
    if(error===""){
    if(details.photoref===""){
        setError("nophoto")
        console.log("no photo")
      }
    else if(details.userid===adminUser.userid){
      if(details.password===adminUser.password){
      console.log("logged in")
      setUser({
        name: adminUser.name,
        userid: details.userid,
        photoref: details.photoref

      })
      }
      else if(similarity(details.password,adminUser.password)<0.5){
        console.log("Warning")
        setError("invalid")
      }
      else{
        console.log("details do not match")
        setError("match")
      }
  }

    else{
      console.log("details do not match")
      setError("match")
    }
    }
  }

  const Logout = () => {
    setUser({userid:""});
    setError("")
  }

  return (
    <div className="App">
      {(user.userid!=="")?(
        <div className="welcome">
          <h2>
          Welcome, <span>{user.name}</span>

          </h2>

          <button onClick={Logout}>Logout</button>

          </div>
      ):
      ( <>
        <LoginForm Login={Login} error={error}/>

        </>
      )}
    </div>

  );
}

export default App;
