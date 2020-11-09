var express = require('express');
var bodyParser = require('body-parser')
var fs = require('fs');
var app = express();

var {PythonShell} = require('python-shell');

app.set("view engine", "ejs");

const multer  = require('multer');
let execSync = require('child_process').execSync;
const path = require("path");

var cloth_result=[];

// PythonShell.run('color.py', null, function (err, data) {
//   if (err) throw err;
//     cloth_import=data[4];
//     cloth_result=data[5];
//     console.log(cloth_import);
//     console.log(cloth_result)
//     console.log(data[4]);
//     console.log('finished');
// });

app.use(express.static('images'))
app.use(express.static('image'))


app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.static('images'));
app.use(bodyParser.json());

app.get('/', function (req, res) {
    //res.sendfile('index.ejs');
    //console.log(cloth_import);
    //res.render("test",{file:cloth_import});
    //res.redirect('http://google.com');
    res.render("index");
});

app.get('/result', function (req, res) {
    //res.sendfile(cloth_import);
    console.log("きとる");
    console.log(cloth_result);
    res.render("index",{file:cloth_result});
});


app.post('/download', (req, res) => {
  // クライアントからの送信データを取得する
    var a = function() {
        return new Promise(function(resolve, reject) {
            setTimeout(function() {
                let body = req.body;
                let parse = JSON.parse(JSON.stringify(body));
                let parse_data = parse.data;
                var data = parse_data.replace(/^data:image\/\w+;base64,/, "");
                var buf = Buffer.from(data, 'base64');
                fs.writeFile('./images/downloads/image.png', buf, function(err, result) {
                    if(err) console.log('error', err);
                });
                resolve();
            }, 1000);
        });
    };
    var b = function() {
        return new Promise(function(resolve, reject) {
            setTimeout(function() {
                PythonShell.run('color.py', null, function (err, data) {
                    console.log(data);
                    console.log('finished');
                    cloth_result=data[1];
                    console.log(cloth_result);
                    cloth_result=cloth_result.substring(5);
                    res.locals.file = cloth_result
                    console.log(cloth_result);
                });
                resolve();
            }, 1000);
        });
    };

    a().then(b);

  //console.log("遷移するはずやねんな");
  //res.render("index",{file:cloth_result});

  // res.redirect(307,'/result');
});

app.listen(443);

