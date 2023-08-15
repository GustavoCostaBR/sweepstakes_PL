from datetime import datetime, timedelta
import pytz
import sys
import urllib.request
from bs4 import BeautifulSoup
import ssl
import pdb
import yaml

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# sys.stdout.reconfigure(encoding='utf-8')

# Gambiarra champions
u0 = 0


def time_or_result(string):
	if ":" in string and "(" in string:
        # String contains ":" and "(", likely a result
        # Perform specific treatment for results
		return "Result"
	elif "resch." in string:
		return "postponed"
	else:
        # String doesn't contain ":" and "(", likely a team name
        # Perform specific treatment for team names
		return "Team"

def selection_liga(url, data2):
	url_times_world_diferentes = "z"
	url_times_eng_sco_diferentes = "z"
	if "premier-league" in url:
		liga = 'PL'

	elif 'sco-playoff' in url:
		liga = 'SPFL - playoff'
		champstring = "sco-playoff"
		stagestring = ["Final"]
		liga_url = champstring
		url_times_eng_sco_diferentes = data2['CTDS']['URL_TIMES_SPFL_PLAYOFF']
	elif 'eng-playoff' in url:
		liga = 'LCH - playoff'
		champstring = "eng-playoff"
		stagestring = ["Final"]
		liga_url = champstring

	elif "premiership" in url:
		liga = 'SPFL'
	elif "championship" in url:
		liga = 'LCH'
	elif "champions-league-qual" in url:
		liga = 'UCL_QUAL'
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_QUAL_UCL']
	elif "champions-league" in url:
		liga = 'UCL'
		champstring = "champions-league"
		stagestring = ["Round of 16", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_UCL']
	elif "europa-league-qual" in url:
		liga = 'UEL_QUAL'
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_QUAL_UEL']
	elif "europa-league" in url:
		liga = 'UEL'
		champstring = "europa-league"
		stagestring = ["Round of 16", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_UEL']
	elif "europa-conference-league-qual" in url:
		liga = 'UECL_QUAL'
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_QUAL_UECL']
	elif "conference-league" in url:
		liga = 'UECL'
		champstring = "europa-conference-league"
		stagestring = ["Round of 16", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_UECL']
	elif "uefa-super-cup" in url:
		liga = 'USC'
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_USC']
	elif "eng-fa-cup" in url:
		liga = 'FAC'
		champstring = "eng-fa-cup"
		stagestring = ["3. Round", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_eng_sco_diferentes = data2['CTDE']['URL_TIMES_FAC']

	elif "eng-league-cup" in url:
		liga = 'EFL'
		champstring = "eng-league-cup"
		stagestring = ["Round of 16", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_eng_sco_diferentes = data2['CTDE']['URL_TIMES_EFL']

	elif "sco-fa-cup" in url:
		liga = 'SC'
		champstring = "sco-fa-cup"
		stagestring = ["Quarter-finals", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_eng_sco_diferentes = data2['CTDS']['URL_TIMES_SC']
	elif "sco-league-cup" in url:
		liga = 'SLC'
		champstring = "sco-league-cup"
		stagestring = ["Quarter-finals", "Semi-finals", "Final"]
		liga_url = champstring
		url_times_eng_sco_diferentes = data2['CTDS']['URL_TIMES_SLC']
	elif "eng-fa-community" in url:
		liga = 'FACS'
		champstring = "eng-fa-community"
		stagestring = ["Final"]
		liga_url = champstring
	elif "klub-wm" in url:
		liga = 'FCWC'
		champstring = "klub-wm"
		stagestring = ["Semi-finals", "Third place", "Final"]
		liga_url = champstring
		url_times_world_diferentes = data2['CTDW']['URL_TIMES_FCWC']
	if 'champstring' in locals():
		return champstring, stagestring, liga, liga_url, url_times_world_diferentes, url_times_eng_sco_diferentes
	else:
		# cannot return None to liga_url, future verification in another function would return a problem, excepction
		return None, None, liga, 'jiorjito', url_times_world_diferentes, url_times_eng_sco_diferentes

def cups_after(url, champstring, tag, stagestring):
	z8 = 0
	if champstring in url:
		target_list = []
		for u in stagestring:
			try:
				zeta = tag.find('th')
				zeta2 = zeta.find('a').text
				if zeta2 == u:
					zeta3 = tag.find_next_sibling()
					zeta4 = zeta3.find('td')
					zeta5 = zeta4.find('a').text
					zeta55 = gmt.localize(datetime.strptime(zeta5, "%d/%m/%Y"))
					target_list.append(zeta55)
					z8 = 1
			except:
				if z8 == 1:
					continue
				else:
					z8 = 0
	if z8 == 1:
		return target_list, zeta3
	else:
		return None, None

def extends_cups_after(url, champstring, tag, stagestring):
	z8 = 0
	if champstring in url:
		target_list = []
		try:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			zeta6 = zeta3.find_next_sibling()
			zeta7 = zeta6.find('td')
			zeta8 = zeta7.find('a').text
			zeta88 = gmt.localize(datetime.strptime(zeta8, "%d/%m/%Y"))
			target_list.append(zeta88)
			z8 = 1
		except:
			z8 = 0
	if z8 == 1:
		return target_list, zeta3
	else:
		return None, None

def replace_abv(nome_time):
	if "AFC " in nome_time:
		j = nome_time.replace("AFC ", "")
	elif " AFC" in nome_time:
		j = nome_time.replace(" AFC", "")
	elif "FC " in nome_time:
		j = nome_time.replace("FC ", "")
	elif " FC" in nome_time:
		j = nome_time.replace(" FC", "")
	else:
		j = nome_time
	return j

def selecting_matchs_by_data(url, dt3, dt2, dt, liga_url, j1, special_dates):
	# pdb.set_trace()
	deltachampions = timedelta(days=40)
	global u0
	if dt3 > dt and dt3 < dt2:

		if liga_url in url:
			if len(special_dates) >= 1:
				if len(special_dates) < 2:
					if dt3 >= special_dates[0]:
						v = 1
						data3 = dt3

						# marcador de etapa do campeonato (copas e playoffs) no campeonato
						j1 = 3
						if "champions-league" in url:
							if ((dt3 - special_dates[0]) >= deltachampions):
								u0 = 1

					else:
						if "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "eng-playoff" in url:
							j1=0
							v=1
							data3=dt3

				elif len(special_dates) < 3:
					if dt3 >= special_dates[0] and dt3 < special_dates[1]:
						v = 1
						data3 = dt3
						j1 = 3
				# gambiarra para marcar as quartas para tratamento especial novo de pegar jogos não ingleses
						if "champions-league" in url:
							if ((dt3 - special_dates[0]) >= deltachampions):
								u0 = 1

					elif dt3 >= special_dates[1]:
						v = 1
						data3 = dt3
						j1 = 1

					else:
						if "champions-league" in url or "europa-league" in url or "europa-conference-league" in url:
							j1=0
							v=1
							data3=dt3


				elif len(special_dates) < 4:
					if dt3 >= special_dates[0] and dt3 < special_dates[1]:
						v = 1
						data3 = dt3
						j1 = 3
						if "champions-league" in url:
							if ((dt3 - special_dates[0]) >= deltachampions):
								u0 = 1

					elif dt3 >= special_dates[1] and dt3 < special_dates[2]:
						v = 1
						data3 = dt3
						j1 = 1


					elif dt3 == special_dates[2]:
						v=1
						data3 = dt3
						j1=2

					else:
						if "champions-league" in url or "europa-league" in url or "europa-conference-league" in url:
							j1=0
							v=1
							data3=dt3


		else:
			v=1
			data3 = dt3
			j1=0

	elif (dt3 < dt or dt3 > dt2):
		v = 2
		if (j1 != 2 and j1 != 1 and j1 != 3):
			j1 = 0


	if 'data3' in locals():
		return v, j1, data3
	else:
		return v, j1, None



def set_date(data3, j, Rivalidades, contador, tags):
	# for u0 in Rivalidades:
	# 	if j in u0:
	esquema = []
	if j in Rivalidades[0] or j in Rivalidades[1] or j in Rivalidades[2] or j in Rivalidades[3]:
		if contador % 2 == 0:
			esquema = tags.find_previous_sibling('td')
			# try except para o caso de não ter ainda a hora disponível do jogo
			try:
				hora_reino_unido = datetime.strptime(esquema.text, '%H:%M')
				hora_brasil = hora_reino_unido - timedelta(hours=4)
				hora_brasil_str = datetime.strftime(hora_brasil, '%H:%M')
			except:
				print("hora ainda nao definida, setada como padrão, meio dia")
				hora_brasil = datetime.strptime('12:00', '%H:%M')
				hora_brasil_str = hora_brasil.strftime('%H:%M')
				# hora_brasil_str = datetime.strftime('12:00', '%H:%M')
			datax = datetime.fromisoformat(str(data3))
			dia_mes_str = datax.strftime('%d/%m')
		contador = contador + 1
		# garantindo que não vai apender o j em toda e qualquer situação fora da função
		time0 = j
	# else:
	# 	continue
	# if len(esquema) > 0:
	# if len()
	if contador % 2 == 1:
		return time0, hora_brasil_str, dia_mes_str, contador
	else:
		return time0, None, None, contador
	# elif len(time0) > 1:

	# 	return time0, None, None, contador
	# else:
	# 	return None, None, None, None

# Importando arquivo de rivais, pode ser editável na estrutura atual
with open('Rivals.yml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

with open('Configuracoes.yml', 'r') as f:
	data2 = yaml.load(f, Loader=yaml.FullLoader)



Rivalidades_Inglaterra = data['Rivalidades_Inglaterra']
Rivalidades_Escocia = data['Rivalidades_Escocia']
Times_sem_rivais = data['Times_sem_rivais']
# Inicio_Rodada = data2['Inicio_Rodada']

Rivalidades= [Rivalidades_Inglaterra, Rivalidades_Escocia, Times_sem_rivais]
times_desconsiderados = {}

# cur.execute('SELECT MAX(id) FROM Keywords')
headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'}
url = sys.argv[11]

f = 0
result = []

rescheduling = []
rescheduling_count = 0

champstring, stagestring, liga, liga_url, url_times_world_diferentes, url_times_eng_sco_diferentes = selection_liga(url, data2)

# Verificando se é um dos campeonatos nos quais os times podem estar não listados nas listas de rivais
if url_times_world_diferentes == url_times_eng_sco_diferentes:
	f=0
elif url_times_eng_sco_diferentes != "z":
	f=0
	req = urllib.request.Request(url_times_eng_sco_diferentes, headers=headers)
	html2 = urllib.request.urlopen(req, context=ctx).read()
	soup = BeautifulSoup(html2, 'lxml')
	body2 = soup.findAll('tr')
	for tag in body2:
			a = 1
			try:
				x = tag.find_all('td')
				# pdb.set_trace()
				time_champions = x[1].find('a').text
				# print(time_champions)

				time2 = replace_abv(time_champions)

				if time2 not in Rivalidades[0] and time2 not in Rivalidades[1] and time2 not in Rivalidades[2]:
					times_desconsiderados[time2] = ['Sem rival']

			except:
				continue

	Rivalidades.append(times_desconsiderados)

elif url_times_world_diferentes != "z":
	f=1
	req = urllib.request.Request(url_times_world_diferentes, headers=headers)
	html2 = urllib.request.urlopen(req, context=ctx).read()
	soup = BeautifulSoup(html2, 'lxml')
	body2 = soup.findAll('tr')
	for tag in body2:
			a = 1
			try:
				x = tag.find_all('td')
				# pdb.set_trace()
				time_champions = x[1].find('a').text
				# print(time_champions)

				time2 = replace_abv(time_champions)

				if time2 not in Rivalidades[0] and time2 not in Rivalidades[1] and time2 not in Rivalidades[2]:
					times_desconsiderados[time2] = ['Sem rival']

			except:
				continue
	Rivalidades.append(times_desconsiderados)


req = urllib.request.Request(url, headers=headers)
html1 = urllib.request.urlopen(req, context=ctx).read()


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
# dt = datetime(2023, 4, 12, 20, 30, tzinfo=gmt)
# dt2 = datetime(2023, 4, 21, 20, 30, tzinfo=gmt)

v = 2

jogos_semana = []
time = []
jogos = []
hora = []
dia = []
peso = []

contador = 0
contadorx=0
special_dates = []
datas_playoffs_sco = []
datas_playoffs_eng = []
z8 = 0
z22 = 0
#variable to define filter situations ahead
j1=0
datas_eng_fa_cup = []
datas_eng_league_cup = []
js = []
contador1 = 0

# Verificando se é uma copa ou campeonato que exija tratamento especial quanto a datas
for tag in body:
	# Tentando garantir que ele só pegue a partir de um certo estágio se for playoff ou copa, nessa etapa ele seta datas específicas para acontecimentos específicos. Só deve realizar essa etapa uma vez, por isso o contador.
	if contador1 == 0:
		if "sco-playoff" in url:
			target_list, zeta3 = extends_cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_playoffs_sco.extend(target_list)
				# AQUI QUE REVERTE CASO QUEIRA ADICIONAR OS DOIS JOGOS
				# special_dates.extend(target_list)
				if len(target_list) == 2:
					special_dates.append(target_list[1])
				elif len(target_list) == 1:
					special_dates.append(target_list[0])

				contador1 = 1
		elif "eng-playoff" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_playoffs_eng.extend(target_list)
				special_dates.extend(target_list)
				contador1 = 1

		#Pegando a data de início do bolão pra usar de referência em outros campeonatos
		elif "eng-fa-community" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_playoffs_eng.extend(target_list)
				inicio_bolao = target_list[0]
				special_dates.extend(target_list)
				contador1 = 1

	if contador1 <= 2:
		if "eng-fa-cup" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "eng-league-cup" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "sco-fa-cup" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "sco-league-cup" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "champions-league" in url and "champions-league-qual" not in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "europa-league" in url and "europa-league-qual" not in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "europa-conference-league" in url and "europa-conference-league-qual" not in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1

		elif "klub-wm" in url:
			target_list, zeta3 = cups_after(url, champstring, tag, stagestring)
			if target_list != None:
				# datas_eng_fa_cup.extend(target_list)
				special_dates.extend(target_list)
				contador1 = contador1 + 1


v=2
# Selecionando a partida pelas datas, inclusive considerando as datas especiais evocadas na última parte
for tag in body:
	a=1

	try:
		x = tag.find_all('td')
		for tags in x:
			try:
				if tags.find('a') is None:
					continue

				y = tags.find('a').text
				dt3 = gmt.localize(datetime.strptime(y, "%d/%m/%Y"))

				#Selecionando a parte do campeonanto que vamos pegar, tratamento especial para copas

				v, j1, data3 = selecting_matchs_by_data(url, dt3, dt2, dt, liga_url, j1, special_dates)


			except:
				if v == 1:
					if time_or_result(y) == "Result":
						result.append(y)
						rescheduling_count = rescheduling_count + 1
					elif time_or_result(y) == "postponed":
						rescheduling.append(rescheduling_count)
						rescheduling_count = rescheduling_count + 1
						result.append(y)
					else:
						j = replace_abv(y)

						# montando os jogos com as datas setadas
						time0, hora_brasil_str, dia_mes_str, contador = set_date(data3, j, Rivalidades, contador, tags)
						if hora_brasil_str != None:
							time.append(time0)
							hora.append(hora_brasil_str)
							dia.append(dia_mes_str)
						elif time0 != None:
							time.append(time0)
						else:
							continue

				elif v == 2:
					continue
				else:
					continue
	except:
		continue

# Montando Jogos e slecionando peso de derbies
for x in range(len(time)):
	if x % 2 == 0:
		for y in range(len(Rivalidades)):

			try:
				if time[x+1] in Rivalidades[y][(time[x])]:
					peso.append('P2')

				else:
					peso.append('P1')

			except:
				continue
		jogos.append(time[x] + " x " + time[x+1])

		jogos_semana.append(jogos[contadorx] + " - " + peso[contadorx] + " (" + liga + ") - " + dia[contadorx] + " - " +hora[contadorx]+" zzz"+ result[contadorx])
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

# Removing rescheduled game
if len(rescheduling) > 0:
	for index in reversed(range(len(rescheduling))):
		del jogos_semana[int(rescheduling[index])]

# Casos especiais em que os times não estão nas listas de times ingleses e escoceses, se nenhum dos times do jogo está nessas listas, o jogo é removido
for u in range(len(time)):
	if u % 2 == 0:
		# print(time[u])
		if not time[u] in Rivalidades[0] and not time[u+1] in Rivalidades[0] and not time[u] in Rivalidades[1] and not time[u+1] in Rivalidades[1] and not time[u] in Rivalidades[2] and not time[u+1] in Rivalidades[2]:

			lista_delete_time.extend([u, u+1])
			lista_delete_peso.append(int(u/2))
			lista_delete_jogos.append(int(u/2))
			lista_delete_dia.append(int(u/2))
			lista_delete_hora.append(int(u/2))
			lista_delete_jogos_semana.append(int(u/2))

			# print(time[u])
	# contadory = contadory + 1
	# print(u)

# Removendo times não ingleses e não escoceses seguindo critério do último comentário
timef = [elem for idx, elem in enumerate(time) if idx not in lista_delete_time]

# Removendo jogos não ingleses e não escoceses seguindo critério do último comentário
jogos_semana_f = [elem for idx, elem in enumerate(jogos_semana) if idx not in lista_delete_jogos_semana]

# print(time)

if 'inicio_bolao' in globals():
	print(inicio_bolao)

# pdb.set_trace()

if f == 1 and u0 == 0:
# if f == 1:
	if (j1 == 1 and (("europa-league" in url and "europa-league-qual" not in url) or ("champions-league" in url and "champions-league-qual" not in url))) or ( j1 == 2 and (("europa-conference-league" in url and "europa-conference-league-qual" not in url) or ("europa-league" in url and "europa-league-qual" not in url) or ("champions-league" in url and "champions-league-qual" not in url))):
		for index, y in enumerate(jogos_semana):
			try:
				print(y)
			except:
				print("Time com caracteres especiais, buscar manualmente")


		if j1==1:
			if len(jogos_semana) > 0:
				print("j1=1")

		elif j1==2:
			if len(jogos_semana) > 0:
				print("j1=2")
		elif j1==3 and ("eng-fa-cup" in url or "eng-league-cup" in url or "sco-fa-cup" in url or "sco-league-cup" in url or "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "klub-wm" in url or "eng-playoff" in url) and "champions-league-qual" not in url and "europa-league-qual" not in url and "europa-conference-league-qual" not in url:
			if len(jogos_semana) > 0:
				print("j1=3")
		elif ("eng-fa-cup" in url or "eng-league-cup" in url or "sco-fa-cup" in url or "sco-league-cup" in url or "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "klub-wm" in url) and j1==0 and "champions-league-qual" not in url and "europa-league-qual" not in url and "europa-conference-league-qual" not in url:
			if len(jogos_semana) > 0:
				print("j1=0")




	else:
		for index, y in enumerate(jogos_semana_f):
			try:
				print(y)
			except:
				print("Time com caracteres especiais, buscar manualmente")

		if j1==1:
			if len(jogos_semana_f) > 0:
				print("j1=1")

		elif j1==2:
			if len(jogos_semana_f) > 0:
				print("j1=2")
		elif j1==3 and ("eng-fa-cup" in url or "eng-league-cup" in url or "sco-fa-cup" in url or "sco-league-cup" in url or "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "klub-wm" in url or "eng-playoff" in url) and "champions-league-qual" not in url and "europa-league-qual" not in url and "europa-conference-league-qual" not in url:
			if len(jogos_semana_f) > 0:
				print("j1=3")
		elif ("eng-fa-cup" in url or "eng-league-cup" in url or "sco-fa-cup" in url or "sco-league-cup" in url or "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "klub-wm" in url) and j1==0 and "champions-league-qual" not in url and "europa-league-qual" not in url and "europa-conference-league-qual" not in url:
			if len(jogos_semana_f) > 0:
				print("j1=0")



if f == 0 or u0 == 1:
# if f == 0:
	for index, y in enumerate(jogos_semana):
		try:
			print(y)
		except:
			print("Time com caracteres especiais, buscar manualmente")
	if j1==1:
		if len(jogos_semana) > 0:
			print("j1=1")

	elif j1==2:
		if len(jogos_semana) > 0:
			print("j1=2")
	elif j1==3 and ("eng-fa-cup" in url or "eng-league-cup" in url or "sco-fa-cup" in url or "sco-league-cup" in url or "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "klub-wm" in url or "eng-playoff" in url) and "champions-league-qual" not in url and "europa-league-qual" not in url and "europa-conference-league-qual" not in url:
		if len(jogos_semana) > 0:
			print("j1=3")
	elif ("eng-fa-cup" in url or "eng-league-cup" in url or "sco-fa-cup" in url or "sco-league-cup" in url or "champions-league" in url or "europa-league" in url or "europa-conference-league" in url or "klub-wm" in url) and j1==0 and "champions-league-qual" not in url and "europa-league-qual" not in url and "europa-conference-league-qual" not in url:
		if len(jogos_semana) > 0:
			print("j1=0")




