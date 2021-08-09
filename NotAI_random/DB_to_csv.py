# -*- coding:utf-8 -*-
from cx_Oracle import connect
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import PIL.Image as pilimg

import NotAI_random as nar
from time import sleep

class DB2csv:
    def __init__(self, db='choi', db_name='choi', ip='localhost'):
        self.db, self.db_name, self.ip = db, db_name, ip
    
    def db2csv_all(self):
        try:
            con = connect('%s/%s@%s:1521/xe' % (self.db, self.db_name, self.ip))  # db에 연결
            cur = con.cursor()
            
            sql = """
            select nrg_no, nrg_start_time, nrg_start_clock, nrg_end_time, nrg_end_clock
            from NotAI_Random_game3
            order by nrg_no
            """
            cur.execute(sql)
            
            try:
                now = datetime.strftime(datetime.today(), '%Y%m%d-%H%M%S')
                f = open(r'C:\orbeat\NotAI\data\NotAI_Random_game3_%s.csv' % now, 'a', encoding='utf-8')
            except Exception as e:
                print('파일 열기 실패 :', e)

            for nrg_no, nrg_start_time, nrg_start_clock, nrg_end_time, nrg_end_clock in cur:
                f.write("%d,%s,%.4f,%s,%.4f\n" % (nrg_no,
                                   datetime.strftime(nrg_start_time, '%Y%m%d-%H%M%S'),
                                   nrg_start_clock,
                                   datetime.strftime(nrg_end_time, '%Y%m%d-%H%M%S'),
                                   nrg_end_clock) )
                
            try:
                f.close()
            except Exception as e:
                print('파일 닫기 실패 :', e)
            
            ################################
            
            sql = """
            select *
            from NotAI_Random_Control3
            order by nrc_no
            """
            cur.execute(sql)
            
            try:
                now = datetime.strftime(datetime.today(), '%Y%m%d-%H%M%S')
                f = open(r'C:\orbeat\NotAI\data\NotAI_Random_Control3_%s.csv' % now, 'a', encoding='utf-8')
            except Exception as e:
                print('파일 열기 실패 :', e)

            for no, s_clock, z, x, l, r, d, sco, lev, lin, nb, game_no in cur:
                f.write("%d,%.4f,%s,%s,%s,%s,%s,%d,%d,%d,%s,%d\n" % (no,
                                                                   s_clock,
                                                                   z, x, l, r, d,
                                                                   sco, lev, lin, nb,
                                                                   game_no))
                
            try:
                f.close()
            except Exception as e:
                print('파일 닫기 실패 :', e)
            
        except Exception as e:
            print('DB불러오기 실패1', e)
        
        try:
            con.close()
        except Exception as e:
            print('DB연결 해제 실패', e)
    
    def score(self):
        try:
            con = connect('%s/%s@%s:1521/xe' % (self.db, self.db_name, self.ip))  # db에 연결
            cur = con.cursor()
            
            sql = """
            select nrg_no, max(nrc_no)-min(nrc_no)+1, max(nrc_score), max(nrc_level), max(nrc_line) -- 게임 번호, 진행 프레임 수, 최종 점수, 최종 레벨, 최종 라인수
            from NotAI_Random_game3, NotAI_Random_Control3
            where nrg_no = nrc_nrg_no
            group by nrg_no
            order by nrg_no
            """
            cur.execute(sql)
            
            try:
                now = datetime.strftime(datetime.today(), '%Y%m%d-%H%M%S')
                f = open(r'C:\orbeat\NotAI\data\score_%s.csv' % now, 'a', encoding='utf-8')
            except Exception as e:
                print('파일 열기 실패 :', e)
            
            a_score = 0
            for no, frame, score, level, line in cur:
                a_score += score
                f.write('%d,%d,%d,%d,%d,%d\n' % (no, frame, score, a_score, level, line) )
                
            try:
                f.close()
            except Exception as e:
                print('파일 닫기 실패 :', e)
                
                
            
            
        except Exception as e:
            print('DB불러오기 실패1', e)
        
        try:
            con.close()
        except Exception as e:
            print('DB연결 해제 실패', e)
            
    def db2csv_pretreatment(self, x1, y1, x2, y2):
        error_cnt = 0
        oper = nar.Operation()
        max_game_no = oper.current_game_no() # 가장 최근에 한 게임 번호를 받아옴
        try:
            con = connect('%s/%s@%s:1521/xe' % (self.db, self.db_name, self.ip))  # db에 연결
            cur = con.cursor()
            
            try:
                now = datetime.strftime(datetime.today(), '%Y%m%d-%H%M%S')
                f = open(r'C:\orbeat\NotAI\data\db2csv_pretreatment_%s.csv' % now, 'a', encoding='utf-8')
            except Exception as e:
                print('파일 열기 실패 :', e)
                return False
                
            game_info = {}
            _dir = ''
            imgs = []
            key_bool_li = []
            img_path = ''
            datas = []
            is_equal = None
            for i in range(1, max_game_no+1):
                sql = """
                select *
                from NotAI_Random_game3
                where nrg_no = %d
                """ % i
                # print(sql)
                cur.execute(sql)
                
                for j in cur:
                    game_info = {
                        'start_game_time':datetime.strftime(j[1], '%Y%m%d-%H%M%S'),
                        'start_game_clock':j[2],
                        'end_game_time':datetime.strftime(j[3], '%Y%m%d-%H%M%S'),
                        'end_game_clock':j[4]
                        }
                
                _dir = r'\orbeat\NotAI\data\img\%s_%.4f' % (game_info['start_game_time'], game_info['start_game_clock'])
                print(max_game_no, i, _dir)      
                
                sql = """
                select *
                from NotAI_Random_Control3
                where nrc_nrg_no = %d
                order by nrc_no
                """ % i
                cur.execute(sql)
                
                imgs = []
                datas = []
                for no, s_clock, z, x, l, r, d, sco, lev, lin, nb, game_no in cur:
                    key_bool_li = [z, x, l, r, d]
                    img_path = _dir + '\\%.4f_%s.png' % (s_clock, str(key_bool_li))
                    error_cnt = 0
                    while True:
                        try:
                            imgs.append(np.array(pilimg.open(img_path)))
                            break
                        except Exception as e:
                            print('이미지 불러오기 예외 :', e)
                            sleep(1)
                            error_cnt += 1
                            if error_cnt >= 3: return False
                    # cut_img2= cut_img
                    datas.append("%d,%.4f,%s,%s,%s,%s,%s,%d,%d,%d,%s\n" % (game_no,
                                                                       s_clock,
                                                                       z, x, l, r, d,
                                                                       sco, lev, lin, nb))
                    
                    # 이전 이미지와 같으면 해당 프레임의 데이터는 학습 데이터에 포함하지 않음
                    # if len(imgs) >= 1 and np.all(imgs[-1]==cut_img):
                        # plt.imshow(cut_img2)
                        # plt.show()
                        # continue
                       
                    # plt.imshow(cut_img2)
                    # plt.show() 
                    # imgs.append(cut_img)
                    # if len(imgs) <= 1: continue
                    # plt.imshow(cut_img2)
                    # plt.show() 
                        
                    # break
                
                if len(imgs) < 3: continue # 길이가 너무 짧으면 어차피 저장되는 데이터가 없음
                imgs = np.array(imgs)
                imgs = imgs[:, y1:y2 + 1, x1:x2 + 1,:]
                is_equal = imgs[1:,:,:,:]==imgs[:-1,:,:,:]
                is_equal = np.all(np.all(np.all(is_equal, axis=3), axis=2), axis=1)
                # print(is_equal)
                # exit()
                
                for j in range(1, len(datas)-15):
                    # print(j, len(datas))
                    if is_equal[j-1]:
                        # print(j, len(datas))
                        continue
                    f.write(datas[j])
                
            try:
                f.close()
            except Exception as e:
                print('파일 닫기 실패 :', e)
                error_cnt += 1
            
        except Exception as e:
            print('DB불러오기 실패1', e)
            error_cnt += 1
        
        try:
            con.close()
        except Exception as e:
            print('DB연결 해제 실패', e)
            error_cnt += 1
        
        if error_cnt==0: return True
        else: return False
    
to_csv = DB2csv()
# print(to_csv.db2csv_pretreatment(17, 26, 98, 169))
to_csv.db2csv_all()