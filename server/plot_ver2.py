
''' 
# Google colab用コード
!pip install japanize_matplotlib
from google.colab import drive
import pandas as pd
import os
import matplotlib.pyplot as plt
import japanize_matplotlib # 日本語表示のために必要
import io
import base64

mount_path = '/content/drive/'
if not os.path.ismount(mount_path):
    drive.mount(mount_path)

path_csv = os.path.join(mount_path, 'MyDrive', 'answers.csv')
'''


# server 実行用コード
import pandas as pd
import os
import matplotlib.pyplot as plt
import io 
from datetime import datetime
import base64 
import japanize_matplotlib 
import random
import json

mount_path = './'
path_csv = os.path.join(mount_path,'answers.csv')

try:
    df_loaded = pd.read_csv(path_csv, encoding='utf-8-sig',index_col=False)
    df = pd.DataFrame(df_loaded)

    if 'needSupport' in df.columns:
        word_list = list(df["needSupport"].value_counts().index)
        #word_count = df["needSupport"].value_counts().values
        word_count = df["needSupport"].value_counts()
        desired_order = ['はい', 'いいえ']
        word_count = [word_count.get(label, 0) for label in desired_order] 
        word_list = desired_order
        plot_colors = ['red', 'blue']

        
        fig = plt.figure(figsize=(4,4))
        plt.pie(word_count, labels=word_list, autopct='%1.1f%%', startangle=90, counterclock=False, colors=plot_colors)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
        plt.title("result")
        plt.axis('equal')
        
        ## figの出力結果をエンコードする
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig) 
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')




        ## 転送するデータをまとめる
        data_to_return = {
        "message": "python load success",
        "nowTime": str(datetime.now()),
        "plotImage": image_base64
    }
        ## サーバーにjsonとしてデータ転送
        print(json.dumps(data_to_return))
       
    else:
        print(f"エラー: CSVファイルに  列が見つかりませんでした。利用可能な列は次のとおりです: {df.columns.tolist()}")

except FileNotFoundError:
    print(f"エラー: '{path_csv}' にCSVファイルが見つかりませんでした。パスを確認してください。")
except Exception as e:
    print(f"データの読み込みまたは処理中にエラーが発生しました: {e}")




