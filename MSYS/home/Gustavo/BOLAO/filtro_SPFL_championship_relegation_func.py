import sys
import sqlite3
import var_dump
import pdb
import yaml

def main_SPFL_champ_rele(x):
	conn = sqlite3.connect('championships.db')
	cursor = conn.cursor()

	with open('tabelas.yml', 'r') as f:
		data1 = yaml.load(f, Loader=yaml.FullLoader)

	temp = []
	temp1 = []
	temp1_2 = []
	temp0=[]
	# print(x)

	cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table_relegation")
	rows = cursor.fetchall()
	cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table_championship")
	rows2 = cursor.fetchall()

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
			#a partir da rodada 33
			if data1['RODADA_SPFL_CHAMPIONSHIP'] >= 33:
			# if rows2[0][4] > 32:
				for row in rows2:
					if j in row:
						temp1.append(row)
						z=1
					elif temp[index+1] in row:
						temp1.append(row)
						z=1
				for row in rows:
					if j in row:
						temp1.append(row)
						z=0
					elif temp[index+1] in row:
						temp1.append(row)
						z=0
				#To SPFL_CHAMPIONSHIP
				if z == 1:
					diff = abs(temp1[index][2]-temp1[index+1][2])
					positionto_1 = temp1[index][0] - rows2[0][0]
					positionto_1_2 =  temp1[index+1][0] - rows2[0][0]
					pointstofirst_1 = abs(temp1[index][2] - rows2[0][2])
					pointstofirst_2 = abs(temp1[index+1][2] - rows2[0][2])
					goalstofirst_1 = (rows2[0][3] - temp1[index][3])
					goalstofirst_2 = (rows2[0][3] - temp1[index+1][3])
					positionto_3 = temp1[index][0] - rows2[2][0]
					positionto_3_2 =  temp1[index+1][0] - rows2[2][0]
					pointstothird_1 = (rows2[2][2] - temp1[index][2])
					pointstothird_2 = (rows2[2][2] - temp1[index+1][2])
					goalstothird_1 = (rows2[2][3] - temp1[index][3])
					goalstothird_2 = (rows2[2][3] - temp1[index+1][3])
					pointstolast_1 = 1000
					pointstolast_2 = 1000
					goalstolast_1 = 1000
					goalstolast_2 = 1000
					pointstosecondlast_1 = 1000
					pointstosecondlast_2 = 1000
					goalstosecondlast_1 = 1000
					goalstosecondlast_2 = 1000
				# The 1000 entries here are a workaround to avoid confusing "relegation" with "championship" I had to modify the code, and this was the quickest way to fix the issue without overthinking it.

				#TO SPFL_RELEGATION
				elif z == 0:
					diff = 1000
					positionto_1 = 1000
					positionto_1_2 =  1000
					pointstofirst_1 = 1000
					pointstofirst_2 = 1000
					goalstofirst_1 = 1000
					goalstofirst_2 = 1000
					positionto_3 = 1000
					positionto_3_2 =  1000
					pointstothird_1 = 1000
					pointstothird_2 = 1000
					goalstothird_1 = 1000
					goalstothird_2 = 1000
					pointstolast_1 = (temp1[index][2] - rows[5][2])
					pointstolast_2 = (temp1[index+1][2] - rows[5][2])
					goalstolast_1 = (temp1[index][3] - rows[5][3])
					goalstolast_2 = (temp1[index+1][3] - rows[5][3])
					pointstosecondlast_1 = (temp1[index][2] - rows[4][2])
					pointstosecondlast_2 =(temp1[index+1][2] - rows[4][2])
					goalstosecondlast_1 = (temp1[index][3] - rows[4][3])
					goalstosecondlast_2 =(temp1[index+1][3] - rows[4][3])


				#rodada 33 a 36
				if data1['RODADA_SPFL_CHAMPIONSHIP'] <= 36:

				# critehrio 3 pontos/uel
					if 0 <= positionto_3 <= 2 and 0 <= positionto_3_2 <= 2 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
						temp0.append(12)
						x[index//2] = x[index//2].replace("P1", "P2")

				#critehrio primeiro colocado
					elif (positionto_1 == 0 and diff <=5) or (positionto_1_2 == 0 and diff <=5) or (pointstofirst_1 <= 3 and pointstofirst_2 <= 3):
						# print(diff)
						temp0.append(13)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")

				# critehrio do ultimo colocado
					elif rows[0][4] > 33 and pointstolast_1 <= 3 and pointstolast_2 <= 3:
						temp0.append(11)
						x[index//2] = x[index//2].replace("P1", "P2")

				# critehrio do penultimo colocado
					elif rows[0][4] > 34 and pointstosecondlast_1 <= 3 and pointstosecondlast_2 <= 3:
						temp0.append(10)
						x[index//2] = x[index//2].replace("P1", "P2")


					else:
						temp0.append(1)
				#rodada 37

				elif data1['RODADA_SPFL_CHAMPIONSHIP'] == 37:
				# elif rows2[0][4] == 36:

				# critehrio 3 pontos/uel
					if 0 <= positionto_3 <= 2 and 0 <= positionto_3_2 <= 2 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
						temp0.append(12)
						x[index//2] = x[index//2].replace("P1", "P2")

				# critehrio do ultimo colocado
					elif rows[0][4] > 34 and pointstolast_1 <= 3 and pointstolast_2 <= 3:
						temp0.append(11)
						x[index//2] = x[index//2].replace("P1", "P2")

				# critehrio do penultimo colocado
					elif rows[0][4] > 34 and pointstosecondlast_1 <= 3 and pointstosecondlast_2 <= 3:
						temp0.append(10)
						x[index//2] = x[index//2].replace("P1", "P2")


				#critehrio primeiro colocado (creio haver redundancia nesse critehrio, o ultimo jah garantiria, mas nao estou mais no ponto de mexer nisso)
					elif (positionto_1 == 0 and diff <=3) or (positionto_1_2 == 0 and diff <=3) or (pointstofirst_1 <= 3 and pointstofirst_2 <= 3):
						temp0.append(13)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")

					else:
						temp0.append(1)
				#rodada 38
				elif data1['RODADA_SPFL_CHAMPIONSHIP'] == 38:
				# elif rows2[0][4] == 37:

				# critehrio 3 pontos/uel
				# Aqui eu abri espaço para 10 times na disputa do terceiro lugar, não faz sentido limitarmos isso, creio
					if 0 <= positionto_3 <= 10 and 0 <= positionto_3_2 <= 10 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
						if (goalstothird_1 <= 7 or pointstothird_1 < 3) and (goalstothird_2 <= 7 or pointstothird_2 < 3):
							temp0.append(12)
							x[index//2] = x[index//2].replace("P1", "P2")
						else:
							temp0.append(1)

				# critehrio do ultimo colocado
					elif ((pointstolast_1 == 3 and goalstolast_1 <= 7) or pointstolast_1 <=2) and ((pointstolast_2 == 3 and goalstolast_2 <= 7) or pointstolast_2 <= 2):
						temp0.append(11)
						x[index//2] = x[index//2].replace("P1", "P2")


				# critehrio do penultimo colocado
					elif ((pointstosecondlast_1 == 3 and goalstosecondlast_1 <= 7) or pointstosecondlast_1 <=2) and ((pointstosecondlast_2 == 3 and goalstosecondlast_2 <= 7) or pointstosecondlast_2 <= 2):
						temp0.append(11)
						x[index//2] = x[index//2].replace("P1", "P2")



				#critehrio primeiro colocado

					elif ((pointstofirst_1 == 3 and goalstofirst_1 <= 7) or pointstofirst_1 <= 2) and ((pointstofirst_2 == 3 and goalstofirst_2 <= 7) or pointstofirst_2 <= 2):
						temp0.append(13)
						x[index//2] = x[index//2].replace("P1", "P3")
						x[index//2] = x[index//2].replace("P2", "P3")
					else:
						temp0.append(1)

		#critehrio do derbie
			if temp0[index//2] < 9 and "P2" in x[index//2]:
				temp0[index//2] = 9
		# jogo do primeiro colocado
			elif positionto_1 == 0 or positionto_1_2 == 0:
				temp0[index//2] = 8
		# jogo do segundo colocado
			elif positionto_1 == 1 or positionto_1_2 == 1:
				temp0[index//2] = 7
		# jogo do terceiro colocado
			elif positionto_1 == 2 or positionto_1_2 == 2:
				temp0[index//2] = 6
		# jogo do quarto colocado
			elif positionto_1 == 3 or positionto_1_2 == 3:
				temp0[index//2] = 5
		# jogo do quinto colocado
			elif positionto_1 == 4 or positionto_1_2 == 4:
				temp0[index//2] = 4
		# jogo do sexto colocado
			elif positionto_1 == 5 or positionto_1_2 == 5:
				temp0[index//2] = 3
		# jogo do setimo colocado
			elif positionto_1 == 6 or positionto_1_2 == 6:
				temp0[index//2] = 2


	sorted_values = sorted(zip(temp0, x), reverse=True)
	temp0_sorted, x_sorted = map(list, zip(*sorted_values))


	returnVariable = []

	for index, z in enumerate(x_sorted):
		returnVariable.append(z)
		if index==2:
			break
	conn.close()
	return returnVariable