# import var_dump
import subprocess
import yaml
from datetime import datetime, timedelta
import pytz
import sqlite3
# import pdb
# import sys
import threading
import queue
from buscador_jogosv3_func import main_buscador_jogosv3

# Global variables
gmt = pytz.timezone('GMT')

def weights(championshipName, returnVariable, result):
	bool_call_filter = True
	if championshipName == "FAC" or championshipName == "EFL" or championshipName == "SC" or championshipName == "SLC" or championshipName == "UCL":
			if "j1=3" in result:
				bool_call_filter = True
				if championshipName == "SC" or championshipName == "SLC":
					bool_call_filter = False
					result.remove("j1=3")
				elif championshipName == "UCL":
					bool_call_filter = False
					result.remove("j1=3")
					result = subst_P("P1", "P2", result)

			elif "j1=1" in result:
				returnVariable.append("SEMI-FINAL")
				result.remove("j1=1")
				result = subst_P("P1", "P2", result)
				bool_call_filter = False
				if championshipName == "UCL":
					result = subst_P("P2", "P3", result)

			elif "j1=2" in result:
				returnVariable.append("FINAL")
				result.remove("j1=2")
				result = subst_P("P1", "P3", result)
				result = subst_P("P2", "P3", result)
				bool_call_filter = False
				if championshipName == "UCL":
					result = subst_P("P3", "P4", result)

			elif "j1=0" in result:
				if championshipName == "FAC":
					returnVariable.append("Jogo anterior ao terceiro round não adicionado")
					result = []
				elif championshipName == "EFL":
					returnVariable.append("Jogo anterior as oitavas não adicionado")
					result = []
				elif championshipName == "SC":
					returnVariable.append("Jogo anterior as quartas não adicionado")
					result = []
				elif championshipName == "UCL":
					result = subst_P("P2", "P1", result)
				bool_call_filter = False

	elif championshipName == "SPFL_PLAYOFFS":
		result = subst_P("P1", "P2", result)
		bool_call_filter = False

	elif championshipName == "LCH_PLAYOFFS":
		if "j1=3" in result:
			result.remove("j1=3")
			result[(len(result)-1)] = result[(len(result)-1)].replace("P1", "P3")
		result = subst_P("P1", "P2", result)
		bool_call_filter = False

	elif championshipName == "USC":
		bool_call_filter = False
		result = subst_P("P1", "P2", result)
		result = after_FACS_filter(result, inicio_bolao_date)

	elif championshipName == "QUAL_UCL" or championshipName == "QUAL_UCL":
		bool_call_filter = False
		result = subst_P("P2", "P1", result)
		result = after_FACS_filter(result, inicio_bolao_date)




	return returnVariable, result, bool_call_filter

def custom_key(match):
    parts = match.split(' - ')
    date_parts = parts[-2].split('/')
    day = int(date_parts[0])
    month = int(date_parts[1])
    time = parts[-1]
    return (month, day, time)

def load_data(filename):
	with open(filename, 'r') as f:
		return yaml.load(f, Loader=yaml.FullLoader)

def load_data_worker(queue, filename):
	result = load_data(filename)
	queue.put((filename,result))

def get_configs(filenames):
	result_queue = queue.Queue()
	threads = []

	for filename in filenames:
		t = threading.Thread(target=load_data_worker, args=(result_queue, filename))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()

	results = []

	while not result_queue.empty():
		results.append(result_queue.get())

	results.sort(key=lambda x: filenames.index(x[0]))

	(a, data), (b, data0), (c, data1) = results

	return data, data0, data1

def run_championship(dt, dt2, url, championshipName):

	result = main_buscador_jogosv3(dt, dt2, url)

	returnVariable = []

	# Wait for the program to finish
	if len(result) == 0:
		returnVariable.append("Nenhum resultado para " + championshipName)

	else:
		while "hora ainda nao definida, setada como padrão, meio dia" in result:
			returnVariable.append("hora ainda nao definida, setada como padrão, meio dia")
			result.remove("hora ainda nao definida, setada como padrão, meio dia")
		returnVariable.append("Jogos " + championshipName + " encaminhados para o filtro")

	bool_call_filter = True

	if championshipName in ["FAC", "SPFL_PLAYOFFS", "LCH_PLAYOFFS", "EFL", "SC", "SLC", "USC", "QUAL_UCL", "UCL", "QUAL_UEL"]:
		returnVariable, result, bool_call_filter = weights(championshipName, returnVariable, result)


	return returnVariable, result, bool_call_filter

def championship_filter(championshipName, result):

	if championshipName == "PL":
		from filtro_PL_func import main_filtro_PL
		result = main_filtro_PL(result)

	elif championshipName == "SPFL":
		from filtro_SPFL_func import main_filtro_spfl
		result = main_filtro_spfl(result)

	elif championshipName == "SPFL_championship_relegation" or championshipName == "SPFL_relegation":
		from filtro_SPFL_championship_relegation_func import main_SPFL_champ_rele
		result = main_SPFL_champ_rele(result)

	elif championshipName == "LCH":
		from filtro_LCH_func import main_filtro_LCH
		result = main_filtro_LCH(result)

	elif championshipName == "FAC" or championshipName == "EFL":
		if "j1=3" in result:
			from filtro_FAC_func import main_filtro_FAC
			result.remove("j1=3")
			result = main_filtro_FAC(result)

	# elif championshipName == "SPFL_PLAYOFFS":
	# 	from filtro_SPFL_championship_relegation_func import main_SPFL_champ_rele
	# 	result = main_SPFL_champ_rele(result)

	return result

def run_championship_plus_filter(dt, dt2, url, championshipName):

	returnVariable, result, bool_call_filter = run_championship(dt, dt2, url, championshipName)

	if len(result) == 0:
		returnVariable.append("Nenhum resultado para " + championshipName)

	else:
		# By coding standard I would like to evaluate the weight ("Ps") of the matchs in the end of the program, but here is a multi threading environment complex to build, so I will use tha maximum I can.

		if bool_call_filter == True:
			result = championship_filter(championshipName, result)

		if len(result) > 0:
			# Sort by date
			# print(result)
			sorted_Jogos = sorted(result, key=custom_key)
			returnVariable.append(sorted_Jogos)
		else:
			returnVariable.append("Filtro não retornou nenhum jogo para ", championshipName)

	return returnVariable

def run_championship_worker(queue, dt, dt2, url, championshipName):
	returnVariable, result, bool_call_filter  = run_championship(dt, dt2, url, championshipName)
	queue.put((championshipName, result, returnVariable))

def run_championship_plus_filter_worker(queue, dt, dt2, url, championshipName):
	result = run_championship_plus_filter(dt, dt2, url, championshipName)
	queue.put((championshipName, result))

def championship_filter_worker(queue, result, championshipName):
	result = championship_filter(championshipName, result)
	queue.put((championshipName, result))

def get_championships(dt, dt2, urls, championshipNames):
	result_queue = queue.Queue()
	result_queue_deep = queue.Queue()
	results = []
	threads = []
	threads_deep = []
	championshipNames_ = []
	championshipNames_deep = []
	for idx, championshipName in enumerate(championshipNames):
		#  special treatment for double order double thread
		if championshipName == "SPFL_championship_relegation" or championshipName == "SPFL_relegation" or championshipName == "SPFL_PLAYOFFS" or championshipName == "LCH_PLAYOFFS":
			t = threading.Thread(target=run_championship_worker, args=(result_queue_deep, dt, dt2, urls[idx], championshipName))
			threads_deep.append(t)
			t.start()
			championshipNames_deep.append(championshipName)

		else:
			t = threading.Thread(target=run_championship_plus_filter_worker, args=(result_queue, dt, dt2, urls[idx], championshipName))
			threads.append(t)
			t.start()
			championshipNames_.append(championshipName)

	for t in threads_deep:
		t.join()


	results_deep = []

	while not result_queue_deep.empty():
		results_deep.append(result_queue_deep.get())

	results_deep.sort(key=lambda x: championshipNames_deep.index(x[0]))

	playoffs = []
	if "SPFL_championship_relegation" in championshipNames or "SPFL_PLAYOFFS" in championshipNames or "LCH_PLAYOFFS" in championshipNames:
		returnVariable = []
		result_deep = []

		for championshipName, result, returnVariable_ in results_deep:
			return_Variable2 = []
			if championshipName == "SPFL_championship_relegation" or championshipName == "SPFL_relegation":
				result_deep.extend(result)
				returnVariable.extend(returnVariable_)
			elif "SPFL_PLAYOFFS" in championshipNames or "LCH_PLAYOFFS" in championshipNames:
				return_Variable2.extend(returnVariable_)
				if result != []:
					return_Variable2.append(result)

				if championshipName == "SPFL_PLAYOFFS":
					result_SPFL_PLAY = ["SPFL_PLAYOFFS", return_Variable2]
					playoffs.append(result_SPFL_PLAY)
				elif championshipName == "LCH_PLAYOFFS":
					result_LCH_PLAY = ["LCH_PLAYOFFS", return_Variable2]
					playoffs.append(result_LCH_PLAY)

		# special treatment for double order double thread
		if len(result_deep) != 0:
			t = threading.Thread(target=championship_filter_worker, args=(result_queue, result_deep, "SPFL_championship_relegation"))
			threads.append(t)
			t.start()

		elif "SPFL_championship_relegation" in championshipNames:
			results.append(list(("SPFL_championship_relegation", returnVariable)))


	for t in threads:
		t.join()

	count_ = 0

	while not result_queue.empty():
		a = list(result_queue.get())
		if a[0] != "SPFL_championship_relegation":
			results.append(a)

		# Special treatment for championships that got double threaded
		else:
			if "SPFL" not in championshipNames:
				if len(result_deep) !=0 and a[0] == "SPFL_championship_relegation":
					results.append([[[]]])
					temp_name, temp_result = a
					results[count_].insert(0, temp_name)
					results[count_][1].insert(0, returnVariable[0])
					sorted_results = sorted(temp_result, key=lambda s: tuple(s.split(' - ')[-2:]))
					results[count_][1][1].extend(sorted_results)
		count_ = count_ + 1

	if len(playoffs) > 0:
		for matchs in playoffs:
			results.append(matchs)


	if "SPFL_relegation" in championshipNames:
		championshipNames.remove("SPFL_relegation")

	# print(results)

	results.sort(key=lambda x: championshipNames.index(x[0]))

	return results

def after_FACS_filter(variavel, inicio_bolao_date):
	current_year = datetime.now().year
	horarios_filtrados = []
	horarios_filtrados_date_time = []
	index_delete=[]
	# pdb.set_trace()
	for index in range(len(variavel)):
		horarios_filtrados.append(variavel[index].split(" - ")[2].strip())
		horarios_filtrados_date_time.append(datetime.strptime(horarios_filtrados[index], "%d/%m"))
		horarios_filtrados_date_time[index] = horarios_filtrados_date_time[index].replace(year=current_year)
		horarios_filtrados_date_time[index] = gmt.localize(horarios_filtrados_date_time[index])
		if horarios_filtrados_date_time[index] < inicio_bolao_date:
			print(horarios_filtrados_date_time[index])
			print(inicio_bolao_date)
			index_delete.append(index)

	variavel = [value for index, value in enumerate(variavel) if index not in index_delete]
	return variavel

def subst_P(peso, peso_replace, temp):
	index1 = 0
	if len(temp) > 0:
		while peso in temp[index1]:
			temp[index1] = temp[index1].replace(peso, peso_replace)
			if index1 < (len(temp)-1):
				index1=index1 + 1
	return temp

def get_dates(data_begin, data_end):
	dt = []
	dt2 = []

	for numeros in data_begin:
		dt.append(int(numeros))

	for numeros in data_end:
		dt2.append(int(numeros))

	dt = datetime(*dt, tzinfo=gmt)
	dt2 = datetime(*dt2, tzinfo=gmt)

	return dt, dt2

def main():

	filenames = ['Configuracoes.yml', 'Ativar_Desativar_campeonatos.yml', 'tabelas.yml']

	championshipNames = []

	data, data0, data1 = get_configs(filenames)

	# Getting the dates from the begining and end of the round from the configuration files
	dt, dt2 = get_dates(data['Inicio_Rodada'], data['Fim_Rodada'])

	# Printing the capturing starting date
	print("Data inicial de captura: ", dt)

	# Printing the capturing ending date
	print("Data final de captura: ", dt2)

	# dt = datetime(*data['Inicio_Rodada'], tzinfo=gmt)
	# dt2 = datetime(*data['Fim_Rodada'], tzinfo=gmt)
	url_FACS = data['URL_FACS']
	url_PL = data['URL_PL']
	url_SPFL = data['URL_SPFL']
	url_SPFL_championship = data['URL_SPFL_CHAMPIONSHIP']
	url_SPFL_relegation = data['URL_SPFL_RELEGATION']
	url_SPFL_PLAYOFFS = data['URL_SPFL_PLAYOFFS']
	url_LCH = data['URL_LCH']
	url_LCH_PLAYOFFS = data['URL_LCH_PLAYOFFS']
	url_FAC = data['URL_FAC']
	url_EFL = data['URL_EFL']
	url_SC = data['URL_SC']
	url_SLC = data['URL_SLC']
	url_USC = data['URL_USC']
	url_QUAL_UCL = data['URL_QUAL_UCL']
	url_UCL = data['URL_UCL']
	url_QUAL_UEL = data['URL_QUAL_UEL']
	url_UEL = data['URL_UEL']
	url_QUAL_UECL = data['URL_QUAL_UECL']
	url_UECL = data['URL_UECL']
	url_FCWC = data['URL_FCWC']

	urls = []

	Tabelas = []
	temp = []
	temp1 = []
	Jogos = []
	Jogos_final = []
	# var_dump.var_dump(dt)

	if data0['TABELAS'] == 1:
		# Start program 0
		from TABELA_CAMPEONATOS_func import main_TABELA_CAMPEONATOS
		main_TABELA_CAMPEONATOS(0) # 0 to NOT print the tables and 1 to print
		print("Tabelas dos campeonatos atualizadas")

	# connect to the database
	conn = sqlite3.connect('championships.db')

	# create a cursor object
	cursor = conn.cursor()

	# Only program not in a multiple thread environment because all other programs need data from here.
	if data0['FACS'] == 1:
		# Start first program
		result = main_buscador_jogosv3(dt, dt2, url_FACS)

		# Print a warning if the function fails
		if len(result) == 0:
			print("Problema na FACS")

		else:
			if len(result) > 0:
				print('Data inicial do bolao capturada')

				while "hora ainda nao definida, setada como padrão, meio dia" in result:
					result.remove("hora ainda nao definida, setada como padrão, meio dia")
					print("hora ainda nao definida, setada como padrão, meio dia")

				# Printing the starting date
				inicio_bolao = result[0]
				print(inicio_bolao)
				global inicio_bolao_date
				inicio_bolao_date = inicio_bolao - timedelta(days=4)

				# Veryfieng if there are any game in the championship for the specified date
				if len(result) > 1:
					print('Jogo adicionado para FACS')
					#
					[result[1]] = subst_P("P1", "P2", [result[1]])
					Jogos.append(result[1])
				else:
					print("Nenhum jogo adicionado para FACS")

			else:
				print('Data inicial do bolao nao capturada')


	if data0['PL'] == 1:
		# # # Start second program
		championshipNames.append("PL")
		urls.append(url_PL)

	if data0['SPFL'] == 1:
		# if resultado < 33:
		if data1['RODADA_SPFL'] <= 33:
			championshipNames.append("SPFL")
			urls.append(url_SPFL)

		elif data1['RODADA_SPFL_CHAMPIONSHIP'] <= 38:
			championshipNames.append("SPFL_championship_relegation")
			urls.append(url_SPFL_championship)
			championshipNames.append("SPFL_relegation")
			urls.append(url_SPFL_relegation)

		else:
			championshipNames.append("SPFL_PLAYOFFS")
			urls.append(url_SPFL_PLAYOFFS)


	if data0['LCH'] == 1:
		if data1['RODADA_LCH'] <= 46:
			championshipNames.append("LCH")
			urls.append(url_LCH)
		else:
			championshipNames.append("LCH_PLAYOFFS")
			urls.append(url_LCH_PLAYOFFS)

	if data0['FAC'] == 1:
		championshipNames.append("FAC")
		urls.append(url_FAC)

	if data0['EFL'] == 1:
		championshipNames.append("EFL")
		urls.append(url_EFL)


	if data0['SC'] == 1:
		championshipNames.append("SC")
		urls.append(url_SC)


	if data0['SLC'] == 1:
		championshipNames.append("SLC")
		urls.append(url_SLC)

	if data0['USC'] == 1:
		championshipNames.append("USC")
		urls.append(url_USC)

	if data0['QUAL_UCL'] == 1:
		championshipNames.append("QUAL_UCL")
		urls.append(url_QUAL_UCL)

	if data0['UCL'] == 1:
		championshipNames.append("UCL")
		urls.append(url_UCL)

	if data0['QUAL_UEL'] == 1:
		championshipNames.append("QUAL_UEL")
		urls.append(url_QUAL_UEL)





	if data0['UEL'] == 1:
		result13 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_UEL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		# pdb.set_trace()
		if result13.returncode != 0:
			print(result13.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result13.stdout != '':
				zz=0
				variavel = result13.stdout.split('\n')
				for o in variavel:
						temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					temp.remove("j1=0")
					print('Jogo UEL adicionado')

					# pdb.set_trace()
					temp = subst_P("P2", "P1", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")

					temp = subst_P("P1", "P2", temp)

					print('Jogo UEL oitavas/quartas adicionado')

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=1" in temp:
					temp.remove("j1=1")
					index1 = 0
					print('Jogo UEL semi-final adicionado')
					temp = subst_P("P1", "P3", temp)
					temp = subst_P("P2", "P3", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					index1=0
					print('Jogo UEL final adicionado')

					temp = subst_P("P1", "P4", temp)
					temp = subst_P("P2", "P4", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para UEL')

	if data0['QUAL_UECL'] == 1:
		result14 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_QUAL_UECL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

		temp=[]
		variavel=[]
		index1 = 0
		# Wait for the program to finish
		if result14.returncode != 0:
			print(result14.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result14.stdout != '':
				zz=0
				variavel = result14.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")

				print("Jogo encaminhado ao filtro para qualificatorias UECL")

				temp = after_FACS_filter(temp, inicio_bolao_date)

				if len(temp) > 0:
					temp = subst_P("P2", "P1", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)
			else:
				print('Nenhum resultado para QUAL-UECL')



	if data0['UECL'] == 1:
		result15 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_UECL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]

		# Wait for the program to finish
		if result15.returncode != 0:
			print(result15.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result15.stdout != '':
				zz=0
				variavel = result15.stdout.split('\n')
				for o in variavel:
						temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					temp.remove("j1=0")
					print('Jogo UECL adicionado')

					# pdb.set_trace()
					temp = subst_P("P2", "P1", temp)


					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")

					temp = subst_P("P2", "P1", temp)

					print('Jogo UECL oitavas/quartas adicionado')

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=1" in temp:
					temp.remove("j1=1")
					index1 = 0
					print('Jogo UECL semi-final adicionado')
					temp = subst_P("P1", "P2", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)



				elif "j1=2" in temp:
					temp.remove("j1=2")
					index1=0
					print('Jogo UECL final adicionado')

					temp = subst_P("P1", "P3", temp)
					temp = subst_P("P2", "P3", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para UECL')



	if data0['FCWC'] == 1:
		result16 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_FCWC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		if result16.returncode != 0:
			print(result16.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result16.stdout != '':
				zz=0
				variavel = result16.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					temp.remove("j1=0")
					print('Jogo anterior a semi FCWC')

					temp = subst_P("P2", "P1", temp)


					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")

					temp = subst_P("P2", "P1", temp)

					print('Jogo FCWC semi adicionado')

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=1" in temp:
					temp.remove("j1=1")
					index1 = 0
					print('Jogo FCWC terceiro adicionado')
					temp = subst_P("P2", "P1", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					index1=0
					print('Jogo FCWC final adicionado')

					temp = subst_P("P1", "P2", temp)


					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para FCWC')

	results = get_championships(dt, dt2, urls, championshipNames)

	print(results)

	# print(Jogos)

	# for o in range(len(sorted_Jogos)):
	# 	sorted_Jogos[o] = sorted_Jogos[o].replace("_QUAL", '')
	# 	print(sorted_Jogos[o])

	for o in range(len(Jogos)):
		Jogos[o] = Jogos[o].replace("_QUAL", '')
		Jogos[o] = Jogos[o].replace("Wolverhampton Wanderers", "Wolverhampton")
		Jogos[o] = Jogos[o].replace("Heart of Midlothian", "Hearts")
		Jogos[o] = Jogos[o].replace("Rosenborg BK", "Rosenborg")

		print(Jogos[o])






	if data0['LANCAR_FORMS'] == 1:
		from forms_func import main2, forms2
		forms2(Jogos)
	# 	process = subprocess.Popen(['python', 'forms.py', *Jogos], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# 	while True:
	# 		line = process.stdout.readline()
	# 		if not line:
	# 			break
	# 		print(line.strip())

	# # Wait for the process to finish and get the return code
	# return_code = process.wait()

		# result17 = subprocess.run(['python', 'forms.py', *Jogos], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

		# if result17.returncode != 0:
		# 	print(result17.stderr)
		# else:
		# 	# Print the stdout output if the subprocess ran successfully
		# 	if result17.stdout != '':
		# 		variavel = result17.stdout.split('\n')
		# 		for o in variavel:
		# 			print(o)


main()