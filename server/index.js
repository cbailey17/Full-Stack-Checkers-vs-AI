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


app.post('/', (req, res) => {

    console.log(req.body);

    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python3', ['./python/Python-Checkers-solver-master/uiCheckers.py', req.body]);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        console.log(data.toString());
        dataToSend = data.toString();
    });  
        
    python.stderr.on('data', (data) => {
        console.error('err: ', data.toString());
    });
    
    python.on('error', (error) => {
        console.error('error: ', error.message);
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
    });
});


//Start your server on a specified port
app.listen(port, ()=>{
    console.group(`Server is running on port ${port}......`)
    console.log("Try your hand at playing my AI algorithm in checkers!");
    console.log("Author: Alex Cameron Bailey");
    console.groupEnd("-----------------------------------------------");
});