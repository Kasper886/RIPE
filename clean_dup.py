import json, re, requests, bs4, sys, os
#Удаляем дубликаты строк через файл
name = input('Введите имя текстового файла без расширения: ')
name2 = name+'_clean'+'.txt'
path1 = 'result/'+name+'.txt'
path2 = 'result/'+name2
input = open(path1, 'r')
output = open(path2, 'w')
linesarray = input.readlines()
input.close()

seen = []

# for i in range(0,30):
for i in range(len(linesarray)):
	if seen.count(linesarray[i]) == 0:
		seen.append(linesarray[i])
		output.write(linesarray[i])
output.close()		