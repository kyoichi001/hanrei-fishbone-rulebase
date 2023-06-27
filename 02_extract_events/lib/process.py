import glob
import os
import json

class Process:

    def process(self,path:str):
        pass

    def __export_to_json(self,filename:str,obj)->None:
        with open(filename, 'w', encoding='utf8', newline='') as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    def main(self,inputDir:str,outputDir:str):
        os.makedirs(outputDir, exist_ok=True)
        files = glob.glob(f"{inputDir}/*.pdf")
        for file in files:
            print(file)
            output_path=os.path.splitext(os.path.basename(file))[0]
            dat=self.process(file)
            self.__export_to_json(f"./{outputDir}/{output_path}.json",dat)
