import t01_01_mark_time
import t01_02_mark_rentaishi
import t01_03_mark_person

print("=====================task 01=====================")
t01_01_mark_time.main("../00_process_data/03", "./01")
print("=====================task 02=====================")
t01_02_mark_rentaishi.main("./01", "./02")
print("=====================task 03=====================")
t01_03_mark_person.main("./02", "./03")
print("=====================task 04=====================")
t01_03_mark_person.main("./03", "./04")
