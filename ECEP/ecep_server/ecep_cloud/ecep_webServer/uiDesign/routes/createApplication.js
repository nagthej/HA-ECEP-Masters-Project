
var express = require('express');
var router = express.Router();
var http = require('http');
var request = require("request");
var fs1 = require('fs');
var fs = require('fs-extra');
var formidable = require("formidable");
var util = require('util');

var mkdirp = require('mkdirp');
var mv=require('mv');
var multer = require('multer');

var fileName;



var filestorage = multer.diskStorage({
    destination: function (req, file, cb) {
        console.log("************************************************Entered multer");
        var dest = './upload/';
       mkdirp.sync(dest);
        cb(null, dest);
        console.log("*********************************Exited multer");
    },
    filename: function (req, file, cb) {
        console.log("FileName:" +file.originalname);
          fileName=file.originalname;
        cb(null, file.originalname);
    }

});

var rfcal_upload = multer({ storage: filestorage,limits: {fileSize: 30000000, files:1} });



router.post('/', rfcal_upload.single('applicationFile'),function (req, res,next) {
    //debugger
    console.log("***********************Entered Docker1");

    console.log("***************************body data:"+JSON.stringify(req.body));

    console.log("**********************Entered Docker2");


    console.log("******************filename:"+fileName);
    console.log("cont name"+req.body.containerName_app);

    var source= './upload/'+fileName;
    var destination = '/home/ubuntu/ecep/'+'admin'+'_'+req.body.containerName_app+'/'+fileName;

    fs.copy(source, destination, function (err) {
        if (err) return console.error(err);

        fs.remove(source);
        console.log("success!")


   var data = JSON.stringify({
        "command": "upStart",
        "username":"admin",
        "containerName":req.body.containerName_app,
        "deviceId":req.body.device_app,
        "filename":fileName
    });
    console.log(data);
    var post_options = {
        host: 'ec2-18-218-62-54.us-east-2.compute.amazonaws.com',
        port: '9000',
        path: '/handle_request',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(data)
        }
    };

    var post_req = http.request(post_options, function (reses) {
        reses.setEncoding('utf8');
        reses.on('data', function (chunk) {
            console.log('Response: ' + chunk);
            res.send({"data":"success"});
            //res.render('index', { title: 'Express' });
        });
    });

// post the data
    post_req.write(data);
    post_req.end();

});

});

module.exports = router;
  //  res.send({"data":"Success"});

/*
           console.log("Entered Docker3");

           var post_options = {
               //host: 'ec2-52-39-130-106.us-west-2.compute.amazonaws.com',
               host: 'http://ec2-18-218-62-54.us-east-2.compute.amazonaws.com',
               port: '9000',
               path: '/handle_request',
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
                   'Content-Length': Buffer.byteLength(data)
               }
           };

           console.log("**************************h1");
           var post_req = http.request(post_options, function (reses) {
               reses.setEncoding('utf8');
               console.log("*******************************h2");
               reses.on('data', function (chunk) {
                   console.log("***************************h3");
                   console.log('***********************Response: ' + chunk);
                   // res.send(chunk);
                   res.send({"data": "Success"});
                   // res.render('index', { title: 'Express' });
               });
           });
           console.log("h4");

// post the data
    post_req.write(data);
    post_req.end();

   });
});



module.exports = router;

*/

