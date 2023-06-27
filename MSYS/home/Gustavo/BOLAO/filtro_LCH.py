import sys
import sqlite3
# import var_dump
import pdb
import yaml

conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

with open('TIMES_PRIMEIRA_RODADA.yml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

with open('Configuracoes.yml', 'r') as f:
	data0 = yaml.load(f, Loader=yaml.FullLoader)

# x = sys.argv[1:]

x = ['Time5 x Time6 - P1 (PL) - 20/05 - 08:30','Time7 x Time8 - P1 (PL) - 20/05 - 08:30','Time9 x Time10 - P1 (PL) - 20/05 - 08:30','Time11 x Time12 - P1 (PL) - 20/05 - 08:30','Time13 x Time14 - P1 (PL) - 20/05 - 08:30', 'Time3 x Time4 - P1 (PL) - 20/05 - 08:30', 'Time15 x Time16 - P1 (PL) - 20/05 - 08:30','Time17 x Time18 - P1 (PL) - 20/05 - 08:30','Time1 x Time2 - P1 (PL) - 20/05 - 08:30','Time19 x Time20 - P1 (PL) - 20/05 - 08:30','Time21 x Time22 - P1 (PL) - 20/05 - 08:30','Time23 x Time24 - P1 (PL) - 20/05 - 08:30']

# x = ['Rotherham United x Blackburn Rovers - P1 (LCH) - 14/01 - 08:30', 'Sunderland x Swansea City - P1 (LCH) - 14/01 - 11:00', 'Bristol City x Birmingham City - P1 (LCH) - 14/01 - 11:00', 'Cardiff City x Wigan Athletic - P1 (LCH) - 14/01 - 11:00', 'Burnley x Coventry City - P1 (LCH) - 14/01 - 11:00', 'Middlesbrough x Millwall - P1 (LCH) - 14/01 - 11:00', 'Reading x Queens Park Rangers - P1 (LCH) - 14/01 - 11:00', 'Watford x Blackpool - P1 (LCH) - 14/01 - 11:00', 'Hull City x Huddersfield Town - P1 (LCH) - 14/01 - 11:00', 'Luton Town x West Bromwich Albion - P1 (LCH) - 14/01 - 11:00', 'Preston North End x Norwich City - P1 (LCH) - 14/01 - 11:00', 'Sheffield United x Stoke City - P1 (LCH) - 14/01 - 11:00']


ones_list = [1] * 12
temp = []
temp1 = []
temp1_2 = []
temp0=[]
temp_classi = []
teams_delete = []
# marcadorcri = 0
# temp_classi_2 = []


def p(choice ,index, positionr):
	global rows
	global temp1
	if choice == 0:
		points_1 = (temp1[index][2] - rows[positionr][2])
		return points_1
	elif choice == 1:
		posi_1 = (temp1[index][0] - rows[positionr][0])
		return posi_1
	elif choice == 2:
		goals_1 = (temp1[index][3] - rows[positionr][3])
		return goals_1
	elif choice == 3:
		points_1 = (temp1[index][2] - rows[positionr][2])
		goals_1 = (temp1[index][3] - rows[positionr][3])
		return points_1, goals_1


cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM eng_championship_table")
rows = cursor.fetchall()



for y in x:
	parts = y.split(" x ")
	part1 = parts[0]
	part2 = parts[1].split(" - ")
	part3 = part2[0]
	temp.append(part1)
	temp.append(part3)


list_to_delete = []
lista_times_delete = []
contador = 0


for index, j in enumerate(temp):
	if index % 2 == 0:
		if rows[0][4] >= 1:
			for row in rows:
				if j in row:
					temp1.append(row)
				elif temp[index+1] in row:
					temp1.append(row)


# Defines the search of the first positions to exclude mathematics defined positions
index2=0

# Defines the search of the last positions to exclude mathematics defined positions
index3 = 0




while contador < 20:
	for index, team in enumerate(temp):
	# Excluir times matematicamente definidos em alguma posicao
		# if index == 23:
			# pdb.set_trace()
		if rows[0][4] < 45:
			# Playoff verification
			if 5 >= index2 >= 2 and ((p(1, index, index2) == 0 and p(0, index, 6) > (((46 - (rows[0][4])) * 3) ))):
				index2 = index2 + 1
				if index not in list_to_delete:
					list_to_delete.append(index)
					lista_times_delete.append(team)
					if index % 2 == 0:
						if index+1 not in list_to_delete:
							list_to_delete.append(index+1)
							lista_times_delete.append(temp[index+1])
					else:
						if index-1 not in list_to_delete:
							list_to_delete.append(index-1)
							lista_times_delete.append(temp[index-1])

			# First positions verification, should be after because of the index2
			elif index2 < 2 and ((p(1, index, index2) == 0 and p(0, index, index2+1) > (((46 - (rows[0][4])) * 3)))):
				index2 = index2 + 1
				if index not in list_to_delete:
					list_to_delete.append(index)
					lista_times_delete.append(team)
					if index % 2 == 0:
						if index+1 not in list_to_delete:
							list_to_delete.append(index+1)
							lista_times_delete.append(temp[index+1])
					else:
						if index-1 not in list_to_delete:
							list_to_delete.append(index-1)
							lista_times_delete.append(temp[index-1])

			# Last positions verification
			elif 2 >= index3  and ((p(1, index, 23-index3) == 0 and abs(p(0, index, 20)) > (((46 - (rows[0][4])) * 3)))):
				index3 = index3 + 1
				if index not in list_to_delete:
					list_to_delete.append(index)
					lista_times_delete.append(team)
					if index % 2 == 0:
						if index+1 not in list_to_delete:
							list_to_delete.append(index+1)
							lista_times_delete.append(temp[index+1])
					else:
						if index-1 not in list_to_delete:
							list_to_delete.append(index-1)
							lista_times_delete.append(temp[index-1])

		elif rows[0][4] == 45:
			# Playoff verification
			if 5 >= index2 >= 2 and ((p(1, index, index2) == 0 and (((p(0, index, 6) > (((46 - (rows[0][4])) * 3) ))) or ((p(0, index, 6) == (((46 - (rows[0][4])) * 3))) ) and p(2, index, 6) > 7 ) )):
				if index not in list_to_delete:
					list_to_delete.append(index)
					lista_times_delete.append(team)
					if index % 2 == 0:
						if index+1 not in list_to_delete:
							list_to_delete.append(index+1)
							lista_times_delete.append(temp[index+1])
					else:
						if index-1 not in list_to_delete:
							list_to_delete.append(index-1)
							lista_times_delete.append(temp[index-1])



			# First positions verification, should be after because of the index2
			elif index2 < 2 and ((p(1, index, index2) == 0 and (((p(0, index, index2+1) > (((46 - (rows[0][4])) * 3) ))) or ((p(0, index, index2+1) == (((46 - (rows[0][4])) * 3))) ) and p(2, index, index2+1) > 7 ) )):
				index2 = index2 + 1
				if index not in list_to_delete:
					list_to_delete.append(index)
					lista_times_delete.append(team)
					if index % 2 == 0:
						if index+1 not in list_to_delete:
							list_to_delete.append(index+1)
							lista_times_delete.append(temp[index+1])
					else:
						if index-1 not in list_to_delete:
							list_to_delete.append(index-1)
							lista_times_delete.append(temp[index-1])



			# Last positions verification
			elif 2 >= index3  and (((p(1, index, 23-index3) == 0 and abs(p(0, index, 20)) > (((46 - (rows[0][4])) * 3))) or (((abs((p(0, index, 20)))) == (((46 - (rows[0][4])) * 3))) ) and (p(2, index, 20) < (-7))  )):
				index3 = index3 + 1
				if index not in list_to_delete:
					list_to_delete.append(index)
					lista_times_delete.append(team)
					if index % 2 == 0:
						if index+1 not in list_to_delete:
							list_to_delete.append(index+1)
							lista_times_delete.append(temp[index+1])
					else:
						if index-1 not in list_to_delete:
							list_to_delete.append(index-1)
							lista_times_delete.append(temp[index-1])

	contador = contador + 1









# while contador < 20:
# 	for index, team in enumerate(temp):
# 	# Excluir times matematicamente definidos em alguma posicao
# 		if index % 2 == 0:
# 			if rows[0][4] < 45:
# 				# Playoff verification
# 				if 5 >= index2 >= 2 and ((p(1, index, index2) == 0 and p(0, index, 6) > (((46 - (rows[0][4])) * 3) )) or (p(1, index+1, index2) == 0 and p(0, index+1, 6) > (((46 - (rows[0][4])) * 3)))):
# 					index2 = index2 + 1
# 					if index not in list_to_delete and (index+1) not in list_to_delete:
# 						list_to_delete.extend([index, index+1])



# 				# First positions verification, should be after because of the index2
# 				elif index2 < 2 and ((p(1, index, index2) == 0 and p(0, index, index2+1) > (((46 - (rows[0][4])) * 3))) or (p(1, index+1, index2) == 0 and p(0, index+1, index2+1) > (((46 - (rows[0][4])) * 3)))):
# 					index2 = index2 + 1
# 					if index not in list_to_delete and (index+1) not in list_to_delete:
# 						list_to_delete.extend([index, index+1])

# 				# Last positions verification
# 				elif 2 >= index3  and ((p(1, index, 23-index3) == 0 and abs(p(0, index, 20)) > (((46 - (rows[0][4])) * 3))) or (p(1, index+1, 23-index3) == 0 and abs(p(0, index+1, 20)) > (((46 - (rows[0][4])) * 3)))):
# 					index3 = index3 + 1
# 					if index not in list_to_delete and (index+1) not in list_to_delete:
# 						list_to_delete.extend([index, index+1])


# 			if rows[0][4] == 45:
# 				# Playoff verification
# 				if 5 >= index2 >= 2 and ((p(1, index, index2) == 0 and (((p(0, index, 6) > (((46 - (rows[0][4])) * 3) ))) or ((p(0, index, 6) == (((46 - (rows[0][4])) * 3))) ) and p(2, index, 6) > 7 ) ) or (p(1, index+1, index2) == 0 and (((p(0, index+1, 6) > (((46 - (rows[0][4])) * 3) ))) or ((p(0, index+1, 6) == (((46 - (rows[0][4])) * 3))) ) and p(2, index+1, 6) > 7 ))):
# 					if index not in list_to_delete and (index+1) not in list_to_delete:
# 						list_to_delete.extend([index, index+1])



# 				# First positions verification, should be after because of the index2
# 				elif index2 < 2 and ((p(1, index, index2) == 0 and (((p(0, index, index2+1) > (((46 - (rows[0][4])) * 3) ))) or ((p(0, index, index2+1) == (((46 - (rows[0][4])) * 3))) ) and p(2, index, index2+1) > 7 ) ) or (p(1, index+1, index2) == 0 and  (((p(0, index+1, index2+1) > (((46 - (rows[0][4])) * 3) ))) or ((p(0, index+1, index2+1) == (((46 - (rows[0][4])) * 3))) ) and p(2, index+1, index2+1) > 7 ))):
# 					index2 = index2 + 1
# 					if index not in list_to_delete and (index+1) not in list_to_delete:
# 						list_to_delete.extend([index, index+1])

# 	contador = contador + 1

contador = 0
for index in sorted(list_to_delete, reverse=True):
	if contador % 2 == 0:
		del x[index//2]
	del temp[index]
	contador = contador + 1

for jogo in x:
	print(jogo)

temp1 = []

# for index, j in enumerate(temp):
# 	if index % 2 == 0:
# 		if rows[0][4] == 0:
# 			if data['FIRST_ROUND_LCH']['TIME1'] in x[index//2]:
# 				temp0.append(9)
# 			elif data['FIRST_ROUND_LCH']['TIME2'] in x[index//2]:
# 				temp0.append(8)
# 			elif data['FIRST_ROUND_LCH']['TIME3'] in x[index//2]:
# 				temp0.append(7)
# 			elif data['FIRST_ROUND_LCH']['TIME4'] in x[index//2]:
# 				temp0.append(6)
# 			elif data['FIRST_ROUND_LCH']['TIME5'] in x[index//2]:
# 				temp0.append(5)
# 			elif data['FIRST_ROUND_LCH']['TIME6'] in x[index//2]:
# 				temp0.append(4)
# 			elif data['FIRST_ROUND_LCH']['TIME7'] in x[index//2]:
# 				temp0.append(3)
# 			elif data['FIRST_ROUND_LCH']['TIME8'] in x[index//2]:
# 				temp0.append(2)
# 			else:
# 				temp0.append(1)
# 		# rodada 2 a 33
# 		if rows[0][4] >= 1:

# 			for row in rows:
# 				if j in row:
# 					temp1.append(row)
# 				elif temp[index+1] in row:
# 					temp1.append(row)
# 			# print(temp1)
# 			diff = abs(temp1[index][2]-temp1[index+1][2])
# 			positionto_1 = temp1[index][0] - rows[0][0]
# 			positionto_1_2 =  temp1[index+1][0] - rows[0][0]
# 			pointstofirst_1 = abs(temp1[index][2] - rows[0][2])
# 			pointstosecond_1 = (temp1[index][2] - rows[1][2])
# 			pointstosecond_2 = (temp1[index+1][2] - rows[1][2])
# 			points1 = temp1[index][2]
# 			points2 = temp1[index+1][2]
# 			# print(pointstofirst_1)
# 			pointstofirst_2 = abs(temp1[index+1][2] - rows[0][2])
# 			# print(pointstofirst_2)
# 			positionto_3 = temp1[index][0] - rows[2][0]
# 			positionto_3_2 =  temp1[index+1][0] - rows[2][0]
# 			pointstothird_1 = (rows[2][2] - temp1[index][2])
# 			pointstothird_2 = (rows[2][2] - temp1[index+1][2])
# 			pointstosixth_1 = (rows[5][2] - temp1[index][2])
# 			pointstosixth_2 = (rows[5][2] - temp1[index+1][2])

# 			pointstoseventh_1 = (rows[6][2] - temp1[index][2])
# 			pointstoseventh_2 = (rows[6][2] - temp1[index+1][2])



# 		# rodada 2 a 12
# 			if rows[0][4] <=11:
# 				temp0.append(int(points1+points2))
# 				temp_classi.append(min(int(positionto_1),int(positionto_1_2)))


# 			# rodada 13 ateh critério de troca
# 			elif rows[0][4] < data0['RODADA_TROCA_CRITERIO_LCH']:


# 		#critehrio do primeiro colocado
# 				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
# 					temp0.append(255)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)

# 		#critehrio do segundo colocado
# 				elif 0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3):
# 					temp0.append(254)
# 					temp_classi.append(points1+points2)
# 					x[index//2] = x[index//2].replace("P1", "P2")


# 		# Jogos entre quaisquer dois times nas 6 primeiras posições
# 				elif p(1, index, 0) <= 5 and p(1, index+1, 0) <= 5:
# 					temp0.append(252)
# 					temp_classi.append(points1+points2)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					# marcadorcri = 1

# 		# critehrio da soma de pontos

# 				else:
# 					# pdb.set_trace()
# 					temp0.append(points1+points2)
# 					temp_classi.append(149-int(min(p(1, index, 0), p(1, index+1, 0))))
# 					# marcadorcri = 1

# 		# rodada escolhida a 44
# 			elif rows[0][4] < 44:


# 		#critehrio do primeiro colocado
# 				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
# 					temp0.append(255)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)
# 				elif (pointstofirst_1 <=5 and positionto_1_2 == 0) or (pointstofirst_2 <=5 and positionto_1 == 0):
# 					temp0.append(255)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)

# 		#critehrio do segundo colocado
# 				elif 0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3):
# 					temp0.append(254)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)
# 		# critehrio do playoff
# 			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
# 				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and 6 > (p(1, index, 0) > 1 and 6 > p(1, index+1,0) > 1):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)
# 			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
# 				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) and (1 < p(1, index+1, 0) >= 6) or (1 < p(1, index+1, 0)) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and (1 < p(1, index, 0) >= 6):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
# 				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 		# critehrio da zona de rebaixamento
# 			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
# 				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) >= 1 and p(1, index+1, 20) >= 1):
# 					temp0.append(252)
# 					if rows[0][4] >= 43:
# 						x[index//2] = x[index//2].replace("P1", "P2")
# 						temp_classi.append(points1+points2)

# 			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
# 				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) and (p(1, index+1, 20) <= 0) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) and (p(1, index, 20) <= 0):
# 					temp0.append(252)
# 					if rows[0][4] >= 43:
# 						x[index//2] = x[index//2].replace("P1", "P2")
# 						temp_classi.append(points1+points2)

# 			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
# 				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3):
# 					temp0.append(252)
# 					if rows[0][4] >= 43:
# 						x[index//2] = x[index//2].replace("P1", "P2")
# 						temp_classi.append(points1+points2)
# 		# critehrio de colocacao

# 				else:
# 					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))
# 					temp_classi.append(points1+points2)


# 		# rodada 45
# 			elif rows[0][4] < 45:


# 		#critehrio do primeiro colocado
# 				if (pointstofirst_1 <= 3 and pointstofirst_2 <= 3):
# 					temp0.append(255)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)

# 		#critehrio do segundo colocado
# 				elif 0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3):
# 					temp0.append(254)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)
# 		# critehrio do playoff
# 			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
# 				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and 6 > (p(1, index, 0) > 1 and 6 > p(1, index+1,0) > 1):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)
# 			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
# 				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) and (1 < p(1, index+1, 0) >= 6) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) and (1 < p(1, index, 0) >= 6):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
# 				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 		# critehrio da zona de rebaixamento
# 			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
# 				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) >= 1 and p(1, index+1, 20) >= 1):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
# 				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) and (p(1, index+1, 20) <= 0) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) and (p(1, index, 20) <= 0):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
# 				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)
# 		# critehrio de colocacao

# 				else:
# 					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))
# 					temp_classi.append(points1+points2)


# 		# rodada 46
# 			elif rows[0][4] == 45:


# 		#critehrio do primeiro colocado
# 				if (pointstofirst_1 <= 3 and pointstofirst_2 <= 3) and (p(2, index, 0) >= (-6) and p(2, index+1, 0) >=(-6)):
# 					temp0.append(255)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)
# 				elif (pointstofirst_1 <= 2 and pointstofirst_2 <= 2):
# 					temp0.append(255)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)

# 		#critehrio do segundo colocado
# 				elif (0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3)) and (p(2, index, 1) >= (-6) and p(2, index+1, 1) >= (-6)):
# 					temp0.append(254)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)

# 				elif (0 >= pointstosecond_1 >= (-2) and 0 >= pointstosecond_2 >= (-2)):
# 					temp0.append(254)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					x[index//2] = x[index//2].replace("P2", "P3")
# 					temp_classi.append(points1+points2)

# 		# critehrio do playoff
# 			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
# 				elif (0 <= p(0, index, 6) <= 3 and 0 <= p(0, index+1, 6) <= 3) and (p(2, index,6) >= 6 and p(2, index+1,6) >= 6 ) and 6 > (p(1, index, 0) > 1 and 6 > p(1, index+1,0) > 1):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					temp_classi.append(points1+points2)

# 				elif (0 <= p(0, index, 6) <=2 and 0 <= p(0, index+1, 6) <= 2) and 6 > (p(1, index, 0) > 1 and 6 > p(1, index+1,0) > 1):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					temp_classi.append(points1+points2)

# 			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
# 				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and (p(2, index, 0)-p(2, index+1, 0)) <= 6) and (1 < p(1, index+1, 0) >= 6) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and (p(2, index+1, 0)-p(2, index, 0)) <= 6) and (1 < p(1, index, 0) >= 6):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					temp_classi.append(points1+points2)

# 				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2) and (1 < p(1, index+1, 0) >= 6) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2) and (1 < p(1, index, 0) >= 6):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					temp_classi.append(points1+points2)


# 			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
# 				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)) and (p(2, index, 5) >= (-6) and p(2, index+1, 5) >= (-6)):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					temp_classi.append(points1+points2)

# 				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-2) and p(0, index+1, 5) >= (-2)):
# 					temp0.append(253)
# 					x[index//2] = x[index//2].replace("P1", "P3")
# 					temp_classi.append(points1+points2)

# 		# critehrio da zona de rebaixamento
# 			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
# 				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) >= 1 and p(1, index+1, 20) >= 1) and (p(2, index, 20) >= (-6) and p(2, index+1, 20) >= (-6)):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 				elif (0 >= p(0, index, 20) >= (-2) and 0 >= p(0, index+1, 20) >= (-2)) and (p(1, index, 20) >= 1 and p(1, index+1, 20) >= 1):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
# 				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and (p(2, index+1, 0)-p(2, index, 0)) <= 6) and (p(1, index+1, 20) <= 0) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and (p(2, index, 0)-p(2, index+1, 0)) <= 6) and (p(1, index, 20) <= 0):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2) and (p(1, index+1, 20) <= 0) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2) and (p(1, index, 20) <= 0):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
# 				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3) and (p(2, index, 21) <= 6 and p(2, index+1, 21) <= 6):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)

# 				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 2 and p(0, index+1, 21) <= 2):
# 					temp0.append(252)
# 					x[index//2] = x[index//2].replace("P1", "P2")
# 					temp_classi.append(points1+points2)
# 		# critehrio de colocacao

# 				else:
# 					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))
# 					temp_classi.append(points1+points2)



# 		#critehrio do derbie
# 		if rows[0][4] >= data0['RODADA_TROCA_CRITERIO_LCH'] or rows[0][4] <= 11:
# 			if temp0[index//2] < 250 and  "P2" in x[index//2]:
# 				temp0[index//2] = 250
# 				temp_classi.append(points1+points2)

# 		else:
# 			if temp0[index//2] < 253 and  "P2" in x[index//2]:
# 				temp0[index//2] = 253
# 				temp_classi.append(points1+points2)
# # print(temp)
# # print(temp0)
# tempoo = []
# index2=0
# # for index, y in enumerate(temp):
# # 	if index%2 == 0:
# # 		for z in x:
# # 			if y in z:
# # 				tempoo.append(z)
# # temp0_sorted, x_sorted = zip(*sorted(zip(temp0, x), reverse=True))

# # temp0_sorted, x_sorted = zip(*sorted(zip(temp0, x), reverse=True))
# a = "z"
# b = "z"
# c = "z"
# d = "z"
# index2 = 0
# if 1 <= rows[0][4]:
# 	sorted_values = sorted(zip(temp0, x, temp_classi), reverse=True)
# 	temp0_sorted, x_sorted, temp_classi_sorted = map(list, zip(*sorted_values))
# else:
# 	sorted_values = sorted(zip(temp0, x), reverse=True)
# 	temp0_sorted, x_sorted = map(list, zip(*sorted_values))

# filtrado = []
# # print(x_sorted[0])
# # for u in x_sorted:
# # 	filtrado.append(u)
# # print(temp0_sorted)
# # print(x_sorted)
# # print(len(temp0_sorted))
# if rows[0][4] <=11:
# 	if temp0_sorted[2] == temp0_sorted[3]:
# 		while index2 < 5:
# 			if len(temp0_sorted) % 2 == 0:
# 				zx = len(temp0_sorted)
# 			else:
# 				zx = len(temp0_sorted) - 1


# 			for indx in range(zx):
# 				if indx%2 == 0:
# 					if temp0_sorted[indx] == temp0_sorted[indx+1]:
# 						if (temp_classi_sorted[indx]) > (temp_classi_sorted[(indx+1)]):
# 							a, b, c = temp0_sorted[indx], x_sorted[indx], temp_classi_sorted[indx]
# 							temp0_sorted[indx], x_sorted[indx], temp_classi_sorted[indx] = temp0_sorted[indx+1], x_sorted[indx+1], temp_classi_sorted[indx+1]
# 							temp0_sorted[indx+1], x_sorted[indx+1], temp_classi_sorted[indx+1] = a, b, c

# 				# if indx >= len(temp0_sorted) - 3:
# 				# 	break

# 			for indx in range(zx):
# 				if indx%2 == 1:
# 					if temp0_sorted[indx] == temp0_sorted[indx+1]:
# 						if (temp_classi_sorted[indx]) > (temp_classi_sorted[(indx+1)]):
# 							a, b, c = temp0_sorted[indx], x_sorted[indx], temp_classi_sorted[indx]
# 							temp0_sorted[indx], x_sorted[indx], temp_classi_sorted[indx] = temp0_sorted[indx+1], x_sorted[indx+1], temp_classi_sorted[indx+1]
# 							temp0_sorted[indx+1], x_sorted[indx+1], temp_classi_sorted[indx+1] = a, b, c

# 				if indx >= len(temp0_sorted) - 3:
# 					break
# 			index2 = index2 + 1

# if  11 < rows[0][4]:
# 	indx = 0
# 	while indx < 7:
# 		for index in range(len(temp0_sorted)-1):
# 			if temp0_sorted[index] == temp0_sorted[index+1]:
# 				if temp_classi_sorted[index] < temp_classi_sorted[index+1]:
# 					temp_classi_sorted[index], temp_classi_sorted[index+1] = temp_classi_sorted[index+1], temp_classi_sorted[index]
# 					temp0_sorted[index], temp0_sorted[index+1] = temp0_sorted[index+1], temp0_sorted[index]
# 					x_sorted[index], x_sorted[index+1] = x_sorted[index+1], x_sorted[index]

# 		indx = indx+1

# for index, z in enumerate(x_sorted):
# 	print(z)
# 	if index==2:
# 		break
# conn.close()
# # var_dump.var_dump(part1)
# # var_dump.var_dump(part3)