const express = require('express')
var cors = require('cors')
bodyParser = require('body-parser');

const app = express()
app.use(cors())
app.use(bodyParser.json());

app.post('/', (req, res) => {
    console.log(req.body);

    const { spawn } = require('child_process');
    const pyProg = spawn('python', ['./../Models/test.py',1,2,5]);

    pyProg.stdout.on('data', function(data) {
        console.log(data.toString());
        res.json({response:data.toString()});
    });
})

app.listen(4000, () => console.log('Application listening on port 4000!'))