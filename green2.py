import cv2
import glob
import pandas as pd
import numpy as np

# 上限は固定
green_upper = np.array([90, 255, 255])

def nothing(x):
    pass

# ウィンドウ設定
def window(width, height):
    # 画像がウィンドウ内に収まるようにリサイズ
    cv2.namedWindow("original", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("original", width, height)
    cv2.namedWindow("img_binary", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("img_binary", width, height)
    # トラックバーの設定
    cv2.createTrackbar('Green', 'img_binary', 0, 89, nothing)


def main(folder_path, output_file_name):
    # Trueだと実行
    do = True
    # 全画像のリスト
    path_list = glob.glob(f"{folder_path}/**/*.jpg", recursive=True)
    # データフレーム作成
    df = pd.DataFrame(columns=["image_name", "green(%)"])

    for path in path_list:
        if do:
            path = path.replace('\\', '/')
            # オリジナル画像
            img = cv2.imread(path)
            # 見やすくするためにサイズを変更
            height = img.shape[0] // 5
            width = img.shape[1] // 5
            window(width, height)
            while True:
                # 画像を表示
                cv2.imshow("original", img)
                if cv2.waitKey(1) == 27 & 0xFF:
                    # 「do」がFalseになるから終了
                    do = False
                    break
                # グレー画像
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # トラックバーから値を取得
                green_lower = cv2.getTrackbarPos('Green', 'img_binary')
                # 緑の下限を設定
                green_min = np.array([green_lower, 0, 0])
                # hsvに変換
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                # minからmaxの範囲を抽出。それ以外は0(黒)にする
                frame_mask = cv2.inRange(hsv, green_min, green_upper)
                # マスクを適用
                dst = cv2.bitwise_and(gray, frame_mask)
                cv2.imshow("img_binary", dst)
                if cv2.waitKey(1) == ord("s") & 0xFF:
                    # 黒でない部分を求める
                    not_black_area = cv2.countNonZero(dst)
                    # 画像のサイズを取得
                    whole_area = gray.size
                    # 緑の部分の割合 = 黒でない部分　÷　全体のサイズ
                    green_percent = round(
                        (not_black_area / whole_area) * 100, 2)
                    # csvファイルに書き込み
                    df = df.append(
                        {'image_name': path, 'green(%)': green_percent}, ignore_index=True)
                    df.to_csv(output_file_name, index=False)
                    print(f"{path} : {green_percent}%")
                    break
            cv2.destroyAllWindows()
        else:
            break
