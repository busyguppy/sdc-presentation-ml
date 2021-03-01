
define year = '2017'

--整年借閱
drop table tmp_kk;
create table tmp_kk as
select wpinno, to_char(transt, 'YYYYMMDD') transt, receiver, viewtype
from wpborrow
;


drop table tmp_aa1;
create table tmp_aa1 as
select wpinno
from logtable
where to_char(transdatetime, 'YYYY') = '&year' and comments in ('紙本歸檔','電子檔歸檔')
;

--整年歸檔
drop table tmp_aa2;
create table tmp_aa2 as
select a.wpinno, substr(b.wpkind,1,1) wpkind1, b.wpkind, b.wptype
from tmp_aa1 a left join fpv.wprec@filescanfpv b
    on a.wpinno = b.wpinno
;

--各類公文歸檔數
drop table tmp_aa;
create table tmp_aa as
select wpkind1, count(*) cnt
from tmp_aa2
group by wpkind1
;


-- *** 掃描後曾被借閱比例 ***
with s1 as ( -- 掃描後曾被借閱公文數
    select count(*) cnt
    from barcodetable a
    where to_char(createtime, 'YYYY') = '&year' and exists (
        select ''
        from wpborrow b
        where a.barcodevalue = b.wpinno
    )
), s2 as ( -- 掃描公文數
    select count(*) cnt
    from barcodetable
    where to_char(createtime, 'YYYY') = '&year'
    
)
select a.cnt "掃描借閱數(紙本/電子)", b.cnt 掃描數, round((a.cnt/b.cnt),3)*100 百分比
from s1 a, s2 b
;

select * from barcodetable;

-- *** 借閱、掃描、歸檔數 ***
with s1 as (
    select barcodevalue, to_char(createtime, 'YYYY') createtime
    from barcodetable
    where to_char(createtime, 'YYYY') = '&year'
), s2 as ( --掃描數
    select count(*) cnt
    from s1
), s3 as (
    select to_char(transt, 'YYYY') transt
    from wpborrow
    where to_char(transt, 'YYYY') = '&year'
), s4 as ( -- 借閱數
    select count(*) cnt
    from s3
), s5 as ( -- 歸檔數
    select count(*) cnt
    from logtable
    where to_char(transdatetime, 'YYYY') = '&year'
        and comments in ('紙本歸檔','電子檔歸檔')
)
select b.cnt 借閱數, a.cnt 掃描數, c.cnt 歸檔數, round((b.cnt/a.cnt),3)*100 "借閱/掃描百分比"
from s2 a, s4 b, s5 c
;



-- *** 年度借檔方式統計 ***
select substr(transt,1,4) 年度, 
        (case   when viewtype = 1 then '紙本' 
                when viewtype = 2 then '電子'
                else '未知'end) 借檔方式, 
        count(*) 數量
from tmp_kk
where substr(transt,1,4) = '&year'
group by substr(transt,1,4), viewtype
;

-- *** 借檔類別統計（大項） ***
drop table tmp_kk1;
create table tmp_kk1 as
select a.*, substr(b.wpkind,1,1) wpkind1, b.wpcode, c.desc_, b.wpkind, b.wptype, 
    (case when d.wpname is not null then d.wpname else f.wpname end) wpname
from tmp_kk a
    left join fpv.wprec@filescanfpv b on substr(a.transt,1,4) = '&year' and a.wpinno = b.wpinno
    left join fpv.wpcode@filescanfpv c on b.wpcode = c.wpkind
    left join fpv.cirlmweb@filescanfpv d on b.wpkind = d.wpkind and b.wptype = d.wptype
    left join fpv.cirlm@filescanfpv e on b.wpkind = e.wpkind and b.wptype = e.wptype
    left join fpv.cirlmweb@filescanfpv f on e.cirlkind = f.cirlkind and e.cirlser = f.cirlser
where substr(a.transt,1,4) = '&year'
;

drop table tmp_kk2;
create table tmp_kk2 as
select wpinno, transt, receiver, viewtype,
    cast(wpkind1 as nvarchar2(20)) wpkind1,
    wpcode, desc_, wpkind, wptype, wpname
from tmp_kk1
;

select count(*)
from tmp_kk2
where wpname is null
;

with s1 as (
    select count(*) cntAll
    from tmp_kk2
), s2 as (
    select wpkind1, count(*) cnt
    from tmp_kk2
    group by wpkind1
), s3 as (
    select b.wpkind1, b.cnt, a.cntAll
    from s1 a, s2 b
), s4 as (
    select a.*, b.cnt cntWpkind1
    from s3 a left join tmp_aa b on a.wpkind1 = b.wpkind1
), s5 as (
    select 
    (case when wpkind1 = '0' then cast('不分類-管理組' as nvarchar2(20))
                when wpkind1 = '1' then cast('製造業' as nvarchar2(20))
                when wpkind1 = '2' then cast('營造業' as nvarchar2(20))
                when wpkind1 = '3' then cast('家庭看護' as nvarchar2(20))
                when wpkind1 = '4' then cast('家庭幫傭' as nvarchar2(20))
                when wpkind1 = '5' then cast('漁船' as nvarchar2(20))
                when wpkind1 = '6' then cast('特殊' as nvarchar2(20))
                when wpkind1 = '7' then cast('白領' as nvarchar2(20))
                when wpkind1 = '8' then cast('就業安定費' as nvarchar2(20))
                when wpkind1 = '9' then cast('養護機構' as nvarchar2(20))
                else wpkind1 end) wpkind1,
        cntWpkind1, cnt, cntAll,
        (round((cnt/cntAll), 3)*100) percentage,
        (round((cnt/cntwpkind1), 3)*100) bwpkind1Perc
    from s4
)
select wpkind1 公文類別, cntwpkind1 類別公文總數, cnt 借閱數量, cntAll 總借檔數, bwpkind1Perc 類別被借閱百分比, percentage 借閱數佔總借閱百分比
from s5
order by bwpkind1Perc desc, percentage desc
;


-- *** 借檔種類統計（細項） ***
with s1 as (
    select wpkind1, count(*) cntWpkindAll
    from tmp_kk2
    group by wpkind1
), s2 as (
    select wpkind1, wpname, count(*) cnt
    from tmp_kk2
    group by wpkind1, wpname
), s3 as (
    select b.wpkind1, b.wpname, b.cnt, a.cntWpkindAll
    from s1 a, s2 b
    where a.wpkind1 = b.wpkind1
), s4 as (
    select 
        wpkind1,
        wpname, cnt, cntWpkindAll,
        (round((cnt/cntWpkindAll), 3)*100) percentage
    from s3
), s5 as (
    select 
        (case when wpkind1 = '0' then cast('不分類-管理組' as nvarchar2(20))
                    when wpkind1 = '1' then cast('製造業' as nvarchar2(20))
                    when wpkind1 = '2' then cast('營造業' as nvarchar2(20))
                    when wpkind1 = '3' then cast('家庭看護' as nvarchar2(20))
                    when wpkind1 = '4' then cast('家庭幫傭' as nvarchar2(20))
                    when wpkind1 = '5' then cast('漁船' as nvarchar2(20))
                    when wpkind1 = '6' then cast('特殊' as nvarchar2(20))
                    when wpkind1 = '7' then cast('白領' as nvarchar2(20))
                    when wpkind1 = '8' then cast('就業安定費' as nvarchar2(20))
                    when wpkind1 = '9' then cast('養護機構' as nvarchar2(20))
                    else wpkind1 end) wpkind1,
        wpname, cnt, cntWpkindAll, percentage
    from s4
    order by wpkind1, percentage desc
)
select  wpname 種類, wpkind1 類別, cnt 種類計數, cntWpkindAll 類別計數, percentage 百分比
from s5
;

drop table tmp_aa;
drop table tmp_aa1;
drop table tmp_aa2;
drop table tmp_kk;
drop table tmp_kk1;
drop table tmp_kk2;
