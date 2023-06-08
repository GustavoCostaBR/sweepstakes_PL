import var_dump
import subprocess
import yaml
from datetime import datetime, timedelta
import pytz
import sqlite3
import pdb

with open('Configuracoes.yml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

gmt = pytz.timezone('GMT')
dt = []
dt2 = []
for numeros in data['Inicio_Rodada']:
	dt.append(str(numeros))

for numeros in data['Fim_Rodada']:
	dt2.append(str(numeros))

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


Tabelas = []
temp = []
temp1 = []
Jogos = []
Jogos_final = []
# var_dump.var_dump(dt)

# Start program 0
result0 = subprocess.run(['python', 'TABELA_CAMPEONATOS.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if result0.returncode != 0:
	print(result0.stderr)
else:
    # Print the stdout output if the subprocess ran successfully
	if result0.stdout != '':
		print('Tabela dos campeonatos criada/atualizada')
        # variavel = result0.stdout.split('\n')
        # for o in variavel:
            # Tabelas.append(o)
	else:
		print('Erro provável no subprograma TABELA_CAMPEONATOS.py')
        # var_dump.var_dump(result.stdout)

# print(Tabelas)

# connect to the database
conn = sqlite3.connect('championships.db')

# create a cursor object
cursor = conn.cursor()

# Start first program
result = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_FACS], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Wait for the program to finish
if result.returncode != 0:
	print(result.stderr)
else:
    # Print the stdout output if the subprocess ran successfully
	if result.stdout != '':
		print('Jogo adicionado para FACS')
        # var_dump.var_dump(result.stdout)
		variavel = result.stdout.split('\n')
		for o in variavel:
			Jogos.append(o)
	else:
		print('Nenhum resultado para FACS')
        # var_dump.var_dump(result.stdout)
# print(Jogos)


# # Start second program

# pdb.set_trace()
result2 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_PL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Wait for the program to finish
if result2.returncode != 0:
	print(result2.stderr)
else:
    # Print the stdout output if the subprocess ran successfully
	if result2.stdout != '':
		print('Jogo adicionado para PL')
		variavel = result2.stdout.split('\n')
		for o in variavel:
			Jogos.append(o)
        # var_dump.var_dump(variavel[0])
        # Jogos.append(result2.stdout.split['\n'])
	else:
		print('Nenhum resultado para PL')
        # var_dump.var_dump(result.stdout)
while "" in Jogos:
	Jogos.remove("")
# print(Jogos)

cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table_championship")
resultado1 = cursor.fetchone()[0]
temp = []
cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table")
resultado = cursor.fetchone()[0]
if resultado < 33:
	# Start third program
	result3 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SPFL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Wait for the program to finish
	if result3.returncode != 0:
		print(result3.stderr)
	else:
    	# Print the stdout output if the subprocess ran successfully
		if result3.stdout != '':
			print('Jogos SPFL encaminhados para o filtro')
			variavel = result3.stdout.split('\n')
			for o in variavel:
				temp.append(o)
			while "" in temp:
				temp.remove("")
			# print(temp)
			# print("\n")
			result3_1 = subprocess.run(['python', 'filtro_SPFL.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
			# # var_dump.var_dump(variavel[0])
			# print(result3_1.stdout)
			# variavel = result3_1.stdout.split('\n')
			# while "" in variavel:
			# 	variavel.remove("")
			# for o in variavel:
			# 	Jogos.append(o)
			# Jogos.append(result3_1.stdout)
		else:
			print('Nenhum resultado para SPFL')
			# var_dump.var_dump(result.stdout)
# print(Jogos)

elif resultado1 < 38:
	temp=[]
	# Start third program
	result3 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SPFL_championship], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Wait for the program to finish
	if result3.returncode != 0:
		print(result3.stderr)
	else:
    	# Print the stdout output if the subprocess ran successfully
		if result3.stdout != '':
			print('Jogos SPFL_championship encaminhados para o filtro')
			variavel = result3.stdout.split('\n')
			for o in variavel:
				temp.append(o)
			while "" in temp:
				temp.remove("")


		else:
			print('Nenhum resultado para SPFL_championship')
			# var_dump.var_dump(result.stdout)

	# Start third program (part2)
	result3_2 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SPFL_relegation], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Wait for the program to finish
	if result3_2.returncode != 0:
		print(result3_2.stderr)
	else:
    	# Print the stdout output if the subprocess ran successfully
		if result3_2.stdout != '':
			print('Jogos SPFL_relegation encaminhados para o filtro')
			variavel = result3_2.stdout.split('\n')
			for o in variavel:
				temp.append(o)
			while "" in temp:
				temp.remove("")
			# print(temp)
			# print("\n")


		else:
			print('Nenhum resultado para SPFL_relegation')
			# var_dump.var_dump(result.stdout)


	print(len(temp))
	if len(temp) > 0:
		result3_1 = subprocess.run(['python', 'filtro_SPFL_championship_relegation.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		variavel = result3_1.stdout.split('\n')
		while "" in variavel:
			variavel.remove("")
		for o in variavel:
			Jogos.append(o)

	temp=[]
	variavel=[]

	# print(Jogos)

# # Remove the else for now for testing propose
else:
	result3 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SPFL_PLAYOFFS], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Wait for the program to finish
	if result3.returncode != 0:
		print(result3.stderr)
	else:
    	# Print the stdout output if the subprocess ran successfully
		if result3.stdout != '':
			print('Jogos SPFL_playoffs adicionados')
			variavel = result3.stdout.split('\n')
			for o in variavel:
				if "SPFL - playoff" in o:
					u5 = o.replace("P1", "P2")
					Jogos.append(u5)
        	# var_dump.var_dump(variavel[0])
        	# Jogos.append(result2.stdout.split['\n'])
		else:
			print('Nenhum resultado para SPFL_playoffs')
			# var_dump.var_dump(result.stdout)
# print(Jogos)


cursor.execute("SELECT [Número de jogos] FROM eng_championship_table")
resultado = cursor.fetchone()[0]
if resultado < 46:

	# # Start fourth program
	result4 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_LCH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	temp=[]
	variavel=[]
	# Wait for the program to finish
	if result4.returncode != 0:
		print(result4.stderr)
	else:
		# Print the stdout output if the subprocess ran successfully
		if result4.stdout != '':
			print('Jogo LCH encaminhado ao filtro')
			variavel = result4.stdout.split('\n')
			for o in variavel:
					temp.append(o)
			while "" in temp:
				temp.remove("")
			# print(temp)
			result4_1 = subprocess.run(['python', 'filtro_LCH.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				# # var_dump.var_dump(variavel[0])
				# print(result3_1.stdout)
			variavel = result4_1.stdout.split('\n')
			while "" in variavel:
				variavel.remove("")
			print(variavel)
				# for o in variavel:
				# 	Jogos.append(o)
				# Jogos.append(result3_1.stdout)
		else:
			print('Nenhum resultado para LCH')

			# var_dump.var_dump(variavel[0])

			# Jogos.append(result2.stdout.split['\n'])
else:

	# # Start fourth program
	result4 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_LCH_PLAYOFFS], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	# # p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	temp=[]
	variavel=[]
	# Wait for the program to finish
	if result4.returncode != 0:
		print(result4.stderr)
	else:
		# Print the stdout output if the subprocess ran successfully
		if result4.stdout != '':
			print('Jogo LCH_PLAYOFF adicionado')
			variavel = result4.stdout.split('\n')
			for o in variavel:
					temp.append(o)
			while "" in temp:
				temp.remove("")
			# print(temp)
			if "j1=3" in temp:
				temp.remove("j1=3")
				temp[(len(temp)-1)] = temp[(len(temp)-1)].replace("P1", "P3")
			# print(temp)
			index1=0
			while "P1" in temp[index1]:
				temp[index1] = temp[index1].replace("P1", "P2")
				if index1 < (len(temp)-1):
					index1=index1 + 1

			# print(temp)
			for o in temp:
				Jogos.append(o)

		else:
			print('Nenhum resultado para LCH_PLAYOFF')

			# var_dump.var_dump(variavel[0])

			# Jogos.append(result2.stdout.split['\n'])

# while "" in Jogos:
# 	Jogos.remove("")
# print(Jogos)

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
			while "P1" in temp[index1]:
				temp[index1] = temp[index1].replace("P1", "P2")
				if index1 < (len(temp)-1):
					index1=index1 + 1
			for o in temp:
				Jogos.append(o)


			# for z3 in temp:
			# 	if "P1" in z3:
			# 		z3 = z3.replace("P1", "P2")

		elif "j1=2" in temp:
			temp.remove("j1=2")
			index1=0
			print('Jogo FAC final adicionado')
			while "P1" in temp[index1]:
				temp[index1] = temp[index1].replace("P1", "P3")
				if index1 < (len(temp)-1):
					index1=index1 + 1
			index1=0
			while "P2" in temp[index1]:
				temp[index1] = temp[index1].replace("P2", "P3")
				if index1 < (len(temp)-1):
					index1=index1 + 1
			for o in temp:
				Jogos.append(o)
		# print(temp)
		if len(temp) > 0 and zz == 2:
			result5_1 = subprocess.run(['python', 'filtro_FAC.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				# # var_dump.var_dump(variavel[0])
				# print(result3_1.stdout)
			variavel = result5_1.stdout.split('\n')
			while "" in variavel:
				variavel.remove("")
			# print(variavel)
			for o in variavel:
				Jogos.append(o)
		# 	# Jogos.append(result3_1.stdout)
		# else:
		# 	print('Nenhum resultado para FAC')
	else:
		print('Nenhum resultado para FAC')

		# var_dump.var_dump(variavel[0])

		# Jogos.append(result2.stdout.split['\n'])


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
			index1 = 0
			print('Jogo EFL semi-final adicionado')
			while "P1" in temp[index1]:
				temp[index1] = temp[index1].replace("P1", "P2")
				if index1 < (len(temp)-1):
					index1=index1 + 1
			for o in temp:
				Jogos.append(o)


			# for z3 in temp:
			# 	if "P1" in z3:
			# 		z3 = z3.replace("P1", "P2")

		elif "j1=2" in temp:
			temp.remove("j1=2")
			index1=0
			print('Jogo EFL final adicionado')
			while "P1" in temp[index1]:
				temp[index1] = temp[index1].replace("P1", "P3")
				if index1 < (len(temp)-1):
					index1=index1 + 1
			index1=0
			while "P2" in temp[index1]:
				temp[index1] = temp[index1].replace("P2", "P3")
				if index1 < (len(temp)-1):
					index1=index1 + 1
			for o in temp:
				Jogos.append(o)
		# print(temp)
		if len(temp) > 0 and zz == 2:
			result5_1 = subprocess.run(['python', 'filtro_FAC.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				# # var_dump.var_dump(variavel[0])
				# print(result3_1.stdout)
			variavel = result5_1.stdout.split('\n')
			while "" in variavel:
				variavel.remove("")
			# print(variavel)
			for o in variavel:
				Jogos.append(o)
		# 	# Jogos.append(result3_1.stdout)
		# else:
		# 	print('Nenhum resultado para FAC')
	else:
		print('Nenhum resultado para EFL')

		# var_dump.var_dump(variavel[0])

		# Jogos.append(result2.stdout.split['\n'])

print(Jogos)



# cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table_championship")
# resultado1 = cursor.fetchone()[0]

# for jogo in Jogos:
#     if jogo == '':
#         del jogo
#     else:
#         Jogos_final.append(jogo)
# # output = result.stdout.decode('utf-8')
# # print(output)
# # # out1, err1 = p1.communicate()

# print(Jogos_final)
