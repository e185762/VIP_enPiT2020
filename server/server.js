var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');
var app = express();
const router = require('express-promise-router')();

var {PythonShell} = require('python-shell');

app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({ limit:'100mb',extended: true }));

const multer  = require('multer');
let execSync = require('child_process').execSync;
const path = require("path");

var cloth_result=null;
var cloth_url=null;


/* DO NOT USE LOCALHOST */
var options = {
     mode: 'text',
     pythonPath: '/usr/local/bin/python',
     pythonOptions: ['-u'],
     // make sure you use an absolute path for scriptPath
     scriptPath: '/home/ec2-user/VIP_enPiT2020/server/'
    };

const sleep = (millis) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      PythonShell.run('color.py', null, function (err, data) {
        console.log(err);
	console.log(data);
        console.log('finished');
        cloth_result=data[1];
        console.log(cloth_result);
        cloth_result=cloth_result.substring(5);
        console.log(cloth_result);
        cloth_url = data[2]
      });
      resolve()
    }, millis);
  });
};
const redirects = (millis,res) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      res.redirect(307,'/result');
      resolve()
    }, millis);
  });
};

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
  res.render("result",{file:cloth_result, url:cloth_url});
});


app.post('/download', async (req, res) => {
  // クライアントからの送信データを取得する
  let body = req.body;
  let parse = JSON.parse(JSON.stringify(body));
  let parse_data = parse.data;
  var data = parse_data.replace(/^data:image\/\w+;base64,/, "");
  var buf = Buffer.from(data, 'base64');
  fs.writeFile('./images/downloads/canvas.png', buf, function(err, result) {
    if(err) console.log('error', err);
  });
});

app.get('/analysis', (req, res, next) => {
  awaitFunc(res).then(() => {awaitRedirect(res)});
  //awaitFunc(res)
});

async function awaitFunc(res) {
  console.log(1);
  await sleep(2000); // Promise が返ってくるまで awaitで 処理停止
  console.log(2); // 約3秒経過に表示
}
async function awaitRedirect(res) {
  console.log(3);
  await redirects(3000,res); // Promise が返ってくるまで awaitで 処理停止
  console.log(4); // 約3秒経過に表示
}


app.listen(443);

