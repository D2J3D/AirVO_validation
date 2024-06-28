import numpy as np
import pandas as pd
import sys, os, glob

def cut_data(df, num_cols:int):
    """
    Обрезает df до количества столбцов равного num_cols
    """
    return df[df.columns[:num_cols]]


def reduce_dot(df, column_name:str):
    """
    В столбце column_name переводит строковые данные формата 12.345 в 12345 типа int
    """
    df[column_name] = df[column_name].str.replace('.', '').astype(int)
    return df


def upload_files(dir:str) -> list[str, str]:
    files = os.listdir(dir)
    csv_files = [fn for fn in files if fn.endswith(".csv")]
    txt_files = [fn for fn in files if fn.endswith(".txt")]
    if len(txt_files) > 1 or len(csv_files) > 1:
        raise ValueError
    return csv_files[0], txt_files[0]


def process_gt_df(df, save_path:str) -> None:   
    tum_df = cut_data(df, 8) # приводим gt к tum  формату, оставляя только 8 первых столбцов
    tum_df.to_csv(save_path, sep=',', index=False)  # сохраняем tum данные
    print("Processed Ground_Truth")

def process_traj_df(df, save_path:str) -> None:
    df.iloc[:, 1:] = df.iloc[:, 1:].map(lambda x: float(x))
    df[df.columns[0]] = df[df.columns[0]].str.replace('.', '').astype(int)
    df.to_csv(save_path, sep=',', index=False)
    print("Processed traj file")

if __name__ == '__main__':
    DATA_DIR = sys.argv[1] # dir with Gt.csv and traj.txt
    ground_truth, traj = upload_files(DATA_DIR) # get filenames of ground-thruth.csv and trajectory.txt
    ground_truth_path, traj_path = os.path.join(DATA_DIR, ground_truth), os.path.join(DATA_DIR, traj) #make full paths
    ground_truth_filename, traj_filename = os.path.splitext(ground_truth)[0], os.path.splitext(traj)[0]
    # check that pathes are correct
    assert os.path.isfile(ground_truth_path)
    assert os.path.isfile(traj_path)

    # make new dir for files in EVO formats
    try:
        os.mkdir(os.path.join(DATA_DIR, 'evo'))
    except:
        print("EVO dir already exists.")

    ground_truth_df, traj_df = pd.read_csv(ground_truth_path, sep=','), pd.read_csv(traj_path, sep=' ', header=None, dtype=str)
    
    process_gt_df(ground_truth_df, os.path.join(DATA_DIR, f"evo/{ground_truth_filename}.txt"))
    process_traj_df(traj_df, os.path.join(DATA_DIR, f"evo/{traj_filename}.txt"))
