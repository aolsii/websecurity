import csv
import os


filename="EnFrequency125k.txt"
filename1="EnFreq25k.txt"

i=0
with open(filename1,'w')as csv_file:
    with open(filename, 'r', encoding='utf-8', errors='ignore') as fi:
            for line in fi:
                if(i<25000):
                    csv_file.write(line)
                    i = i + 1
                else:
                    break
    fi.close()
csv_file.close()




