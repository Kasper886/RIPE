#IP parser
import json, re, requests, bs4, sys, os

#TOR
import socket, socks
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket
#END TOR

mask = input('Введите маску сети, которую будем парсить, например, 22: ')
finputurl = 'files/NotAnnounced_'+str(mask)+'.txt'
foutputname = 'email_'+str(mask)+'.txt'
input = open(finputurl, 'r')
output = open(foutputname, 'w')
linesarray = input.readlines()
input.close()

mail_template = '[\w.-]+@[0-9A-Za-z-]+\.[\w.]+' #Шаблон поиска email
org_template = 'ORG-[a-zA-Z0-9]*-RIPE' #Шаблон поиска ORG

number = len(linesarray)

print(r'Всего сетей {}'.format(number))

#Формируем ссылку и вынимаем контакты
#for i in range(34, 38):
for i in range(len(linesarray)):
	url = 'https://rest.db.ripe.net/search.json?query-string='+linesarray[i]+'&flags=no-referenced&flags=no-irt&source=RIPE'
	
	#print(url)
	s = requests.get(url)
	b = bs4.BeautifulSoup(s.text, "html.parser")
	b=str(b)
	mail1 = re.findall(mail_template, b)
	
	#Формируем номер сети для вывода
	string = str(linesarray[i])
	#linesarray[i] = string.replace('%20',' ')
	string = string.replace('%2F','/')
	string = str(i) + '. ' + string
	
	#Ищем ORG и вытаскиваем email
	try: #Если ORG нет, значит сеть является частью более крупной сети
		org  = re.findall(org_template, b)[0]
	except IndexError:
		string = 'Сеть '+string+'является подсетью более крупной сети\n\n'
		output.write(string)
		print(string, end='')
		continue
	
	url2 = 'https://rest.db.ripe.net/search.json?query-string='+org+'&inverse-attribute=org&flags=no-filtering&source=RIPE'	#https://rest.db.ripe.net/search.json?query-string=ORG-LEA1-RIPE&inverse-attribute=org&flags=no-filtering&source=RIPE
	
	#print(url2)
	s2 = requests.get(url2)
	b2 = bs4.BeautifulSoup(s2.text, "html.parser")
	b2=str(b2)
	mail2 = re.findall(mail_template, b2)
	#print(mail2)
	#mail = str(mail)
	mail=mail1+mail2
	
	#Вывод сети 
	print (string, end='')
	# if i == 0:
		# output.write(linesarray[i])
	# else:
		# output.write('\n\n'+linesarray[i])
	output.write(string+'')
	#Удаляем дубликаты
	seen=[]
	for i in range(len(mail)):
		if seen.count(mail[i]) == 0:
			seen.append(mail[i])
			output.write(mail[i]+' ')
	output.write('\n\n')
output.close()
