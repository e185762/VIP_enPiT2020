var express = require('express');
var app = express();
var {PythonShell} = require('python-shell');

app.set("view engine", "ejs");

var cloth_import=[];
var cloth_result=[];

PythonShell.run('color.py', null, function (err, data) {
  if (err) throw err;
    cloth_import=data[4];
    cloth_result=data[5];
    console.log(cloth_import);
    console.log(cloth_result)
    console.log(data[4]);
    console.log('finished');
});
app.use(express.static('images'))
app.use(express.static('image'))

app.get('/', function (req, res) {
    //res.sendfile('index.html');
    res.render("test",{file:cloth_import});
});

app.get('/result', function (req, res) {
    //res.sendfile(cloth_import);
    res.render("./views/test.ejs",{file,cloth_import});
});

app.listen(8080)

//function previewFile(file) {
  // プレビュー画像を追加する要素
//  const preview = document.getElementById('preview');

  // FileReaderオブジェクトを作成
//  const reader = new FileReader();

  // URLとして読み込まれたときに実行する処理
//  reader.onload = function (e) {
//    const imageUrl = e.target.result; // URLはevent.target.resultで呼び出せる
//    const img = document.createElement("img"); // img要素を作成
//    img.src = imageUrl; // URLをimg要素にセット
//    preview.appendChild(img); // #previewの中に追加
//  }

  // いざファイルをURLとして読み込む
//  reader.readAsDataURL(file);
//}

// <input>でファイルが選択されたときの処理
//<no-ssr>
//    <vue-tags-input
//      v-model="tag"
//      :tags="tags"
//      @tags-changed="newTags => tags = newTags"
//    />
//const fileInput = document.getElementById('sample');
//const handleFileSelect = () => {
  //const files = fileInput.files;
  //for (let i = 0; i < files.length; i++) {
    //previewFile(files[i]);
  //}
//}
//fileInput.addEventListener('change', handleFileSelect);
//</no-ssr>
