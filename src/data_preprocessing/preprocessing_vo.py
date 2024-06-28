import numpy as np
import pandas as pd
import sys, os, glob

def cut_data(df, num_cols:int):
    """
    Cuts all except first n = num_cols columns
    """
    return df[df.columns[:num_cols]]


def reduce_dot(df, column_name:str):
    """
   In column_name changes str data in format like 12.345 into 12345 of int dtype
    """
    df[column_name] = df[column_name].str.replace('.', '').astype(int)
    return df


def upload_files(dir:str) -> list[str, str]:
    """
    Retruns name of file with ground truth (data.csv) and of file with estimated trajectory (.txt)
    """
    files = os.listdir(dir)
    csv_files = [fn for fn in files if fn.endswith(".csv")]
    txt_files = [fn for fn in files if fn.endswith(".txt")]
    if len(txt_files) > 1 or len(csv_files) > 1:
        raise ValueError
    return csv_files[0], txt_files[0]


def process_gt_df(df, save_path:str) -> None:   
    """
    Rm odd data and keep only 8 first columns (like needed for TUM files)
    """
    tum_df = cut_data(df, 8) # keep only first 8 cols like in tum format.
    tum_df.to_csv(save_path, sep=',', index=False)
    print("Processed Ground_Truth")


def process_traj_df(df, save_path:str) -> None:
    """
    Process file with trajectory estimation and keep in needed for evo_rpe format style.
    """
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

    ground_truth_df, traj_df = pd.read_csv(ground_truth_path, sep=','), pd.read_csv(traj_path, sep=' ', header=None, dtype=str) # loading all the data
    
    process_gt_df(ground_truth_df, os.path.join(DATA_DIR, f"evo/{ground_truth_filename}.txt")) # processing and saving ground truth file
    process_traj_df(traj_df, os.path.join(DATA_DIR, f"evo/{traj_filename}.txt")) # processing and saving traj.txt file
