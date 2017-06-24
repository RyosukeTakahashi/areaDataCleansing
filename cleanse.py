#  配車IDXX　配車　1600
# の行を見つけてXXを取得
# そこから、
# XX　確認or走行開始
# XX　走行完了
# までの行を抽出。
# 抽出した行でCSVを作成し、XYデータを作成（チリ座標注意）
# 可能なら確認～走行完了が何時の便かデータを足す。
# シンボルをあてる。

import os
import pandas as pd


TIME = 1600
narashi = []

def generate_csv(time, csv_path):

    df = pd.read_csv(csv_path, encoding='SJIS')
    df_time = df.loc[(df["配車操作"] == "配車") & (df["運行時刻"] == time), "配車ID"]

    haisha_indices = list(df_time.index)
    haisha_ids = list(df_time.values.flatten())

    endrun_indices = [get_index_of_endrun_from_haishaId(df, id) for id in haisha_ids]

    dfs = [df[haisha_index:end_index+1] for haisha_index, end_index in zip(haisha_indices, endrun_indices)]

    jousha_counts = []
    for carId in dfs:

        jousha_counts.append(carId[carId["予約操作"] == "乗車"].count()["車両"])

    maxCount = max(jousha_counts)
    minCount = min(jousha_counts)



    if maxCount - minCount <= 1:
        print(csv_path)
        print(jousha_counts)
        narashi.append(csv_path)



    # output_df = pd.concat(dfs)
    #
    # path_temp = csv_path.replace('pathData', 'pathDataCleansed')
    # path = path_temp.replace('緯度経度', '緯度経度_Cleansed')
    #
    # output_df.to_csv(path, encoding='SJIS')


def get_index_of_endrun_from_haishaId(df, id):

    df_end = df.loc[(df["配車ID"] == id) & (df["配車操作"] == "走行完了")]
    return df_end.index.values.flatten()[0]


months = os.listdir('./pathData')

for month in months:

    days = os.listdir('./pathData/{}'.format(month))

    for day in days:
        path = './pathData/{}/{}'.format(month, day)
        generate_csv(TIME, path)




print(len(narashi))