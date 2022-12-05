"""
KNPの結果から、時間表現に当てはまる文節のidのリストを出力
"""

import glob
from operator import is_
import os
import json
import re
import csv
from value.time import Time
from typing import Optional

def extract_time_1(s:str,befTime:Time)->Time|None:
    """
    年号XX年XX月XX日から抽出
    """
    a= re.search(r'(昭和|平成|令和)((\d+年)|(元年))\d+月\d+日',s)
    if a is not None:
        b=re.findall(r'\d+',s)
        c=re.findall(r'(昭和|平成|令和)',s)
        d=re.findall(r'元年',s)
      #  print(s,c,d,b)
        year,month,day=0,0,0
        if len(d)!=0:
            year=1
            month=int(b[0])
            day=int(b[1])
        else:
            year=int(b[0])
            month=int(b[1])
            day=int(b[2])
        if c[0]=="令和":
            return Time(2018+year,month,day)
        elif c[0]=="平成":
            return Time(1988+year,month,day)
        elif c[0]=="昭和":
            return Time(1925+year,month,day)
        return None
    return None
def extract_time_2(s:str,befTime:Time)->Time|None:
    """
    年号XX年XX月から抽出
    """
    a= re.search(r'(昭和|平成|令和)((\d+年)|(元年))\d+月',s)
    if a is not None:
        b=re.findall(r'\d+',s)
        c=re.findall(r'(昭和|平成|令和)',s)
        d=re.findall(r'元年',s)
        year,month=0,0
        if len(d)!=0:
            year=1
            month=int(b[0])
        else:
            year=int(b[0])
            month=int(b[1])
        if c[0]=="令和":
            return Time(2018+year,month,0)
        elif c[0]=="平成":
            return Time(1988+year,month,0)
        elif c[0]=="昭和":
            return Time(1925+year,month,0)
        return None
    return None

def extract_time_3(s:str,befTime:Time)->Time|None:
    """
    年号XX年から抽出
    """
    a= re.search(r'(昭和|平成|令和)((\d+年)|(元年))',s)
    if a is not None:
        b=re.findall(r'\d+',s)
        c=re.findall(r'(昭和|平成|令和)',s)
        d=re.findall(r'元年',s)
        year=0
        if len(d)!=0:
            year=1
        else:
            year=int(b[0])
        if c[0]=="令和":
            return Time(2018+year,0,0)
        elif c[0]=="平成":
            return Time(1988+year,0,0)
        elif c[0]=="昭和":
            return Time(1925+year,0,0)
    return None

def extract_time_4(s:str,befTime:Time)->Time|None:
    """
    同年XX月XX日から抽出
    """
    a= re.search(r'同年\d+月\d+日',s)
    if a is not None:
        b=re.findall(r'\d+',s)
        year,month,day=befTime.year,int(b[0]),int(b[1])
        return Time(year,month,day)
    return None
def extract_time_5(s:str,befTime:Time)->Time|None:
    """
    同年XX月XX日から抽出
    """
    a=  re.search(r'同年\d+月',s)
    if a is not None:
        b=re.findall(r'\d+',s)
        year,month=befTime.year,int(b[0])
        return Time(year,month,0)
    return None
def extract_time_6(s:str,befTime:Time)->Time|None:
    """
    同年XX月XX日から抽出
    """
    a=  re.search(r'同年',s)
    if a is not None:
        year=befTime.year
        return Time(year,0,0)
    return None
def extract_time_7(s:str,befTime:Time)->Time|None:
    """
    同月XX日から抽出
    """
    a=  re.search(r'同月\d+日',s)
    if a is not None:
        b=re.findall(r'\d+',s)
        year,month,day=befTime.year,befTime.month,int(b[0])
        return Time(year,month,day)
    return None
def extract_time_8(s:str,befTime:Time)->Time|None:
    """
    同月XX日から抽出
    """
    a=  re.search(r'同月',s)
    if a is not None:
        year,month=befTime.year,befTime.month
        return Time(year,month,0)
    return None
def extract_time_9(s:str,befTime:Time)->Time|None:
    """
    同日から抽出
    """
    a=  re.search(r'同日',s)
    if a is not None:
        year,month,day=befTime.year,befTime.month,befTime.day
        return Time(year,month,day)
    return None

def export_to_json(filepath,data):
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_to_csv(filepath,data):
    import csv
    with open(filepath, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def extract_time(text:str,befTime:Time)->Optional[Time]:
    funcs=[
        extract_time_1,
        extract_time_2,
        extract_time_3,
        extract_time_4,
        extract_time_5,
        extract_time_6,
        extract_time_7,
        extract_time_8,
        extract_time_9,
    ]
    for f in funcs:
        obj=f(text,befTime)
        if obj is not None:
            return obj
    return None
    
def main():
    os.makedirs("01", exist_ok=True)
    files = glob.glob("./00/*.json")
    csv_res=[["id","text_id","text","value"]]
    count=0
    for file in files:
        print(file)
        data={}
        with open(file,encoding="utf-8") as f:
            data=json.load(f)
            befTime=None
            for content in data["contents"]:
                for dat in content["datas"]:
                    for bunsetsu in dat["bunsetsu"]:
                        t=extract_time(bunsetsu["text"],befTime)
                        if t is not None:
                            befTime=t
                            bunsetsu["time"]={
                                "value":t.value()
                            }
                            csv_res.append([count,dat["text_id"],bunsetsu["text"],t.value()])
                            count+=1
        output_path=os.path.splitext(os.path.basename(file))[0]
        export_to_json(f"./01/{output_path}.json",data)
    export_to_csv(f"./01/time_list.csv",csv_res)

if __name__=="__main__":
    main()



