import sys
import sqlite3
# import var_dump
# import pdb
import yaml

def main_filtro_spfl(x):
	conn = sqlite3.connect('championships.db')
	cursor = conn.cursor()

	with open('TIMES_PRIMEIRA_RODADA.yml', 'r') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)


	with open('tabelas.yml', 'r') as f:
		data1 = yaml.load(f, Loader=yaml.FullLoader)


	temp = []
	temp1 = []
	temp0=[]


	cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table")
	rows = cursor.fetchall()


	for y in x:
		parts = y.split(" x ")
		part1 = parts[0]
		part2 = parts[1].split(" - ")
		part3 = part2[0]
		temp.append(part1)
		temp.append(part3)


	for index, j in enumerate(temp):
		# pdb.set_trace()
		if index % 2 == 0:
			# rodada inicial
			if data1['RODADA_SPFL'] == 1:
			# if rows[0][4] == 0:
				if data['FIRST_ROUND_SPFL']['TIME1'] in x[index//2]:
					# print('jorge')
					temp0.append(9)
				elif data['FIRST_ROUND_SPFL']['TIME2'] in x[index//2]:
					temp0.append(8)
				elif data['FIRST_ROUND_SPFL']['TIME3'] in x[index//2]:
					temp0.append(7)
				elif data['FIRST_ROUND_SPFL']['TIME4'] in x[index//2]:
					temp0.append(6)
				elif data['FIRST_ROUND_SPFL']['TIME5'] in x[index//2]:
					temp0.append(5)
				else:
					temp0.append(1)
			# rodada 2 a 33
			elif data1['RODADA_SPFL'] >= 2:
			# if rows[0][4] >= 1:
				for row in rows:
					if j in row:
						temp1.append(row)
					elif temp[index+1] in row:
						temp1.append(row)
				# print(temp1)
				diff = abs(temp1[index][2]-temp1[index+1][2])
				positionto_1 = temp1[index][0] - rows[0][0]
				positionto_1_2 =  temp1[index+1][0] - rows[0][0]
				pointstofirst_1 = abs(temp1[index][2] - rows[0][2])
				# print(pointstofirst_1)
				pointstofirst_2 = abs(temp1[index+1][2] - rows[0][2])
				# print(pointstofirst_2)
				positionto_3 = temp1[index][0] - rows[2][0]
				positionto_3_2 =  temp1[index+1][0] - rows[2][0]
				pointstothird_1 = (rows[2][2] - temp1[index][2])
				pointstothird_2 = (rows[2][2] - temp1[index+1][2])
				# rodada escolhida a 11
				Rodadas_iniciais = 5
				if data1['RODADA_SPFL'] <= Rodadas_iniciais:
				# if rows[0][4] < 4:
					temp0.append(1)

				elif  data1['RODADA_SPFL'] <= 11:
				# if 4 <= rows[0][4] <11:
				# critehrio do primeiro colocado
					if positionto_1 == 0 and diff <=3:
						temp0.append(12)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")
					elif positionto_1_2 == 0 and diff <=3:
						temp0.append(12)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")
					elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
						temp0.append(12)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")

					else:
						temp0.append(1)

				# rodada 12 a 33
				elif  data1['RODADA_SPFL'] <= 33:
				# elif rows[0][4] > 10 and rows[0][4] <33:

				# critehrio 3 pontos/uel. A conferencia de posicoes eu coloquei um valor alto, mas nem fazia sentido conferir no sentido superior, somente deve indicar que o time tah depois do terceiro ou eh o terceiro
					if 0 <= positionto_3 <= 10 and 0 <= positionto_3_2 <= 10 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
						if  data1['RODADA_SPFL'] >= 23:
						# if rows[0][4] >= 22:
							temp0.append(11)
							x[index//2] = x[index//2].replace("P1", "P2")
						else:
							temp0.append(1)
				#critehrio primeiro colocado
					elif (positionto_1 == 0 and diff <=5) or (positionto_1_2 == 0 and diff <=5) or (pointstofirst_1 <= 3 and pointstofirst_2 <= 3):
						temp0.append(12)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")

					else:
						temp0.append(1)

			# jogo do primeiro colocado
				if (positionto_1 == 0 or positionto_1_2 == 0):
					temp0[index//2] = 9
			# jogo do segundo colocado
				elif positionto_1 == 1 or positionto_1_2 == 1:
					temp0[index//2] = 8
			# jogo do terceiro colocado
				elif positionto_1 == 2 or positionto_1_2 == 2:
					temp0[index//2] = 7
			# jogo do quarto colocado
				elif positionto_1 == 3 or positionto_1_2 == 3:
					temp0[index//2] = 6
			# jogo do quinto colocado
				elif positionto_1 == 4 or positionto_1_2 == 4:
					temp0[index//2] = 5
			# jogo do sexto colocado
				elif positionto_1 == 5 or positionto_1_2 == 5:
					temp0[index//2] = 4
			# jogo do setimo colocado
				elif positionto_1 == 6 or positionto_1_2 == 6:
					temp0[index//2] = 3


		#critehrio do derbie
			if temp0[index//2] < 10 and  "P2" in x[index//2]:
				temp0[index//2] = 10



	tempoo = []
	index2=0


	sorted_values = sorted(zip(temp0, x), reverse=True)
	temp0_sorted, x_sorted = map(list, zip(*sorted_values))
	filtrado = []

	returnVariable = []

	for index, z in enumerate(x_sorted):
		returnVariable.append(z)
		if index==2:
			break
	conn.close()
	return returnVariable