const express = require('express')
var cors = require('cors')
bodyParser = require('body-parser');
const fs = require('fs');

const app = express()
app.use(cors())
app.use(express.json({limit: '50mb'}));

app.post('/', (req, res) => {
    console.log(req.body);
    let buff = Buffer.from(req.body._image.substr(23), 'base64');
    fs.writeFileSync('stack-abuse-logo-out.jpeg', buff);

    const { spawn } = require('child_process');
    const pyProg = spawn('python', ['./../Models/main.py',req.body._card_number, req.body._expiry_month, req.body._name, req.body._cvv, req.body._mouse_text, req.body._image]);

    pyProg.stdout.on('data', function(data) {

        console.log(data.toString());
        res.json({response:data.toString()});
    });
})

app.listen(4000, () => console.log('Application listening on port 4000!'))