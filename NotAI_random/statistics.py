import os
from time import perf_counter as clock
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np

fontFile = 'C:/Windows/Fonts/malgun.ttf'
fontName = fm.FontProperties(fname=fontFile, size=50).get_name()
plt.rc('font', family=fontName)

def get_file_names(targetdir):
    try:
        files = os.listdir(targetdir)
        # print(files)
        return files
    except Exception as e:
        print(e)
        return False

def lastest_save_file_name(file_names):
    if file_names:
        save_time_li = []
        t = 0
        for i in file_names:
            if 'db2csv_pretreatment' in i:
                t = int(i[-19:-11]+i[-10:-4])
                # print(t, type(t))
                save_time_li.append(t)
    lastest_save_time = str(max(save_time_li))
    return r'\db2csv_pretreatment_%s-%s.csv' % (lastest_save_time[:8], lastest_save_time[8:])

def load_csv(targetdir):
    files = get_file_names(targetdir)
    file = lastest_save_file_name(files)
    file_dir = targetdir + file
    
    df = pd.read_csv(file_dir,
                     names=['game_no', 'save_clock', 'z', 'x', 'left', 'right', 'down', 'score', 'level', 'line', 'next_piece'])
    
    return df

def current_avg(score_np, n=100):
    score_avg = score_np[n-1:].copy()
    for i in range(1, n):
        # print(score_np[:10])
        score_avg += score_np[n-i-1:-i]
    
    score_avg = score_avg / n
    return score_avg

if __name__=='__main__': 
    targetdir = r"C:\orbeat\NotAI\data/"
    refiend_data_df = load_csv(targetdir)
    refiend_data_df['control'] = refiend_data_df['z']*6 + refiend_data_df['x']*12 + refiend_data_df['left']*2 + refiend_data_df['right']*4 + refiend_data_df['down']
    # print(refiend_data_df.groupby(['z', 'x', 'left', 'right', 'down'])['game_no'].count()) # 조작키 분류(0~17)별 개수
    print(refiend_data_df.groupby('control')['game_no'].count()) # 조작키 분류(0~17)별 개수
    
    print(refiend_data_df[refiend_data_df['z']==1]['game_no'].count()) # z키를 누른 횟수
    print(refiend_data_df[refiend_data_df['x']==1]['game_no'].count()) # x키를 누른 횟수
    print(refiend_data_df[refiend_data_df['left']==1]['game_no'].count()) # left키를 누른 횟수
    print(refiend_data_df[refiend_data_df['right']==1]['game_no'].count()) # right키를 누른 횟수
    print(refiend_data_df[refiend_data_df['down']==1]['game_no'].count()) # down키를 누른 횟수
    
    print(refiend_data_df.groupby('next_piece')['game_no'].count()) # 블럭 종류별 비율
    # print(refiend_data_df['next_piece'].value_counts()) # 블럭 종류별 비율
    
    last_score_df = refiend_data_df.groupby('game_no')['score'].max() # 게임별 최대(최종) 점수
    print(last_score_df)
    score_np = last_score_df.to_numpy()
    print(np.max(score_np))
    
    last_line_df = refiend_data_df.groupby('game_no')['line'].max()
    line_np = last_line_df.to_numpy()
    sns.histplot(x=line_np, bins=np.max(line_np))#, kde=True)
    # sns.histplot(x=score_np, bins=int(np.max(score_np)/63)+1, kde=True)
    plt.show()
    print(score_np[:20])
    print(current_avg(score_np)[:20])
    
    # for i in current_avg(score_np, 1):
        # print(i)