import numpy as np
import pandas as pd

def cut_data(df, num_cols:int):
    """
    Обрезает df до количества столбцов равного num_cols
    """
    return df[df.columns[:num_cols]]

if __name__ == '__main__':
    df = pd.read_csv('./data.csv', sep=',') # Ground-truth дата

    tum_df = cut_data(df, 8) # приводим gt к tum  формату, оставляя только 8 первых столбцов
    tum_df.to_csv('./MH_02_medium_gt.txt', sep=',', index=False)  # сохраняем tum данные