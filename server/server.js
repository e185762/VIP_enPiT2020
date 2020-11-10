var express = require('express');
var bodyParser = require('body-parser')
var fs = require('fs');
var app = express();
const router = require('express-promise-router')();

var {PythonShell} = require('python-shell');

app.set("view engine", "ejs");

const multer  = require('multer');
let execSync = require('child_process').execSync;
const path = require("path");

var cloth_result=null;

const sleep = (millis) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            PythonShell.run('color.py', null, function (err, data) {
                console.log(data);
                console.log('finished');
                cloth_result=data[1];
                console.log(cloth_result);
                cloth_result=cloth_result.substring(5);
                console.log(cloth_result);
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
    res.render("result",{file:cloth_result});
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

    // PythonShell.run('color.py', null, function (err, data) {
    //     console.log(data);
    //     console.log('finished');
    //     cloth_result=data[1];
    //     console.log(cloth_result);
    //     cloth_result=cloth_result.substring(5);
    //     console.log(cloth_result);
    // });



  //console.log("遷移するはずやねんな");
  //res.render("index",{file:cloth_result});

  // res.redirect(307,'/result');
});

app.get('/analysis', (req, res, next) => {
    awaitFunc(res).then(() => {awaitRedirect(res)});
    //awaitFunc(res)
});

async function awaitFunc(res) {
    console.log(1);
    await sleep(1000); // Promise が返ってくるまで awaitで 処理停止
    console.log(2); // 約3秒経過に表示
}
async function awaitRedirect(res) {
    console.log(3);
    await redirects(2000,res); // Promise が返ってくるまで awaitで 処理停止
    console.log(4); // 約3秒経過に表示
}


app.listen(443);

