import sys

#import t00_01_conbine_data
import t00_02_conbine_bunsetsu
import t00_03_conbine_tango
import t00_04_replace_serif

import t01_01_mark_time
import t01_02_mark_rentaishi
import t01_03_mark_person
import t01_04_time_group

import t02_01_extract_time
import t02_02_extract_people
import t02_03_mark_kakari
import t02_04_mark_verb
import t02_05_extract_act

def export_to_json(filename:str,data)->None:
    import json
    with open(filename, 'w', encoding='utf8', newline='') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

inputPath = sys.argv[1]
outputPath = sys.argv[2]

#print("=====================task 01=====================")
#t00_01_conbine_data.main("./data", "./01")
# 使ってない
print("=====================task 00-02=====================", file=sys.stderr)
res=t00_02_conbine_bunsetsu.main(inputPath)
print("=====================task 00-03=====================", file=sys.stderr)
res=t00_03_conbine_tango.main(res)
print("=====================task 00-04=====================", file=sys.stderr)
res=t00_04_replace_serif.main(res)

print("=====================task 01-01=====================", file=sys.stderr)
res=t01_01_mark_time.main(res)
print("=====================task 01-02=====================", file=sys.stderr)
res=t01_02_mark_rentaishi.main(res)
print("=====================task 01-03=====================", file=sys.stderr)
res=t01_03_mark_person.main(res)
print("=====================task 01-04=====================", file=sys.stderr)
res=t01_04_time_group.main(res)

print("=====================task 02-01=====================", file=sys.stderr)
res=t02_01_extract_time.main(res)
print("=====================task 02-02=====================", file=sys.stderr)
res=t02_02_extract_people.main(res)
print("=====================task 02-03=====================", file=sys.stderr)
res=t02_03_mark_kakari.main(res)
print("=====================task 02-04=====================", file=sys.stderr)
res=t02_04_mark_verb.main(res)
print("=====================task 02-05=====================", file=sys.stderr)
res=t02_05_extract_act.main(res)

print("fishbone extracted", file=sys.stderr)
export_to_json(outputPath,res)