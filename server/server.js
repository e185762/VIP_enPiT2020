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

var options = {
     mode: 'text',
     pythonPath: '/usr/local/bin/python',
     pythonOptions: ['-u'],
     // make sure you use an absolute path for scriptPath
     scriptPath: '/home/ec2-user/VIP_enPiT2020/server/'
    };

const sleep = (millis,request,response) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // console.log(request);
      
      var test = request.cookies.test;
      const path = 'images/share_image/' + test + '.png';
      var pyshell = new PythonShell('color.py',options,{mode:'text'});
      pyshell.send(path);
      var n=0;
      const path_list = [];
      const url_list = [];
      pyshell.on('message',function (data){
      console.log(data);
      if(data=="fin"){
              response.cookie('cloth_result', path_list, {maxAge:60000, httpOnly:false});
              response.cookie('cloth_url', url_list);
      }
      else if(n%2==0){
          var cloth_result = data;
          cloth_result = cloth_result.substring(5);
          path_list.push(cloth_result);
          //console.log("path --> ",path_list);
        }
        else if (n%2==1){
          url_list.push(data);
          //console.log("url_list --> ",url_list);
        }
        n += 1
      });
      resolve();
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
  var lists = [];
  for (var i=0; i<file.length ;i++){
    var n = Number(file[i].slice(13,-4));
    lists.push([n,file[i]]);
  }
  lists.sort(function(a,b){return(b[0] - a[0]);});
  for (var i=0; i<lists.length ;i++){
    file[i] = lists[i][1];
  }
  var files = [];
  for (let i = 0; i < file.length-1; i++){
    var fil = '/share_image/' + file[i];
    files.push(fil);
  }
  console.log(files);
  res.render("index",{files:files});
});

app.get('/result_:uuid', function (req, res) {
  var cloth_result = req.cookies.cloth_result;
  var cloth_url = req.cookies.cloth_url;
  var test = req.cookies.test;
  console.log("cloth_result -->",cloth_result,"cloth_url -->",cloth_url,"test -->",test);
  if (cloth_url === undefined) {
    cloth_url = [];
  }
  res.render("result",{file:cloth_result, url:cloth_url, image:"/share_image/"+test + ".png"});
});

app.post('/download', async (req, res, next) => {
  // クライアントからの送信データを取得する
  let body = req.body;
  let parse = JSON.parse(JSON.stringify(body));
  let parse_data = parse.data;
  var data = parse_data.replace(/^data:image\/\w+;base64,/, "");
  var buf = Buffer.from(data, 'base64');
  fs.writeFile('./images/downloads/canvas.png', buf, function(err, result) {
    if(err) console.log('error', err);
  });
  uuid = getUniqueStr();
  res.cookie('test', uuid, {maxAge:60000, httpOnly:false});
  console.log("uuid -->",uuid);
  fs.writeFile('./images/share_image/' + uuid + '.png', buf, function(err, result) {
    if(err) console.log('error', err);
  });
  next();
});

app.get('/download', async (req, res, next) => {
  uuid = getUniqueStr();
  // res.cookie('test', uuid, {maxAge:60000, httpOnly:false});
  res.redirect('/analysis/'+uuid);
});

app.get('/analysis/:uuid', (req, res) => {
    var uuid = req.cookies.test;
    fs.open('./images/share_image/' + uuid + '.png', 'r', (err, fd) => {
    if (err) {
        console.log("ファイルが存在しない時の処理");
        res.redirect('/analysis/'+uuid);
    }
    if(fd){
        console.log("ファイルが存在する時の処理");
        awaitFunc(req,res).then(() => {awaitRedirect(res,req)});
    }
});
  //awaitFunc(res)
});

async function awaitFunc(req,res) {
  console.log(1);
  await sleep(3000,req,res); // Promise が返ってくるまで awaitで 処理停止
  console.log(2); // 約3秒経過に表示
}
async function awaitRedirect(res,req) {
  console.log(3);
  await redirects(4000,res,req); // Promise が返ってくるまで awaitで 処理停止
  console.log(4); // 約3秒経過に表示
}

function getUniqueStr(myStrong){
  var file = fs.readdirSync('./images/share_image');
  var n_large = null;
  for (let i = 1; i < file.length; i++){
    var n = file[i].slice(13,-4);
    n = Number(n);
    if (n_large < n ){
      n_large = n
    }
  }
  n_large = n_large+1;
  var file_name = "make_T_shirt_" + String(n_large) ;
 return file_name
}

app.listen(443);
