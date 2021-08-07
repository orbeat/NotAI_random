drop table NotAI_Random_game3 cascade constraint purge;
drop sequence NotAI_Random_game3_seq;

drop table NotAI_Random_Control3 cascade constraint purge;
drop sequence NotAI_Random_Control3_seq;


create table NotAI_Random_game3(
	nrg_no number(10) primary key,
	nrg_start_time date not null,			-- 게임 시작 시간
	nrg_start_clock number(13,4) not null,	-- 게임 시작 클럭
	nrg_end_time date not null,				-- 게임 종료 시간
	nrg_end_clock number(13,4) not null		-- 게임 종료 클럭
);
create sequence NotAI_Random_game3_seq;


create table NotAI_Random_Control3
(
	nrc_no number(13) primary key,
	nrc_start_clock number(13,4) not null,		-- 누르기 시작한 시간
	
	nrc_key_z number(1) not null,		-- z키를 눌렀으면 1, 아니면 0
	nrc_key_x number(1) not null,		-- x키를 눌렀으면 1, 아니면 0
	nrc_key_left number(1) not null,		-- left키를 눌렀으면 1, 아니면 0
	nrc_key_right number(1) not null,	-- right키를 눌렀으면 1, 아니면 0
	nrc_key_down number(1) not null,		-- down키를 눌렀으면 1, 아니면 0
	
	nrc_score number(6) not null,				-- 누르기 시작한 시간(캡쳐한 시각)의 점수
	nrc_level number(3) not null,				-- 누르기 시작한 시간(캡쳐한 시각)의 레벨
	nrc_line number(4) not null,					-- 누르기 시작한 시간(캡쳐한 시각)의 부순 줄 수
	nrc_next_block varchar(1 char),				-- 누르기 시작한 시간(캡쳐한 시각)의 다음 블럭
	nrc_nrg_no number(10) not null,				-- 해당 게임의 번호
	constraint nrc_key3
		foreign key(nrc_nrg_no) references NotAI_Random_game3(nrg_no)
		on delete cascade
);
create sequence NotAI_Random_Control3_seq;

select * from NotAI_Random_game3;
select * from NotAI_Random_Control3;

-- 최근 1판 조회
select * from NotAI_Random_Control3
where nrc_nrg_no = (select max(nrg_no) from NotAI_Random_game3)
order by nrc_no;

select * from NotAI_Random_game3
where nrg_no = (select max(nrg_no) from NotAI_Random_game3);

select nrg_no, max(nrc_no)-min(nrc_no)+1, max(nrc_score), max(nrc_level), max(nrc_line) -- 게임 번호, 진행 프레임 수, 최종 점수, 최종 레벨, 최종 라인수
from NotAI_Random_game3, NotAI_Random_Control3
where nrg_no = nrc_nrg_no
group by nrg_no
order by nrg_no;

-- 최근 1판 삭제
delete from NotAI_Random_game3
where nrg_no = (select max(nrg_no) from NotAI_Random_game3);

-- 특정 게임 불러오기
select * from NotAI_Random_game3 where nrg_no = 29;

-- 특정 게임 정보 수정
update NotAI_Random_game3
set nrg_start_clock = 2844.1227	--2844.1228에서 2844.1227로 바뀜
where nrg_no = 29;

-- 조작키(z,x,left,right,down)별 사용 횟수