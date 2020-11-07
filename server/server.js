var express = require('express');
var bodyParser = require('body-parser')
var fs = require('fs');
var app = express();

var {PythonShell} = require('python-shell');

app.set("view engine", "ejs");

const multer  = require('multer');
let execSync = require('child_process').execSync;
const path = require("path");

var cloth_import=[];
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
    res.sendfile('index.html');
    //res.render("test",{file:cloth_import});
});

app.get('/result', function (req, res) {
    //res.sendfile(cloth_import);
    res.render("./views/test.ejs",{file,cloth_import});
});




app.listen(8080)



app.post('/download', (req, res) => {
  // クライアントからの送信データを取得する
  let body = req.body;
  let parse = JSON.parse(JSON.stringify(body));
  let parse_data = parse.data;
  var data = parse_data.replace(/^data:image\/\w+;base64,/, "");
  var buf = Buffer.from(data, 'base64');
  fs.writeFile('./images/downloads/image.png', buf);
});

app.listen(443);

