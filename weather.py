from bs4 import BeautifulSoup as bs
import requests, mechanize


def parse_text(url):
	r = requests.get(url).text   
	#делается запрос по url и возвращет html код url страницы в виде текста

	return r


def find_name_city():
	url = 'https://whatleaks.com/ru/'
	site = parse_text(url)
	result = bs(site, 'lxml').find_all(class_='txt')[1].get_text() 
	#заходит на сайт, где определсяется ip, и парсится название города

	return result


def browsing(name_city):
	if name_city.lower() == 'москва':
		
		return str("https://rp5.ru/Погода_в_Москве_(ВДНХ)") 
		
 	
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.open("https://rp5.ru/")

	br.select_form(name="fsearch")
	br["searchStr"] = name_city
	res = br.submit() 
	#заходит на сайт в формы прописывает название города нажимает поиск(send)

	result = br.follow_link(text=name_city) 
	#ищет ссылку среди списка с указанным названием города и открывает её

	return result.geturl() 
	#возвращает абсолютную ссылку на сайт с определённым городом и погодой в нём


def find_city():
	name_city = find_name_city()

	try:
		return browsing(name_city) 
		# если удачно парсится город с whatleaks.com/ru/
	except:
		print('Возникли проблемы с определением вашего местоположения...')


		def error_area():
			name_city = str(input(
				'''Пожалуйста введите Название вашего города
				 [Для выхода введите "n"]\n> '''))
			
			if name_city.lower() == "n":
				quit()

			for sym in name_city:
				if sym.lower() not in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя -" + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя".upper():
					print("Неверный формат ввода.\nПопробуйте ещё раз\n.....")
					error_area() #повтор ввода

			return name_city.title() 
			#возвращает написанное название города с заглавной буквы


		return browsing(error_area())


def find_weather():
	url = find_city()
	r = parse_text(url)

	name = bs(r, 'lxml').find(id="pointNavi").find("h1").get_text()
	#парсится название города не с whatleaks, а с сайта с погодой
	
	soup = bs(r, 'lxml').find(class_="forecastTable")

	days = []
	soupdays = soup.find("tr")

	for i in range(1, 4):
		soup_day = soupdays.find_all("td")[i].find("b").get_text()
		days.append(soup_day) 
	# парсятся первые три дня. Например: Сегодня, Завтра, Понедельник/Вторник..


	time = [] 
	temp = []
	heaven = []
	fall = []

	souptime = soup.find_all("tr")[1]
	souptemp = soup.find_all("tr")[5] if soup.find_all('tr')[5].find("a").get_text() == 'Температура' else soup.find_all('tr')[4]
	soupheaven = soup.find_all("tr")[2]
	soupfall = soup.find_all("tr")[3]

	last_num = [str(x+18) for x in range(6)] 
	# нужно для разделения температуры и т.д по времени. См. ниже

	box = [[], [], [], []]
	for j in range(1, 14):
		soup1 = souptime.find_all("td")[j].get_text() #парсится время
		soup2 = souptemp.find_all('td')[j].find("b").get_text()	#парсится температура
		soup3 = str(soupheaven.find_all("td")[j].find_all("div")[1])[90:150] #парсится облачность
		soup4 = str(soupfall.find_all("td")[j].find_all("div")[0])[82:150] #парсится наличе осадков


		sup3 = 90 #из-за того, что soup3 & soup4 были внутри скрипта
		sup4 = 82 #необходимо дописывать два цикла

		for a in soup3:
			if a != '&':
				sup3 += 1
			else:
				break

		for b in soup4:
			if b != '(' and b != "'":
				sup4 += 1
			else:
				break

		soup3 = soup3[:(sup3-90)]
		soup4 = soup4[:(sup4-82)] 


		box[0].append(soup1+':00')
		box[1].append(soup2+'C')
		box[2].append(soup3) 
		box[3].append(soup4) 
		#в box-ы постепенно добавляются данные(за какой-либо день)


		if soup1 in last_num:
			time.append(box[0])
			temp.append(box[1])
			heaven.append(box[2]) 
			fall.append(box[3])
			#проверка на то, что soup1 в пределах от 18 до 24
			# если условия выполняется, значит это последний элемент для этого дня 
			# затем из box-ов данные за какой-либо день добавляются в списки 
			# длина списка не может быть больше 3, так как дня всего 3

			box = [[], [], [], []] 


	data = [name, days, time, temp, heaven, fall]

	return data


def main():
	data = find_weather()
	
	print('\n*' + data[0])

	for i in range(3):
		print('\n|' + data[1][i] + '\n|')

		for j in range(len(data[2][i])):
			print(f"|_В {data[2][i][j]}  -  {data[3][i][j]}    -  {data[4][i][j]}" 
				+ " "*(29-len(data[4][i][j])-len(data[3][i][j])) 
				+ f"-  {data[5][i][j]}")


if __name__ == '__main__':
	main()