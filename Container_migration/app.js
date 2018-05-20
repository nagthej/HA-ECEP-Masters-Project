const express = require('express');
var cors = require('cors');
var http = require('http');
var path = require('path');
var app = express();
var bodyParser = require('body-parser');
var ejs = require("ejs");
var shell = require('shelljs');

app.set('view engine', 'ejs');

app.get('/', function(req, res) {
    res.render('home',function(err, result) {
        // render on success
        if (!err) {
                 res.end(result);
        }
        // render or error
        else {
                 res.end('An error occurred');
                 console.log(err);
        }
    });
});


app.get('/start', function(req,res){
    console.log("here in start button")

 //shell.exec(comandToExecute, {silent:true}).stdout;
 //you need little improvisation

 shell.exec('./start_script.sh');

 setTimeout(function(){
     res.redirect('/')
 },10000)
});


app.get('/migrate', function(req,res){
    console.log("here in start button")

 //shell.exec(comandToExecute, {silent:true}).stdout;
 //you need little improvisation
 shell.exec('./my_script.sh')
 setTimeout(function(){
    res.redirect('/')
},10000)
});

app.listen(3001, () => console.log('Server running on port 3001'))



