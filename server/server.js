var express = require('express');
var bodyParser = require('body-parser')
var fs = require('fs');
var app = express();
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.static('images'));
app.use(bodyParser.json());
app.get('/', function (req, res) {
    res.sendfile('index.html');
});
// app.use('/receive', 'routes/receive.php')

app.post('/download', (req, res) => {
  // クライアントからの送信データを取得する
  let body = req.body;
  let parse = JSON.parse(JSON.stringify(body));

// fs.writeFile("./image.png", parse.data, function(err) {
//   if (err) throw err;
// });
});

app.listen(443);

