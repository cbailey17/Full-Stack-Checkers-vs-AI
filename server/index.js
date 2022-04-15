const express = require('express')
const {spawn} = require('child_process');
const app = express()
const bodyParser = require('body-parser')
const cors = require('cors')
const port = 3000
var action_str;


app.use( bodyParser.json() );       // to support JSON-encoded bodies

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
 extended: true})); 
app.use(cors());

app.post('/initializeBoard', (req, res) => {
    const python = spawn('python3', ['./python/Python-Checkers-solver-master/boardinit.py']);

    python.stdout.on('data', function (data) {
        console.log('Initializing Board...');
        dataToSend = data.toString();
    });  
    python.stderr.on('data', (data) => {
        console.error('err: ', data.toString());
    });
    python.on('error', (error) => {
        console.error('error: ', error.message);
    });
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        res.send(dataToSend)
    });
});


app.post('/', (req, res) => {
    var dataToSend;
    console.log("Humans move");
    console.log(req.body.action_str);
    console.log("*******************");

    const python = spawn('python3', ['./python/Python-Checkers-solver-master/uiCheckers.py', req.body.action_str]);

    python.stdout.on('data', function (data) {
        console.log('Getting AI move.....');
        dataToSend = data.toString();
        console.log("computers move");
        console.log(dataToSend);
    });  
    python.stderr.on('data', (data) => {
        console.error('err: ', data.toString());
    });
    python.on('error', (error) => {
        console.error('error: ', error.message);
    });
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        res.send(dataToSend)
    });
});

app.post('/clearGameCache', (req, res) => {
    var dataToSend;
    const python = spawn('python3', ['./python/Python-Checkers-solver-master/clearCache.py']);

    python.stdout.on('data', function (data) {
        console.log('Clearing cache......');
        dataToSend = data.toString();
    });  
    python.stderr.on('data', (data) => {
        console.error('err: ', data.toString());
    });
    python.on('error', (error) => {
        console.error('error: ', error.message);
    });
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        res.send(dataToSend)
    });
});


app.listen(port, ()=>{
    console.group(`Server is running on port ${port}......`)
    console.log("Try your hand at playing my AI algorithm in checkers!");
    console.log("Author: Alex Cameron Bailey");
    console.groupEnd("-----------------------------------------------");
});