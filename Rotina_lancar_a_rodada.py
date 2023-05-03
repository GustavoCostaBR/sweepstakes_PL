import var_dump
import subprocess
import yaml
from datetime import datetime, timedelta
import pytz
import sqlite3

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

print(Tabelas)

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
		print('Jogo adicionado para PL')
		variavel = result.stdout.split('\n')
		for o in variavel:
			Jogos.append(o)
	else:
		print('Nenhum resultado para FACS')
        # var_dump.var_dump(result.stdout)

# Start second program
result2 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_PL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
# p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


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

cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table_championship")
resultado1 = cursor.fetchone()[0]

cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table")
resultado = cursor.fetchone()[0]
if resultado < 33:
	# Start third program
	result3 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SPFL], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Wait for the program to finish
	if result2.returncode != 0:
		print(result2.stderr)
	else:
    	# Print the stdout output if the subprocess ran successfully
		if result2.stdout != '':
			print('Jogos SPFL encaminhados para o filtro')
			variavel = result2.stdout.split('\n')
			for o in variavel:
				temp.append(o)
			# result39 = subprocess.run(['python', 'filtro_SPFL.py', *temp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
			# # var_dump.var_dump(variavel[0])
        	# Jogos.append(result2.stdout.split['\n'])
		else:
			print('Nenhum resultado para SPFL')
			# var_dump.var_dump(result.stdout)
elif resultado1 < 38:
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
				Jogos.append(o)
        	# var_dump.var_dump(variavel[0])
        	# Jogos.append(result2.stdout.split['\n'])
		else:
			print('Nenhum resultado para SPFL_championship')
			# var_dump.var_dump(result.stdout)
	# Start third program (part2)
	result35 = subprocess.run(['python', 'buscador_jogosv3.py', *dt, *dt2, url_SPFL_relegation], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	# Wait for the program to finish
	if result35.returncode != 0:
		print(result35.stderr)
	else:
    	# Print the stdout output if the subprocess ran successfully
		if result35.stdout != '':
			print('Jogos SPFL_relegation encaminhados para o filtro')
			variavel = result35.stdout.split('\n')
			for o in variavel:
				Jogos.append(o)
        	# var_dump.var_dump(variavel[0])
        	# Jogos.append(result2.stdout.split['\n'])
		else:
			print('Nenhum resultado para SPFL_relegation')
			# var_dump.var_dump(result.stdout)

# Remove de else for now for testing propose
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



for jogo in Jogos:
    if jogo == '':
        del jogo
    else:
        Jogos_final.append(jogo)
# output = result.stdout.decode('utf-8')
# print(output)
# # out1, err1 = p1.communicate()

print(Jogos_final)


# print('1')
# # Start second program
# p2 = subprocess.Popen(['python', 'gerador_de_string_cod_font.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# out2, err2 = p2.communicate()
# print('2')
# # Print output and errors
# print(out1.decode())
# print(out2.decode())
# print(err1.decode())
# print(err2.decode())

# # Start first program
# p3 = subprocess.Popen(['python', 'spider_links.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# # Wait for both programs to finish
# out3, err3 = p3.communicate()
# print('3')
# p4 = subprocess.Popen(['python', 'spider_content.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# out4, err4 = p4.communicate()
# print('4')
# p5 = subprocess.Popen(['python', 'code_deleter.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out5, err5 = p5.communicate()
# print('5')
# p6 = subprocess.Popen(['python', 'code_infos.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out6, err6 = p6.communicate()
# print('6')

# output1 = subprocess.check_output(['python', 'code_plots.py'])

# output1_values = output1.decode().strip().split(',')
# avg = float(output1_values[0])
# devpad = float(output1_values[1])
# meddifsal = float(output1_values[2])
# devpaddisp = float(output1_values[3])
# p7 = subprocess.Popen(['python', 'code_plots.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# subprocess.check_call(['python', 'plotagem.py', str(avg), str(devpad), str(meddifsal), str(devpaddisp)])

# print('7')



# # p8 = subprocess.Popen(['python', 'plotagem.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # out8, err8 = p8.communicate()
# # print('8')