const express = require('express')
const {spawn} = require('child_process');
const app = express()
const bodyParser = require('body-parser')
const cors = require('cors')
const port = 3000


app.use( bodyParser.json() );       // to support JSON-encoded bodies

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
 extended: true})); 
app.use(cors());


//You can use this to check if your server is working
app.get('/', (req, res)=>{
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python3', ['./python/test.py', 'text', 4]);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });
    console.log( process.env.PATH );
        
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

app.get('/getMove', (req, res) => {
    res.send("finding optimal move using minimax algorithm with alpha-beta pruning...");
});


//Start your server on a specified port
app.listen(port, ()=>{
    console.log(`Server is runing on port ${port}`)
});