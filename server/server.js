const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const router = require('express-promise-router')();

const {PythonShell} = require('python-shell');
const cookieParser = require('cookie-parser');
const multer  = require('multer');
const execSync = require('child_process').execSync;
const path = require("path");

var uuid = null;

app.set("view engine", "ejs");
app.use(cookieParser());
app.use(bodyParser.urlencoded({ limit:'100mb',extended: true }));
app.use(express.static('images'))
app.use(express.static('image'))


app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(bodyParser.json());

/* DO NOT USE LOCALHOST */
// var options = {
//      mode: 'text',
//      pythonPath: '/usr/local/bin/python',
//      pythonOptions: ['-u'],
//      // make sure you use an absolute path for scriptPath
//      scriptPath: '/home/ec2-user/VIP_enPiT2020/server/'
//     };


const sleep = (millis,request,response) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // console.log(request);
      var test = request.cookies.test;
      const path = 'images/share_image/' + test + '.png';
      var pyshell = new PythonShell('color.py',{mode:'text'});
      pyshell.send(path);
      var n=0;
      pyshell.on('message',function (data){
          if(n==0){
            cloth_result = data;
            cloth_result=cloth_result.substring(5);
            response.cookie('cloth_result', cloth_result, {maxAge:60000, httpOnly:false});
          }
          else if (n==1){
            cloth_url =  data;
            response.cookie('cloth_url', cloth_url, {maxAge:60000, httpOnly:false});
          }
          n += 1
      });
      resolve()
    }, millis);
  });
};

const redirects = (millis,res,req) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      var test = req.cookies.test;
      res.redirect(307,'/result_'+test);
      resolve()
    }, millis);
  });
};

app.get('/', function (req, res) {
  var file = fs.readdirSync('./images/share_image');
  var files = [];
  for (let i = 0; i < file.length; i++){
    var fil = '/share_image/' + file[i];
    files.push(fil)
  }
  res.render("index",{files:files});
});

app.get('/result_:uuid', function (req, res) {
  var cloth_result = req.cookies.cloth_result;
  var cloth_url = req.cookies.cloth_url;
  var test = req.cookies.test;
  console.log("cloth_result -->",cloth_result,"cloth_url -->",cloth_url,"test -->",test);

  res.render("result",{file:cloth_result, url:cloth_url, image:"/share_image/"+test + ".png"});
});

app.get('/download', async (req, res) => {
  res.cookie('test', uuid, {maxAge:60000, httpOnly:false});
  res.redirect('/analysis/'+uuid);
});

app.post('/download', async (req, res) => {
  // クライアントからの送信データを取得する
  let body = req.body;
  let parse = JSON.parse(JSON.stringify(body));
  let parse_data = parse.data;
  var data = parse_data.replace(/^data:image\/\w+;base64,/, "");
  var buf = Buffer.from(data, 'base64');
  fs.writeFile('./images/downloads/image.png', buf, function(err, result) {
    if(err) console.log('error', err);
  });
  uuid = getUniqueStr();
  fs.writeFile('./images/share_image/' + uuid + '.png', buf, function(err, result) {
    if(err) console.log('error', err);
  });
});

app.get('/analysis/:uuid', (req, res, next) => {
  awaitFunc(req,res).then(() => {awaitRedirect(res,req)});
  //awaitFunc(res)
});

async function awaitFunc(req,res) {
  console.log(1);
  await sleep(2000,req,res); // Promise が返ってくるまで awaitで 処理停止
  console.log(2); // 約3秒経過に表示
}
async function awaitRedirect(res,req) {
  console.log(3);
  await redirects(3000,res,req); // Promise が返ってくるまで awaitで 処理停止
  console.log(4); // 約3秒経過に表示
}

function getUniqueStr(myStrong){
 var strong = 1000;
 if (myStrong) strong = myStrong;
 return new Date().getTime().toString(16)  + Math.floor(strong*Math.random()).toString(16)
}

app.listen(443);
