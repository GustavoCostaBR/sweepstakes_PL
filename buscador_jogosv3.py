from datetime import datetime, timedelta
import pytz
import sys
# import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import ssl
import pdb
# import var_dump
#from lxml import html
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

Rivalidades_Inglaterra = {'Aldershot Town': ['Reading'],'Arsenal': ['Chelsea', 'Manchester United', 'Tottenham Hotspur'],'Aston Villa': ['Birmingham City', 'West Bromwich Albion', 'Wolverhampton Wanderers'],'Barnet': ['Wycombe Wanderers'],'Barnsley': ['Doncaster Rovers', 'Rotherham United'],'Birmingham City': ['Aston Villa', 'West Bromwich Albion', 'Wolverhamtpon Wanderers'],'Blackburn Rovers': ['Burnley'],'Blackpool': ['Preston North End'],
'Bolton Wanderers': ['Bury', 'Wigan Athletic'],
'Bournemouth': ['Southampton'],
'Bradford City': ['Leeds United', 'Bradford Park Avenue', 'Huddersfield Town', 'Halifax Town'],
'Bradford Park Avenue': ['Bradford City', 'Halifax Town'],
'Brentford': ['Fulham', "Queens Park Rangers"],
'Brighton & Hove Albion': ['Crystal Palace'],
'Bristol City': ['Bristol Rovers', 'Cardiff City'],
'Bristol Rovers': ['Bristol City', 'Swindon Town'],
'Burnley': ['Blackburn Rovers'],
'Bury': ['Bolton Wanderers', 'Rochdale'],
'Cambridge United': ['Colchester United', 'Peterborough United'],
'Cardiff City': ['Swansea City', 'Bristol City', 'Newport County'],
'Carlisle United': ['Workington'],
'Charlton Athletic': ['Crystal Palace', 'Millwall'],
'Chelsea': ['Arsenal', 'Leeds United', 'Manchester United', 'Tottenham Hotspur', 'Fulham', "Queens Park Rangers"],
'Chester': ['Wrexham', 'Tranmere Rovers'],
'Chesterfield': ['Mansfield Town'],
'Colchester United': ['Southend United', 'Cambridge United'],
'Coventry City': ['Leicester City'],
'Crewe Alexandra': ['Port Vale', 'Stockport County'],
'Crystal Palace': ['Brighton & Hove Albion', 'Charlton Athletic', 'Millwall'],
'Darlington': ['Hartlepool United'],
'Derby County': ['Nottingham Forest', 'Leicester City', 'Notts County'],
'Doncaster Rovers': ['Barnsley', 'Rotherham United', 'Scunthorpe United'],
'Everton': ['Liverpool'],
'Exeter City': ['Plymouth Argyle', 'Torquay United'],
'Fulham': ['Brentford', 'Chelsea', "Queens Park Rangers"],
'Gainsborough Trinity': ['Lincoln City'],
'Grimsby Town': ['Hull City', 'Lincoln City', 'Scunthorpe United'],
'Halifax Town': ['Bradford City', 'Bradford Park Avenue'],
'Hartlepool United': ['Darlington'],
'Hereford United': ['Shrewsbury Town'],
'Huddersfield Town': ['Leeds United', 'Bradford City'],
'Hull City': ['Grimsby Town', 'York City'],
'Ipswich Town': ['Norwich City'],
'Leeds United': ['Chelsea', 'Manchester United', 'Bradford City', 'Huddersfield Town'], 'Leicester City': ['Coventry City', 'Derby County', 'Nottingham Forest'],
'Leyton Orient': ['West Ham United'],
'Lincoln City': ['Grimsby Town', 'Scunthorpe United', 'Gainsborough Trinity'],
'Liverpool': ['Everton', 'Manchester City', 'Manchester United'],
'Luton Town': ['Watford'],
'Manchester City': ['Liverpool', 'Manchester United'],
'Manchester United': ['Arsenal', 'Chelsea', 'Leeds United', 'Liverpool', 'Manchester City'],
'Mansfield Town': ['Chesterfield', 'Notts County'],
'Milton Keynes Dons': ['Wimbledon'],
'Middlesbrough': ['Newcastle United', 'Sunderland'],
'Millwall': ['Charlton Athletic', 'Crystal Palace', 'West Ham United'],
'Newcastle United': ['Sunderland', 'Middlesbrough'],
'Newport County': ['Cardiff City'],
'Northampton Town': ['Peterborough United'],
'Norwich City': ['Ipswich Town'],
'Nottingham Forest': ['Derby County', 'Notts County', 'Leicester City'],
'Notts County': ['Nottingham Forest', 'Derby County', 'Mansfield Town'],
'Oldham Athletic': ['Rochdale'],
'Oxford United': ['Reading', 'Swindon Town'],
'Peterborough United': ['Northampton Town', 'Cambridge United'],
'Plymouth Argyle': ['Exeter City', 'Torquay United'],
'Port Vale': ['Crewe Alexandra', 'Stoke City'],
'Portsmouth': ['Southampton'],
'Preston North End': ['Blackpool'],
"Queens Park Rangers": ['Brentford', 'Chelsea', 'Fulham'],
'Reading': ['Oxford United', 'Swindon Town', 'Aldershot Town'],
'Rochdale': ['Oldham Athletic', 'Bury'],
'Rotherham United': ['Barnsley', 'Doncaster Rovers'],
'Scunthorpe United': ['Doncaster Rovers', 'Grimsby Town', 'Lincoln City'],
'Sheffield United': ['Sheffield Wednesday'],
'Sheffield Wednesday': ['Sheffield United'],
'Shrewsbury Town': ['Walsall', 'Hereford United'],
'Southampton': ['Bournemouth', 'Portsmouth'],
'Southend United': ['Colchester United'],
'Stockport County': ['Crewe Alexandra'],
'Stoke City': ['Port Vale'],
'Sunderland': ['Middlesbrough', 'Newcastle United'],
'Swansea City': ['Cardiff City'],
'Swindon Town': ['Reading', 'Oxford United', 'Bristol Rovers'],
'Torquay United': ['Exeter City', 'Plymouth Argyle'],
'Tottenham Hotspur': ['Arsenal', 'Chelsea', 'West Ham United'],
'Tranmere Rovers': ['Chester', 'Wrexham'],
'Walsall': ['Shrewsbury Town'],
'Watford': ['Luton Town'],
'West Bromwich Albion': ['Wolverhampton Wanderers', 'Birmingham City', 'Aston Villa'],
'West Ham United': ['Tottenham Hotspur', 'Millwall', 'Leyton Orient'],'Wigan Athletic': ['Bolton Wanderers'] ,'Wimbledon': ['Milton Keynes Dons'],
'Workington': ['Carlisle United'],
'Wolverhampton Wanderers': ['West Bromwich Albion', 'Birmingham City', 'Aston Villa'],
'Wrexham': ['Chester', 'Tranmere Rovers'],
'Wycombe Wanderers': ['Barnet'],
'York City': ['Hull City']}

Rivalidades_Escocia = {
  'Aberdeen': ['Dundee United', 'Inverness CT'],
  'Airdrieonians': ['Motherwell', 'Hamilton Academical'],
  'Arbroath': ['Montrose', 'Forfar Athletic', 'Brechin City'],
  'Ayr United': ['Kilmarnock'],
  'Brechin City': ['Arbroath', 'Montrose', 'Forfar Athletic'],
  'Celtic': ['Rangers'],
  'Clyde': ['Partick Thistle'],
  'Cowdenbeath': ['Dunfermline Athletic', 'Raith Rovers', 'East Fife'],
  'Dundee': ['Dundee United', 'St. Johnstone'],
  'Dundee United': ['Dundee', 'Aberdeen', 'St. Johnstone'],
  'Dunfermline Athletic': ['Raith Rovers', 'Cowdenbeath', 'East Fife'],
  'East Fife': ['Dunfermline Athletic', 'Raith Rovers', 'Cowdenbeath'],
  'East Stirlingshire': ['Falkirk'],
  'Falkirk': ['East Stirlingshire'],
  'Forfar Athletic': ['Arbroath', 'Montrose', 'Brechin City'],
  'Greenock Morton': ['St. Mirren'],
  'Hamilton Academical': ['Motherwell', 'Airdrieonians'],
  'Heart of Midlothian': ['Hibernian'],  'Hearts': ['Hibernian'],
  'Hibernian': ['Heart of Midlothian', 'Hearts'],
  'Inverness CT': ['Ross County', 'Aberdeen'],
  'Kilmarnock': ['Ayr United'],
  'Montrose': ['Arbroath', 'Forfar Athletic', 'Brechin City'],
  'Motherwell': ['Hamilton Academical', 'Airdrieonians'],
  'Partick Thistle': ['Clyde'],
  "Queen's Park": ['Rangers'],
  'Raith Rovers': ['Dunfermline Athletic', 'Cowdenbeath', 'East Fife'],
  'Rangers': ['Celtic', "Queen's Park"],
  'Ross County': ['Inverness CT'],
  'St. Johnstone': ['Dundee', 'Dundee United'],
  'St. Mirren': ['Greenock Morton']
}

Times_sem_rivais = {'Livingston': ['Sem rival']}
Rivalidades = [Rivalidades_Inglaterra , Rivalidades_Escocia, Times_sem_rivais]
times_desconsiderados = {}
# conn = sqlite3.connect('content.sqlite')
# conn.execute('PRAGMA foreign_keys = ON')
# cur = conn.cursor()
# cur.execute('CREATE TABLE IF NOT EXISTS Jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT UNIQUE, link TEXT UNIQUE, Profession TEXT UNIQUE, Workforce TEXT, [Average Age] REAL, [Average Salary] REAL, [Average Male Salary] REAL, [Average Female Salary] REAL, [Total of Male Workers] REAL, [Total of Female Workers] REAL, [Profession Tier] TEXT)')

# cur.execute('CREATE TABLE IF NOT EXISTS Vari (Jobs_id INTEGER UNIQUE, vari FLOAT, dev FLOAT, [vari acumul] FLOAT, [disparidade salarial] FLOAT, [disparidade salarial relacao media] FLOAT, [disparidade salarial relacao media cumulativa] FLOAT, FOREIGN KEY(Jobs_id) REFERENCES Jobs(id))')


# cur.execute('SELECT MAX(id) FROM Keywords')
headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'}
url = sys.argv[11]
ligas_times_diferentes = ['https://www.worldfootball.net/all_matches/champions-league-2022-2023/', 'https://www.worldfootball.net/all_matches/europa-league-2022-2023/', 'https://www.worldfootball.net/all_matches/europa-conference-league-2022-2023/', 'https://www.worldfootball.net/all_matches/uefa-super-cup-2022/','https://www.worldfootball.net/all_matches/klub-wm-2022/']
urls_times_diferentes = ['https://www.worldfootball.net/players/champions-league-2022-2023/', 'https://www.worldfootball.net/players/europa-league-2022-2023/', 'https://www.worldfootball.net/players/europa-conference-league-2022-2023/', 'https://www.worldfootball.net/players/uefa-super-cup-2022/', 'https://www.worldfootball.net/players/klub-wm-2022/']
ligas_times_ingleses_nao_listados = ['https://www.worldfootball.net/all_matches/sco-fa-cup-2022-2023/','https://www.worldfootball.net/all_matches/sco-league-cup-2022-2023/', 'https://www.worldfootball.net/all_matches/eng-fa-cup-2022-2023/', 'https://www.worldfootball.net/all_matches/eng-league-cup-2022-2023/', 'https://sco.worldfootball.net/all_matches/sco-playoff-2021-2022-premiership/']
urls_times_ingleses_nao_listados = ['https://www.worldfootball.net/players/sco-fa-cup-2022-2023/','https://www.worldfootball.net/players/sco-league-cup-2022-2023/', 'https://www.worldfootball.net/players/eng-fa-cup-2022-2023/', 'https://www.worldfootball.net/players/eng-league-cup-2022-2023/', 'https://sco.worldfootball.net/players/sco-playoff-2021-2022-premiership/']
f = 0

# Verifying if it is one of the international championships
for u in range(len(ligas_times_diferentes)):
	if url == ligas_times_diferentes[u]:
		f = 1
		url2 = urls_times_diferentes[u]
		req2 = req = urllib.request.Request(url2, headers=headers)
		html2 = urllib.request.urlopen(req2, context=ctx).read()
		soup = BeautifulSoup(html2, 'lxml')
		body2 = soup.findAll('tr')
		for tag in body2:
			a = 1
			try:
				x = tag.find_all('td')
				# pdb.set_trace()
				time_champions = x[1].find('a').text
				# print(time_champions)
				if " FC" in time_champions:
					time2 = time_champions.replace(" FC", "")
				elif "AFC " in time_champions:
					time2 = time_champions.replace("AFC ", "")
				elif "FC " in time_champions:
					time2 = time_champions.replace("FC ", "")
				elif " AFC" in time_champions:
					time2 = time_champions.replace(" AFC", "")
				else:
					time2 = time_champions
				if time2 not in Rivalidades[0] and time2 not in Rivalidades[1] and time2 not in Rivalidades[2]:
					times_desconsiderados[time2] = ['Sem rival']

			except:
				continue
		Rivalidades.append(times_desconsiderados)
	if u<5 and url == ligas_times_ingleses_nao_listados[u]:
		f = 0
		url2 = urls_times_ingleses_nao_listados[u]
		req2 = req = urllib.request.Request(url2, headers=headers)
		html2 = urllib.request.urlopen(req2, context=ctx).read()
		soup = BeautifulSoup(html2, 'lxml')
		body2 = soup.findAll('tr')
		for tag in body2:
			a = 1
			try:
				x = tag.find_all('td')
				# pdb.set_trace()
				time_champions = x[1].find('a').text
				# print(time_champions)
				if " FC" in time_champions:
					time2 = time_champions.replace(" FC", "")
				elif "AFC " in time_champions:
					time2 = time_champions.replace("AFC ", "")
				elif "FC " in time_champions:
					time2 = time_champions.replace("FC ", "")
				elif " AFC" in time_champions:
					time2 = time_champions.replace(" AFC", "")
				else:
					time2 = time_champions
				if time2 not in Rivalidades[0] and time2 not in Rivalidades[1] and time2 not in Rivalidades[2]:
					times_desconsiderados[time2] = ['Sem rival']
			except:
				continue

		Rivalidades.append(times_desconsiderados)


req = urllib.request.Request(url, headers=headers)
html1 = urllib.request.urlopen(req, context=ctx).read()



# print(html1)

# file = open("Jorge.txt", mode = 'w')
# file.write(str(html1))
# file.close


soup = BeautifulSoup(html1, 'lxml')
body = soup.findAll('tr')
gmt = pytz.timezone('GMT')
# limite inferior de data
# dt = sys.argv[1]
int_list = [int(x) for x in sys.argv[1:6]]
int_list2 = [int(x) for x in sys.argv[6:11]]

dt = datetime(*int_list, tzinfo=gmt)
# limite superior de data
dt2 = datetime(*int_list2, tzinfo=gmt)
#  dt2 = sys.argv[2]
# dt2 = datetime(2023, 2, 12, 20, 30, tzinfo=gmt)
v = 2
# pdb.set_trace()
jogos_semana = []
time = []
jogos = []
hora = []
dia = []
peso = []
if "premier-league" in url:
	liga = 'PL'

elif 'sco-playoff' in url:
	liga = 'SPFL - playoff'
elif "premiership" in url:
	liga = 'SPFL'
elif "championship" in url:
	liga = 'LCH'
elif "champions-league" in url:
	liga = 'UCL'
elif "europa-league" in url:
	liga = 'UEL'
elif "conference-league" in url:
	liga = 'UECL'
elif "uefa-super-cup" in url:
	liga = 'USC'
elif "eng-fa-cup" in url:
	liga = 'FAC'
elif "eng-league-cup" in url:
	liga = 'EFL'
elif "sco-fa-cup" in url:
	liga = 'SC'
elif "sco-league-cup" in url:
	liga = 'SLC'
elif "eng-fa-community" in url:
	liga = 'FACS'
else:
	liga = 'FCWC'
contador = 0
contadorx=0
datas_playoffs_sco = []
z8 = 0
for tag in body:
	a=1
	# Tentando garantir que ele só pegue a final caso seja playoff escoces
	try:
		if "sco-playoff" in url:
			try:
				zeta = tag.find('th')
				zeta2 = zeta.find('a').text
				if zeta2 == "Final":
					zeta3 = tag.find_next_sibling()
					zeta4 = zeta3.find('td')
					zeta5 = zeta4.find('a').text
					zeta55 = gmt.localize(datetime.strptime(zeta5, "%d/%m/%Y"))
					datas_playoffs_sco.append(zeta55)
					zeta6 = zeta3.find_next_sibling()
					zeta7 = zeta6.find('td')
					zeta8 = zeta7.find('a').text
					zeta88 = gmt.localize(datetime.strptime(zeta8, "%d/%m/%Y"))
					datas_playoffs_sco.append(zeta88)
					z8 = 1
			except:
				z8=0
		x = tag.find_all('td')
		for tags in x:
			try:
				if tags.find('a') is None:
					continue
				y = tags.find('a').text
				dt3 = gmt.localize(datetime.strptime(y, "%d/%m/%Y"))
				if "sco-playoff" in url:
					if dt3 > dt and dt3 < dt2 and dt3 in datas_playoffs_sco:
						v = 1

						data3 = dt3

				elif dt3 > dt and dt3 < dt2:
					v = 1

					data3 = dt3
				elif dt3 < dt or dt3 > dt2:
					v = 2
					# print(dt3)
					# print("chegamos no limite")
			except:
				if v == 1:
					# pdb.set_trace()
					if "FC" in y and "AFC" not in y:
						# index = y.index("FC")
						# j=(y[:index] + y[index+len("FC"):]).replace(" ","")
						if " FC" in y:
							j = y.replace(" FC", "")
						else:
							j = y.replace("FC ", "")
						# print(j)
						if j in Rivalidades[0] or j in Rivalidades[1] or j in Rivalidades[2] or j in Rivalidades[3]:
							time.append(j)
							# print(j)

							if contador % 2 == 0:
								esquema = tags.find_previous_sibling('td')
								hora_reino_unido = datetime.strptime(esquema.text, '%H:%M')
								hora_brasil = hora_reino_unido - timedelta(hours=4)
								hora_brasil_str = datetime.strftime(hora_brasil, '%H:%M')
								hora.append(hora_brasil_str)
								datax = datetime.fromisoformat(str(data3))
								dia_mes_str = datax.strftime('%d/%m')
								dia.append(dia_mes_str)
							contador = contador + 1
					elif "AFC " in y:
						# pdb.set_trace()
						j = y.replace("AFC ", "")
						# print(j)
						if j in Rivalidades[0] or j in Rivalidades[1] or j in Rivalidades[2] or j in Rivalidades[3]:
							time.append(j)
							# print(j)

							if contador % 2 == 0:
								esquema = tags.find_previous_sibling('td')
								hora_reino_unido = datetime.strptime(esquema.text, '%H:%M')
								hora_brasil = hora_reino_unido - timedelta(hours=4)
								hora_brasil_str = datetime.strftime(hora_brasil, '%H:%M')
								hora.append(hora_brasil_str)
								datax = datetime.fromisoformat(str(data3))
								dia_mes_str = datax.strftime('%d/%m')
								dia.append(dia_mes_str)
							contador = contador + 1
					elif " AFC" in y:
						j=(y.rstrip(" AFC"))
						# print(j)
						if j in Rivalidades[0] or j in Rivalidades[1] or j in Rivalidades[2] or j in Rivalidades[3]:
							time.append(j)
							# print(j)

							if contador % 2 == 0:
								esquema = tags.find_previous_sibling('td')
								hora_reino_unido = datetime.strptime(esquema.text, '%H:%M')
								hora_brasil = hora_reino_unido - timedelta(hours=4)
								hora_brasil_str = datetime.strftime(hora_brasil, '%H:%M')
								hora.append(hora_brasil_str)
								datax = datetime.fromisoformat(str(data3))
								dia_mes_str = datax.strftime('%d/%m')
								dia.append(dia_mes_str)
							contador = contador + 1
					else:
						if y in Rivalidades[0] or y in Rivalidades[1] or y in Rivalidades[2] or y in Rivalidades[3]:
							time.append(y)
							# print(y)

							if contador % 2 == 0:
								esquema = tags.find_previous_sibling('td')
								hora_reino_unido = datetime.strptime(esquema.text, '%H:%M')
								hora_brasil = hora_reino_unido - timedelta(hours=4)
								hora_brasil_str = datetime.strftime(hora_brasil, '%H:%M')
								hora.append(hora_brasil_str)
								datax = datetime.fromisoformat(str(data3))
								dia_mes_str = datax.strftime('%d/%m')
								dia.append(dia_mes_str)
							contador = contador + 1
					continue
				if v == 2:
					continue
				else:
					continue
	except:
		continue
# print(time)
# print(dia)
# print(hora)



for x in range(len(time)):
	if x % 2 == 0:
		for y in range(len(Rivalidades)):
			# for z in range(len(Rivalidades[y])):
			try:
				if time[x+1] in Rivalidades[y][(time[x])]:
					peso.append('P2')
					# if time[x] in Rivalidades[0] and time[x+1] in Rivalidades[0]:
					# 	liga.append('PL')
					# elif time[x] in Rivalidades_Inglaterra and time[x+1] in Rivalidades_Inglaterra:

				else:
					peso.append('P1')
					# if time[x] in Rivalidades_Inglaterra and time[x+1] in Rivalidades_Inglaterra:
					# 	liga.append('PL')
			except:
				continue
		jogos.append(time[x] + " x " + time[x+1])
		# print(jogos[contadorx])
		# print(peso[contadorx])
		# print(liga)
		# print(dia[contadorx])
		# print(hora[contadorx])
		jogos_semana.append(jogos[contadorx] + " - " + peso[contadorx] + " (" + liga + ") - " + dia[contadorx] + " - " +hora[contadorx])
		contadorx = contadorx + 1
	else:
		continue
contadory = 0
lista_delete_time = []
lista_delete_peso = []
lista_delete_jogos = []
lista_delete_dia = []
lista_delete_hora = []
lista_delete_jogos_semana = []
for u in range(len(time)):
	if u % 2 == 0:
		# print(time[u])
		if not time[u] in Rivalidades[0] and not time[u+1] in Rivalidades[0] and not time[u] in Rivalidades[1] and not time[u+1] in Rivalidades[1] and not time[u] in Rivalidades[2] and not time[u+1] in Rivalidades[2]:

			lista_delete_time.extend([u, u+1])
			# print(lista_delete_time)
			lista_delete_peso.append(int(u/2))
			lista_delete_jogos.append(int(u/2))
			lista_delete_dia.append(int(u/2))
			lista_delete_hora.append(int(u/2))
			lista_delete_jogos_semana.append(int(u/2))

			# print(time[u])
	# contadory = contadory + 1
	# print(u)

timef = [elem for idx, elem in enumerate(time) if idx not in lista_delete_time]
	# for y in
	# time[x]
jogos_semana_f = [elem for idx, elem in enumerate(jogos_semana) if idx not in lista_delete_jogos_semana]

# print(time)

if f == 1:
	for y in jogos_semana_f:
		print(y)

if f == 0:
	for y in jogos_semana:
		print(y)
# for x in time:
# 	print(x)
	# 	print(x)
	# 	for y in Rivalidades_Inglaterra[x]:
	# 		print(y)
	# 		if time[x] == 0:
	# 			continue