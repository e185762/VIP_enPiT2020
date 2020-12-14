import sqlite3
import numpy as np
import io
import cv2
import matplotlib.pyplot as plt
import sys

def access_db ():
    sqlite3.register_adapter(list, lambda l: ';'.join([str(i) for i in l]))
    sqlite3.register_converter('List', lambda s: [item.decode('utf-8')  for item in s.split(bytes(b';'))])
    sqlite3.register_adapter(bool, lambda b: str(b))
    sqlite3.register_converter('Bool', lambda l: bool(eval(l)))

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

    con = sqlite3.connect( 'DFS.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()
#   cur.execute("create table IMAGE (id,label,URL,Red_histr array ,Green_histr array ,Blue_histr array)")

    return con, cur

def color_divide(blue,green,red):
    if(blue <= 50 and green <= 50 and red <= 50 ):
#         print("黒")
        return "黒"
    elif(blue >= 230 and green >= 230 and red >= 230 ):
#         print("白")
        return "白"
    else:
        if(red == blue and red == green):
#             print("判別できない")
            return None
        else:
            if (red >= green and red >= blue):
                if (green >= blue):
                    distance = red - blue
                    dis_3_1 = round(distance * 0.333) + blue
                    dis_3_2 = round(distance * 0.666) + blue
                    if (green < dis_3_1):
#                         print("赤")
                        return "赤"
                    elif (dis_3_1 <= green <= dis_3_2):
#                         print("オレンジ")
                        return "オレンジ"
                    elif (dis_3_2 < green):
#                         print("黄色")
                        return "黄色"
                elif (green < blue):
                        distance = red - green
                        dis_3_1 = round(distance * 0.333) + green
                        dis_3_2 = round(distance * 0.666) + green
                        if (blue < dis_3_1):
#                             print("赤")
                            return "赤"
                        elif (dis_3_1 < blue < dis_3_2):
#                             print("ピンク")
                            return "ピンク"
                        elif (dis_3_2 < blue):
#                             print("紫")
                            return "紫"
            elif (blue >= green and blue >= red):
                if (red >= green):
                    distance = blue - green
                    dis_3_1 = round(distance * 0.333) + green
                    dis_3_2 = round(distance * 0.666) + green
                    if (red < dis_3_1):
#                         print("青")
                        return "青"
                    elif (dis_3_1 <= red <= dis_3_2):
#                         print("紫")
                        return "紫"
                    elif (dis_3_2 < red):
#                         print("ピンク")
                        return "ピンク"
                elif (red < blue):
                        distance = blue - red
                        dis_3_1 = round(distance * 0.333) + red
                        dis_3_2 = round(distance * 0.666) + red
                        if (green < dis_3_1):
#                             print("青")
                            return "青"
                        elif (dis_3_1 < green < dis_3_2):
#                             print("青")
                            return "青"
                        elif (dis_3_2 < green):
#                             print("水色")
                            return "水色"
            elif (green >= red and green >= blue):
                if (red >= blue):
                    distance = green - blue
                    dis_3_1 = round(distance * 0.333) + blue
                    dis_3_2 = round(distance * 0.666) + blue
                    if (red < dis_3_1):
#                         print("緑")
                        return "緑"
                    elif (dis_3_1 <= red <= dis_3_2):
#                         print("緑")
                        return "緑"
                    elif (dis_3_2 < red):
#                         print("黄色")
                        return "黄色"
                elif (red < blue):
                        distance = green - red
                        dis_3_1 = round(distance * 0.333) + red
                        dis_3_2 = round(distance * 0.666) + red
                        if (blue < dis_3_1):
#                             print("緑")
                            return "緑"
                        elif (dis_3_1 < blue < dis_3_2):
#                             print("緑")
                            return "緑"
                        elif (dis_3_2 < blue):
#                             print("水色")
                            return "水色"

def color_search(IMAGE):
    xy_canvas = []
    y = 180
    while(180 <= y < 455):
        x = 195
        while(195 <= x < 435):
            x += 8
            xy_canvas.append([x,y])
        y += 7

    image = IMAGE
    img = cv2.imread(image) #画つ目の像を読み出しオブジェクトimg_1に代入

    #画像の表示
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える
#     plt.show()

    RGB = []
    color_list = []

    for i in xy_canvas:
        x = i[0]
        y = i[1]
        rgb = img[y,x]
        RGB.append(rgb)

    for i in RGB:
        blue = i[0]
        green = i[1]
        red = i[2]
        color_str = color_divide(blue,green,red)
        color_list.append(color_str)

    return color_list

def Similar_Search(color_list):
    con,cur = access_db()

    URL_LIST = []
    cur.execute("SELECT * FROM IMAGE")
    rows = cur.fetchall()
    for row in rows:
        similar_num = 0
        color_s = row[4]
        URL = row[2]
        PATH = row[3]

        for i in range(len(color_list)):
            if (color_list[i] == color_s[i]):
                similar_num += 1
            else:
                similar_num = similar_num

        similar_parcent = similar_num/len(color_list) * 100

        if(similar_parcent >= 60):
            URL_LIST.append([similar_parcent,URL,PATH])

        URL_LIST.sort(reverse=True)

    for i in URL_LIST:
        image = i[2]
        img = cv2.imread(image) #画つ目の像を読み出しオブジェクトimg_1に代入
        #画像の表示
        # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # OpenCV は色がGBR順なのでRGB順に並べ替える
#         plt.show()

    # print(URL_LIST)
    for i in URL_LIST:
        print(i[2])
        print(i[1])

IMAGE = input()
color_hist = color_search(IMAGE)
Similar_Search(color_hist)
