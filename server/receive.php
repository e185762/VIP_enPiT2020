<?php
/**
 * DataURI Schemaを受け取り保存する
 *
 */

//-------------------------------------------------
// 定数
//-------------------------------------------------
// 画像を保存するディレクトリ
define('SAVE_DIR', 'images/');

//-------------------------------------------------
// POSTで渡されたJSONを取得
//-------------------------------------------------
$json = getParamJSON();

//-------------------------------------------------
// Validation
//-------------------------------------------------
// dataが渡されているか
if( ! isset($json['data']) ){
  sendResult(false, 'Empty query parameter: data');
  exit(1);
}
// データ長が30kbyte以下か
if( strlen($json['data']) > (1024 * 30) ){
  sendResult(false, 'Too long string: data');
  exit(1);
}
// 中身がDataURISchemaか
if( ! preg_match('/^data:image\/png;base64,/', $json['data']) ){
  sendResult(false, 'Not Allow data type: data');
  exit(1);
}

//-------------------------------------------------
// サーバへ保存
//-------------------------------------------------
// Base64をバイナリに戻す
$data = $json['data'];
$data = str_replace('data:image/png;base64,', '', $data);  // 冒頭の部分を削除
$data = str_replace(' ', '+', $data);  // 空白を'+'に変換
$image = base64_decode($data);

// ファイルへ保存
$file = sprintf('%s.png', uniqid());    //ファイル名を作成
$result = file_put_contents(SAVE_DIR.$file, $image, LOCK_EX);

//-------------------------------------------------
// 結果を返却
//-------------------------------------------------
if( $result !== false ){
  sendResult(true, $file);  // ブラウザにファイル名を返却する
}
else{
  // 書き込みエラー
  sendResult(false, 'Can not write image data');
}


/**
 * POSTで渡されたJSONを取得する
 *
 * @return object
 */
function getParamJSON(){
  $buff = file_get_contents('php://input');
  $json = json_decode($buff, true);

  return($json);
}

/**
 * 結果をJSON形式で返却
 *
 * @param  boolean $status 成功:true, 失敗:false
 * @param  mixed   $data   ブラウザに返却するデータ
 * @return void
 */
function sendResult($status, $data){
  // CORS (必要に応じて指定)
  header('Access-Control-Allow-Origin: *');
  header('Access-Control-Allow-Headers: *');

  echo json_encode([
    "status" => $status,
    "result" => $data
  ]);
}
