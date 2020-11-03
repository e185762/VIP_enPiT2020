var express = require('express');
var bodyParser = require('body-parser')
var app = express();
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.static('images'))
app.use(bodyParser.json());
app.get('/', function (req, res) {
    res.sendfile('index.html');
});
// app.use('/receive', 'routes/receive.php')

app.post('/download', (req, res) => {
  // クライアントからの送信データを取得する
  let data = req.body;
  // let todoData = JSON.parse(data);
  
  console.log(data);
});

app.listen(443)

