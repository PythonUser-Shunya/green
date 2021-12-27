# pyinstaller green_gui.py --onefile --noconsole -F --paths="C:\Users\shuny\anaconda3\envs\Open\Lib\site-packages\cv2"

import PySimpleGUI as sg
from green2 import main

sg.theme('DarkTeal7')

layout = [
    [sg.Text('「S」で値を取得。「Esc」で終了。')],
    [sg.Text('都度csvファイルが生成されます。フォルダの中にフォルダがあってもOK')],
    [sg.FolderBrowse("フォルダを選択"), sg.Input(key='inputFolderPath')],
    [sg.Text("出力されるcsvファイル名を↓に入力。例）〇〇.csv")],
    [sg.Input(key='outputFileName')],
    [sg.Button('実行', key='do')],
    [sg.Output(size=(70, 5), key="output")]
]

# ウィンドウの生成
window = sg.Window('Greeeeeeeeeeeeeeeeeeeeeeen', layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # ウィンドウのXボタンを押したときの処理
        break
    # イベントが「OK」ボタンを押したときの処理
    if event == "do":
        if ".csv" in values['outputFileName']:
            folder_path = values['inputFolderPath'] + "/"
            output_file_name = values['outputFileName']
            main(folder_path, output_file_name)
            print("保存が完了しました。")
        else:
            print("csvファイル名には「.csv」をつけてください。")

window.close()
