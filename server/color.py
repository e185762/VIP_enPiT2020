# from flask import Flask, render_template, jsonify
# import test
#
# app = Flask(__name__)
#
# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == "POST":
#         def access_db ():
#             import sqlite3
#             import numpy as np
#             import io
#
#             def adapt_array(arr):
#                 """
#                 http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
#                 """
#                 out = io.BytesIO()
#                 np.save(out, arr)
#                 out.seek(0)
#                 return sqlite3.Binary(out.read())
#             def convert_array(text):
#                 out = io.BytesIO(text)
#                 out.seek(0)
#                 return np.load(out)
#
#                 # Converts np.array to TEXT when inserting
#             sqlite3.register_adapter(np.ndarray, adapt_array)
#
#             # Converts TEXT to np.array when selecting
#             sqlite3.register_converter("array", convert_array)
#
#             con = sqlite3.connect( "sample.db", detect_types=sqlite3.PARSE_DECLTYPES)
#             cur = con.cursor()
#
#             return con, cur
#
#         def color_histogram(image,label):
#             """
#             画像のヒストグラムのデータ量を取得する
#
#             Parameters
#             ----------
#             image : str
#             検索したい画像のurl (なのかな？今回はlocalにある画像を使用しているよ)
#             label : str
#             検索したい画像のlabel　(ここではなんも処理してないから変えたほうがいいかも)
#             Returns
#             -------
#             hist_g_R : numpy.array
#             赤色のヒストグラムのデータ量
#             hist_g_G : numpy.array
#             緑色のヒストグラムのデータ量
#             hist_g_B : numpy.array
#             青色のヒストグラムのデータ量
#             label : str
#             検索したい画像のlabel
#             """
#
#
#             import cv2  #OpenCVのインポート
#             import matplotlib.pyplot as plt #matplotlib.pyplotのインポート
#
#
#             fname = image #1つ目の画像ファイル名
#
#             img = cv2.imread(fname) #画つ目の像を読み出しオブジェクトimg_1に代入
#
#             hist_g_R = cv2.calcHist([img],[2],None,[256],[0,256]) #imgのR(赤)のヒストグラムを計算
#             plt.plot(hist_g_R,color = "r") #ヒストグラムをプロット
#             plt.show() #プロットを表示
#
#             hist_g_G = cv2.calcHist([img],[1],None,[256],[0,256]) #imgのG(緑)のヒストグラムを計算
#             plt.plot(hist_g_G,color = "g") #ヒストグラムをプロット
#             plt.show() #プロットを表示
#
#             hist_g_B = cv2.calcHist([img],[0],None,[256],[0,256]) #imgのB(青)のヒストグラムを計算
#             plt.plot(hist_g_B,color = "b") #ヒストグラムをプロット
#             plt.show() #プロットを表示
#
#             return hist_g_R, hist_g_G, hist_g_B, label
#
#         def Similar_Search (hist_g_R, hist_g_G, hist_g_B, label):
#             #コードが冗長になってて、ごめんなさい。見やすくします
#             """
#             似ている画像を表示する
#
#             Parameters
#             ----------
#             hist_g_R : numpy.array
#             対象画像の赤色ヒストグラムのデータ量
#             hist_g_G : numpy.array
#             対象画像の緑色ヒストグラムのデータ量
#             hist_g_B : numpy.array
#             対象画像の赤色ヒストグラムのデータ量
#             label : 対象データのlabel
#             """
#             import cv2  #OpenCVのインポート
#             import matplotlib.pyplot as plt #matplotlib.pyplotのインポート
#             import matplotlib.image as mpimg
#
#             con,cur = access_db()
#
#             url = []
#             comp_hist_list = []
#             comp_2_list = []
#             comp_choce = []
#
#             n = 0
#
#             sql = "select * from IMAGE"
#             cur.execute(sql)
#             for row in cur:
#                 if row[1] == label:
#                     comp_hist_R = cv2.compareHist(hist_g_R, row[3], cv2.HISTCMP_CORREL) #ヒストグラムの比較。比較methodにcv2.HISTCMP_CORRELを使用
#                     #         print(comp_hist_R) #類似度を表示
#                     comp_hist_G = cv2.compareHist(hist_g_G, row[4], cv2.HISTCMP_CORREL)
#                     #         print(comp_hist_G)
#                     comp_hist_B = cv2.compareHist(hist_g_B, row[5], cv2.HISTCMP_CORREL)
#                     #         print(comp_hist_B)
#
#                     comp_hist_sum = comp_hist_R + comp_hist_G + comp_hist_B
#                     #         print(comp_hist_sum)
#                     lis = [comp_hist_sum, row[2]]
#                     comp_2_list.append(lis)
#                     #         print(comp_2_list)
#
#                     comp_hist_list.append(comp_hist_sum)
#                     list.sort(comp_hist_list, reverse=True)
#                     print(comp_hist_list )
#
#                     comp_choce.append(comp_hist_list[0])
#                     comp_choce.append(comp_hist_list[1])
#                     # print(comp_choce)
#
#                     for i in comp_2_list:
#                         for j in comp_choce:
#                             if i[0] == j:
#                                 url.append(i[1])
#
#                     print(url)
#
#                     for image in url:
#                         img = mpimg.imread(image)
#                         plt.figure()
#                         plt.imshow(img)
#                         plt.show()
#
#             con.close()
#
#         def main():
#             image = "image/T_shirt/T_shirt_01.jpg" # もらってきた画像
#             label = "T_shirt" # 検索するラベル
#
#             hist_R,hist_G,hist_B,label = color_histogram(image,label)
#             Similar_Search(hist_R,hist_G,hist_B,label)
#
#         main()
#
#
#     return render_template('index.html')

def access_db ():
  import sqlite3
  import numpy as np
  import io

  def adapt_array(arr):
     """
     http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
     """
     out = io.BytesIO()
     np.save(out, arr)
     out.seek(0)
     return sqlite3.Binary(out.read())
  def convert_array(text):
      out = io.BytesIO(text)
      out.seek(0)
      return np.load(out)

# Converts np.array to TEXT when inserting
  sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
  sqlite3.register_converter("array", convert_array)

  con = sqlite3.connect( "sample.db", detect_types=sqlite3.PARSE_DECLTYPES)
  cur = con.cursor()

  return con, cur

def color_histogram(image,label):
  """
    画像のヒストグラムのデータ量を取得する

    Parameters
    ----------
    image : str
        検索したい画像のurl (なのかな？今回はlocalにある画像を使用しているよ)
    label : str
        検索したい画像のlabel　(ここではなんも処理してないから変えたほうがいいかも)
    Returns
    -------
    hist_g_R : numpy.array
        赤色のヒストグラムのデータ量
    hist_g_G : numpy.array
        緑色のヒストグラムのデータ量
    hist_g_B : numpy.array
        青色のヒストグラムのデータ量
    label : str
        検索したい画像のlabel
  """


  import cv2  #OpenCVのインポート
  import matplotlib.pyplot as plt #matplotlib.pyplotのインポート


  fname = image #1つ目の画像ファイル名

  img = cv2.imread(fname) #画つ目の像を読み出しオブジェクトimg_1に代入

  hist_g_R = cv2.calcHist([img],[2],None,[256],[0,256]) #imgのR(赤)のヒストグラムを計算
  plt.plot(hist_g_R,color = "r") #ヒストグラムをプロット
  #plt.show() #プロットを表示

  hist_g_G = cv2.calcHist([img],[1],None,[256],[0,256]) #imgのG(緑)のヒストグラムを計算
  plt.plot(hist_g_G,color = "g") #ヒストグラムをプロット
  #plt.show() #プロットを表示

  hist_g_B = cv2.calcHist([img],[0],None,[256],[0,256]) #imgのB(青)のヒストグラムを計算
  plt.plot(hist_g_B,color = "b") #ヒストグラムをプロット
  #plt.show() #プロットを表示

  return hist_g_R, hist_g_G, hist_g_B, label

def Similar_Search (hist_g_R, hist_g_G, hist_g_B, label):
  #コードが冗長になってて、ごめんなさい。見やすくします
  """
    似ている画像を表示する

    Parameters
    ----------
    hist_g_R : numpy.array
        対象画像の赤色ヒストグラムのデータ量
    hist_g_G : numpy.array
        対象画像の緑色ヒストグラムのデータ量
    hist_g_B : numpy.array
        対象画像の赤色ヒストグラムのデータ量
    label : 対象データのlabel
  """
  import cv2  #OpenCVのインポート
  import matplotlib.pyplot as plt #matplotlib.pyplotのインポート
  import matplotlib.image as mpimg

  con,cur = access_db()

  url = []
  comp_hist_list = []
  comp_2_list = []
  comp_choce = []

  n = 0

  sql = "select * from IMAGE"
  cur.execute(sql)
  for row in cur:
      if row[1] == label:
          comp_hist_R = cv2.compareHist(hist_g_R, row[3], cv2.HISTCMP_CORREL) #ヒストグラムの比較。比較methodにcv2.HISTCMP_CORRELを使用
  #         print(comp_hist_R) #類似度を表示
          comp_hist_G = cv2.compareHist(hist_g_G, row[4], cv2.HISTCMP_CORREL)
  #         print(comp_hist_G)
          comp_hist_B = cv2.compareHist(hist_g_B, row[5], cv2.HISTCMP_CORREL)
  #         print(comp_hist_B)

          comp_hist_sum = comp_hist_R + comp_hist_G + comp_hist_B
  #         print(comp_hist_sum)
          lis = [comp_hist_sum, row[2]]
          comp_2_list.append(lis)
  #         print(comp_2_list)

          comp_hist_list.append(comp_hist_sum)
          list.sort(comp_hist_list, reverse=True)
          print(comp_hist_list )

  comp_choce.append(comp_hist_list[0])
  comp_choce.append(comp_hist_list[1])
  # print(comp_choce)

  for i in comp_2_list:
      for j in comp_choce:
          if i[0] == j:
              url.append(i[1])

  most = url[0]
  print(most[5:])
  print(url[1])

  for image in url:
    img = mpimg.imread(image)
    plt.figure()
    plt.imshow(img)
    #plt.show()

  con.close()

def main():
  image = "images/downloads/image.png"
  print("/downloads/image.png")
  #image = "image/T_shirt/T_shirt_01.jpg" # もらってきた画像
  label = "T_shirt" # 検索するラベル

  hist_R,hist_G,hist_B,label = color_histogram(image,label)
  Similar_Search(hist_R,hist_G,hist_B,label)


main()
