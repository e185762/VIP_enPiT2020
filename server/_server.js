// httpモジュールの読み込み
var http = require('http');
var html = require('fs').readFileSync('index.html');
//var filedata = require('fs').readdirSync('./images');


// httpサーバの作成
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end(html);
}).listen(443); // ポート443番でコネクションの受け入れを行う
// 実行時、コンソールに表示されるメッセージ
console.log('Server running at http://13.113.194.238:443/');
