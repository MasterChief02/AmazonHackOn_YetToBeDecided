import React,{useState} from 'react';
import LoginForm from './components/LoginForm';
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

function App() {
  const adminUser = {
    name: "Varun Parashar",
    userid: "varun",
    password: "varun"
  }
  const [user,setUser]=useState({name:"",userid:""});
  const [error,setError]=useState(""); 
  const Login = details=> {
    console.log(details);
    if(details.userid===adminUser.userid){
      if(details.password===adminUser.password){
      console.log("logged in")
      setUser({
        name: adminUser.name,
        userid: details.userid,
      })
      }
      else if(similarity(details.password,adminUser.password)<0.3){
        console.log("Warning")
        setError("Invalid User Warning!")
      }
      else{
        console.log("details do not match")
        setError("Details do not match!")
      }
  }
    
    else{
      console.log("details do not match")
      setError("Details do not match!")
    }
  }
  const Logout = () => {
    setUser({userid:""});

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
      (
        <LoginForm Login={Login} error={error}/>
      )}
    </div>
  );
}

export default App;
