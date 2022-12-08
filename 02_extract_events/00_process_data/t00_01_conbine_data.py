import glob
from operator import is_
import os
import json
from re import T
import csv

"""
TMSの係り受け解析結果とpdfの抽出結果を合成したjsonファイルを作成

csvファイルはjsonファイルを係り受けしたもの
同じファイル名でないとペアとして判定されない

csvファイルに複数文書の係り受け解析結果があってもだめ

"""

# ファイルID,行ID,文章ID,単語ID,見出し語,原形,置換語,品詞,品詞詳細,係り先,態度表現,分かち書き情報
def load_csv(filepath:str):
    print(filepath)
    output_path=os.path.splitext(os.path.basename(filepath))[0]
    res={
        "filename":output_path,
        "texts":[]
    }
    with open(filepath,encoding="cp932") as f:
        reader = csv.reader(f)
        next(reader)
        text_obj={# 文Obj
            "text_id":1-1,
            "bunsetsu":[]
        }
        prev_row_id=1
        for row in reader:
            row_id=int(row[1])
            text_id=int(row[2])
            #print(row)
            if prev_row_id!=row_id:
                res["texts"].append(text_obj)
                text_obj={
                    "text_id":row_id-1,
                    "bunsetsu":[]
                }
            text_obj["bunsetsu"].append({
                "id":int(row[3])-1,
                "text":row[4],
                "mrph":row[5],
                "type":row[7],
                "type2":row[8],
                "parent":max(int(row[9])-1,-1)
            })
            prev_row_id=row_id
        res["texts"].append(text_obj)
    return res
    #with open("./00/"+output_path+"_test.json", 'w', encoding='utf8', newline='') as f:
    #    json.dump(csv_data[output_path], f, ensure_ascii=False, indent=2)

def conbine_to_json(outputDir:str,filepath:str,csv_data):
    output_path=os.path.splitext(os.path.basename(filepath))[0]
    data={}
    with open(filepath,encoding="utf-8") as f:
        print(filepath)
        data=json.load(f)
        index=0
        for content in data["contents"]:
            content["datas"]=[]
            count=len(content["texts"])+len(content["selifs"])+len(content["blackets"])
            for i in range(count):
                content["datas"].append(csv_data[output_path]["texts"][index])
                index+=1
    with open(f"{outputDir}/{output_path}.json", 'w', encoding='utf8', newline='') as f:
        print(f"{outputDir}/{output_path}.json")
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(inputDir:str,outputDir:str):
    os.makedirs(outputDir, exist_ok=True)
    csv_files = glob.glob(f"{inputDir}/*.csv")
    csv_data={}
    for file in csv_files:
        output_path=os.path.splitext(os.path.basename(file))[0]
        csv_data[output_path]=load_csv(file)
    json_files = glob.glob(f"{inputDir}/*.json")
    for file in json_files:
        conbine_to_json(outputDir,file,csv_data)

if __name__=="__main__":
    main("./data","./01")