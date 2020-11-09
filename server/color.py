from PIL import Image
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
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    H_hist = cv2.calcHist([hsv_image],[2],None,[256],[0,256]) 
#     plt.plot(hist_g_R,color = "r") #ヒストグラムをプロット
    #   plt.show() #プロットを表示

    S_hist = cv2.calcHist([hsv_image],[1],None,[256],[0,256]) 
#     plt.plot(hist_g_G,color = "g") #ヒストグラムをプロット
    #   plt.show() #プロットを表示

    V_hist = cv2.calcHist([hsv_image],[0],None,[256],[0,256])
#     plt.plot(hist_g_B,color = "b") #ヒストグラムをプロット
    plt.show() #プロットを表示

    return H_hist, S_hist, V_hist, label

def Similar_Search (H_histr, S_histr, V_histr, label):
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
            H_hist = cv2.compareHist(H_histr, row[3], 1) #ヒストグラムの比較。比較methodにcv2.HISTCMP_CORRELを使用
            #         print(comp_hist_R) #類似度を表示
            S_hist = cv2.compareHist(S_histr, row[4], 1)
#             #         print(comp_hist_G)
            V_hist = cv2.compareHist(V_histr, row[5], 1)
#             #         print(comp_hist_B)

            comp_hist_sum = H_hist + S_hist + V_hist
#             print(comp_hist_sum)
            lis = [comp_hist_sum, row[2]]
            comp_2_list.append(lis)
#             print(comp_2_list)

            comp_hist_list.append(comp_hist_sum)
            list.sort(comp_hist_list, reverse=True)
#             print(comp_hist_list )

    comp_choce.append(comp_hist_list[0])
    comp_choce.append(comp_hist_list[1])
    print(comp_choce)

    for i in comp_choce:
        for j in comp_2_list:
            if i == j[0]:
                url.append(j[1])

    print(url[0])
    print(url[1])

    for image in url:
        img = mpimg.imread(image)
        plt.figure()
        plt.imshow(img)
        #plt.show()

    con.close()
    
def main():
  image = "images/downloads/image.png" # もらってきた画像
  label = "T_shirt" # 検索するラベル

  H_hist, S_hist, V_hist, label = color_histogram(image,label)
  Similar_Search(H_hist, S_hist, V_hist, label)

main()
