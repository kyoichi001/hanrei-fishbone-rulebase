import t02_01_extract_time
import t02_02_extract_people
import t02_03_mark_kakari
import t02_04_extract_act

print("=====================task 01=====================")
t02_01_extract_time.main("../01_mark_data/03", "./01")
print("=====================task 02=====================")
t02_02_extract_people.main("./01", "./02")
print("=====================task 03=====================")
t02_03_mark_kakari.main("./01", "./03")
print("=====================task 04=====================")
t02_04_extract_act.main("./03", "./04")
