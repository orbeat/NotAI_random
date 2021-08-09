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
    
    control_group_cnt = refiend_data_df.groupby('control')['game_no'].count().to_numpy()
    plt.title('조작키 번호별 누른 횟수')
    plt.xlabel('조작키 번호')
    plt.ylabel('조작 횟수')
    sns.barplot(x=list(range(len(control_group_cnt))), y=control_group_cnt, palette='Wistia')
    plt.show()
    
    # for i in ['Wistia']:#['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r']:
        # print(i)
        # sns.barplot(x=list(range(len(control_group_cnt))), y=control_group_cnt, palette=i)
        # plt.show()
    #####################################################
    key_cnt_li = []
    key_cnt_li.append(refiend_data_df[refiend_data_df['z']==1]['game_no'].count()) # z키를 누른 횟수
    key_cnt_li.append(refiend_data_df[refiend_data_df['x']==1]['game_no'].count()) # x키를 누른 횟수
    key_cnt_li.append(refiend_data_df[refiend_data_df['left']==1]['game_no'].count()) # left키를 누른 횟수
    key_cnt_li.append(refiend_data_df[refiend_data_df['right']==1]['game_no'].count()) # right키를 누른 횟수
    key_cnt_li.append(refiend_data_df[refiend_data_df['down']==1]['game_no'].count()) # down키를 누른 횟수
    print(key_cnt_li)
    
    plt.title('조작키별 누른 횟수')
    plt.xlabel('조작키')
    plt.ylabel('누른 횟수')
    sns.barplot(x=['z', 'x', 'left', 'right', 'down'], y=key_cnt_li, palette='Wistia')
    plt.show()
    #####################################################
    block_group_cnt = refiend_data_df.groupby('next_piece')['game_no'].count() # 블럭 종류별 비율
    # print(block_group_cnt, block_group_cnt.filter(regex='|'.join(['I','J','L','O','S','T','Z'])))
    # print(refiend_data_df['next_piece'].value_counts()) # 블럭 종류별 비율
    
    plt.title('블럭 종류별 등장 횟수')
    plt.xlabel('블럭 종류')
    plt.ylabel('등장 횟수')
    # sns.barplot(data=block_group_cnt, x=block_group_cnt.loc, palette='Wistia')
    sns.barplot(x=['I','J','L','O','S','T','Z'], y=block_group_cnt.to_numpy(), palette='Wistia')
    plt.show()
    #####################################################
    
    last_score_df = refiend_data_df.groupby('game_no')['score'].max() # 게임별 최대(최종) 점수
    print(last_score_df)
    score_np = last_score_df.to_numpy()
    print(np.max(score_np))
    
    last_line_df = refiend_data_df.groupby('game_no')['line'].max()
    line_np = last_line_df.to_numpy()
    # print(last_line_df.count())
    sns.histplot(x=line_np, bins=np.max(line_np), palette='asdfafd')#, kde=True)
    # sns.histplot(x=score_np, bins=int(np.max(score_np)/63)+1, kde=True)
    plt.title('랜덤 조작 통계')
    plt.xlabel('부순 줄의 개수')
    plt.ylabel('게임 수')
    plt.xticks(np.array(range(np.max(line_np))))
    plt.show()
    print(score_np[:20])
    print(current_avg(score_np)[:20])
    
    # for i in current_avg(score_np, 1):
        # print(i)