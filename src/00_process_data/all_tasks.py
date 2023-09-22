import t00_01_conbine_data
import t00_02_conbine_bunsetsu
import t00_03_conbine_tango
import t00_04_replace_serif

#print("=====================task 01=====================")
#t00_01_conbine_data.main("./data", "./01")
# 使ってない
print("=====================task 02=====================")
t00_02_conbine_bunsetsu.main("./data", "./02")
print("=====================task 03=====================")
t00_03_conbine_tango.main("./02", "./03")
print("=====================task 04=====================")
t00_04_replace_serif.main("./03", "./04")
