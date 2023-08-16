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



	return returnVariable, result

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

	# elif championshipName == "SPFL_PLAYOFFS":
	# 	from filtro_SPFL_championship_relegation_func import main_SPFL_champ_rele
	# 	result = main_SPFL_champ_rele(result)

	return result

def run_championship_plus_filter(dt, dt2, url, championshipName):

	returnVariable, result = run_championship(dt, dt2, url, championshipName)

	if len(result) == 0:
		returnVariable.append("Nenhum resultado para " + championshipName)

	else:

		result = championship_filter(championshipName, result)

		if len(result) > 0:
			sorted_Jogos = sorted(result, key=lambda s: tuple(s.split(' - ')[-2:]))
			returnVariable.append(sorted_Jogos)
		else:
			returnVariable.append("Filtro não retornou nenhum jogo para ", championshipName)

	return returnVariable

def run_championship_worker(queue, dt, dt2, url, championshipName):
	returnVariable, result = run_championship(dt, dt2, url, championshipName)
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
		if championshipName == "SPFL_championship_relegation" or championshipName == "SPFL_relegation" or championshipName == "SPFL_PLAYOFFS":
			t = threading.Thread(target=run_championship_worker, args=(result_queue_deep, dt, dt2, urls[idx], championshipName))
			threads_deep.append(t)
			t.start()
			championshipNames_deep.append(championshipName)
		elif championshipName == "SPFL_PLAYOFFS":
			t = threading.Thread(target=run_championship_worker, args=(result_queue_deep, dt, dt2, urls[idx], championshipName))
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

	if "SPFL_championship_relegation" in championshipNames:
		returnVariable = []
		result_deep = []

		for championshipName, result, returnVariable_ in results_deep:
			if championshipName == "SPFL_championship_relegation" or championshipName == "SPFL_relegation":
				result_deep.extend(result)
				returnVariable.extend(returnVariable_)

# special treatment for double order double thread
		if len(result_deep) != 0:
			t = threading.Thread(target=championship_filter_worker, args=(result_queue, result_deep, "SPFL_championship_relegation"))
			threads.append(t)
			t.start()

		else:
			results.append(list(("SPFL_championship_relegation", returnVariable)))

	elif "SPFL_PLAYOFFS" in championshipNames:
		returnVariable = []
		result_deep = []
		(championshipName, result, returnVariable_) = results_deep[0]
		returnVariable.extend(returnVariable_)
		if result != []:
			returnVariable.append(result)
		result_SPFL_PLAY = ["SPFL_PLAYOFFS", returnVariable]

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
					# print(a)
					temp_name, temp_result = a
					results[count_].insert(0, temp_name)
					print(results)
					results[count_][1].insert(0, returnVariable[0])
					print(results)
					sorted_results = sorted(temp_result, key=lambda s: tuple(s.split(' - ')[-2:]))
					results[count_][1][1].extend(sorted_results)
		count_ = count_ + 1

	if "SPFL_PLAYOFFS" in championshipNames:
		results.append(result_SPFL_PLAY)


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
			# # Start fourth program



	if data0['FAC'] == 1:
		# # Start fifth program
		result5 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_FAC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		if result5.returncode != 0:
			print(result5.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result5.stdout != '':
				zz=0
				variavel = result5.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					print('Jogo FAC anterior ao Round 3, nao adicionado')
					temp = []
				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")
					print('Jogo FAC encaminhado ao filtro')
				elif "j1=1" in temp:
					temp.remove("j1=1")
					index1 = 0
					print('Jogo FAC semi-final adicionado')
					temp = subst_P("P1", "P2", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					print('Jogo FAC final adicionado')
					temp = subst_P("P1", "P3", temp)
					temp = subst_P("P2", "P3", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)
				# print(temp)
				if len(temp) > 0 and zz == 2:
					print(temp)
					result5_1 = subprocess.run(['python', 'filtro_FAC.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
						# # var_dump.var_dump(variavel[0])
						# print(result3_1.stdout)
					variavel = result5_1.stdout.split('\n')
					while "" in variavel:
						variavel.remove("")
					# print(variavel)
					sorted_Jogos = sorted(variavel, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para FAC')


	if data0['EFL'] == 1:
		result6 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_EFL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		if result6.returncode != 0:
			print(result6.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result6.stdout != '':
				zz=0
				variavel = result6.stdout.split('\n')
				for o in variavel:
						temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					print('Jogo EFL anterior as oitavas, nao adicionado')
					temp = []
				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")
					print('Jogo EFL encaminhado ao filtro')
				elif "j1=1" in temp:
					temp.remove("j1=1")
					print('Jogo EFL semi-final adicionado')
					temp = subst_P("P1", "P2", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					print('Jogo EFL final adicionado')
					temp = subst_P("P1", "P3", temp)
					temp = subst_P("P2", "P3", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)
				# print(temp)
				if len(temp) > 0 and zz == 2:
					result6_1 = subprocess.run(['python', 'filtro_FAC.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

					variavel = result6_1.stdout.split('\n')
					while "" in variavel:
						variavel.remove("")
					# print(variavel)
					sorted_Jogos = sorted(variavel, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para EFL')


	if data0['SC'] == 1:
		result7 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		if result7.returncode != 0:
			print(result7.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result7.stdout != '':
				zz=0
				variavel = result7.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					print('Jogo SC anterior as quartas, nao adicionado')
					temp = []
				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")
					print('Jogos SC quartas-de-final adicionados')
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=1" in temp:
					temp.remove("j1=1")
					print('Jogo SC semi-final adicionado')

					temp = subst_P("P1", "P2", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					print('Jogo SC final adicionado')

					temp = subst_P("P1", "P3", temp)

					temp = subst_P("P2", "P3", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para SC')


	if data0['SLC'] == 1:
		result8 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SLC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		if result8.returncode != 0:
			print(result8.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result8.stdout != '':
				zz=0
				variavel = result8.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					print('Jogo SLC anterior as quartas, nao adicionado')
					temp = []
				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")
					print('Jogos SLC quartas-de-final adicionados')
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=1" in temp:
					temp.remove("j1=1")
					index1 = 0
					print('Jogo SLC semi-final adicionado')
					temp = subst_P("P1", "P2", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					index1=0
					print('Jogo SLC final adicionado')

					temp = subst_P("P1", "P3", temp)
					temp = subst_P("P2", "P3", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para SLC')

	if data0['USC'] == 1:
		result9 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_USC], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		index1 = 0
		# Wait for the program to finish
		if result9.returncode != 0:
			print(result9.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result9.stdout != '':
				zz=0
				variavel = result9.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")

				temp = subst_P("P1", "P2", temp)

				print("Jogo adicionado para USC")

				temp = after_FACS_filter(temp, inicio_bolao_date)

				sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
				for o in sorted_Jogos:
					Jogos.append(o)

			else:
				print('Nenhum resultado para USC')

	if data0['QUAL_UCL'] == 1:
		result10 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_QUAL_UCL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		index1 = 0
		# Wait for the program to finish
		if result10.returncode != 0:
			print(result10.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result10.stdout != '':
				zz=0
				variavel = result10.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")

				print("Jogo encaminhado ao filtro para qualificatorias UCL")

				temp = after_FACS_filter(temp, inicio_bolao_date)

				temp = subst_P("P2", "P1", temp)

				sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
				for o in sorted_Jogos:
					Jogos.append(o)

			else:
				print('Nenhum resultado para QUAL-UCL')


	if data0['UCL'] == 1:
		result11 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_UCL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		# Wait for the program to finish
		if result11.returncode != 0:
			print(result11.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result11.stdout != '':
				zz=0
				variavel = result11.stdout.split('\n')
				for o in variavel:
						temp.append(o)
				while "" in temp:
					temp.remove("")
				# print(temp)
				if "j1=0" in temp:
					temp.remove("j1=0")
					print('Jogo UCL adicionado')

					# pdb.set_trace()
					temp = subst_P("P2", "P1", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=3" in temp:
					zz=2
					temp.remove("j1=3")

					temp = subst_P("P1", "P2", temp)

					print('Jogo UCL oitavas/quartas adicionado')

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

				elif "j1=1" in temp:
					temp.remove("j1=1")
					index1 = 0
					print('Jogo UCL semi-final adicionado')
					temp = subst_P("P1", "P3", temp)
					temp = subst_P("P2", "P3", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)


				elif "j1=2" in temp:
					temp.remove("j1=2")
					index1=0
					print('Jogo UCL final adicionado')

					temp = subst_P("P1", "P4", temp)
					temp = subst_P("P2", "P4", temp)

					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)

			else:
				print('Nenhum resultado para UCL')



	if data0['QUAL_UEL'] == 1:
		result12 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_QUAL_UEL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		temp=[]
		variavel=[]
		index1 = 0
		# Wait for the program to finish
		if result12.returncode != 0:
			print(result12.stderr)
		else:
			# Print the stdout output if the subprocess ran successfully
			if result12.stdout != '':
				zz=0
				variavel = result12.stdout.split('\n')
				for o in variavel:
					temp.append(o)
				while "" in temp:
					temp.remove("")

				print("Jogo encaminhado ao filtro para qualificatorias UEL")

				temp = after_FACS_filter(temp, inicio_bolao_date)

				if len(temp) > 0:
					temp = subst_P("P2", "P1", temp)
					sorted_Jogos = sorted(temp, key=lambda s: tuple(s.split(' - ')[-2:]))
					for o in sorted_Jogos:
						Jogos.append(o)
			else:
				print('Nenhum resultado para QUAL-UEL')



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