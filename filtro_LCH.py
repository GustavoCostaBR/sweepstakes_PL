import sys
import sqlite3
import var_dump
import pdb
import yaml

conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

with open('TIMES_PRIMEIRA_RODADA.yml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

x = sys.argv[1:]
# x = ['Aberdeen x Hibernian - P2 (SPFL) - 20/05 - 15:45']

# x = ['Birmingham City x Norwich City - P1 (LCH) - 30/08 - 15:45', 'Cardiff City x Luton Town - P1 (LCH) - 30/08 - 15:45', 'Burnley x Millwall - P1 (LCH) - 30/08 - 15:45', 'Queens Park Rangers x Hull City - P1 (LCH) - 30/08 - 15:45', 'Wigan Athletic x West Bromwich Albion - P1 (LCH) - 30/08 - 15:45', 'Sheffield United x Reading - P1 (LCH) - 30/08 - 15:45', 'Watford x Middlesbrough - P1 (LCH) - 30/08 - 16:00', 'Sunderland x Rotherham United - P1 (LCH) - 31/08 - 15:45', 'Bristol City x Huddersfield Town - P1 (LCH) - 31/08 - 15:45', 'Coventry City x Preston North End - P1 (LCH) - 31/08 - 15:45', 'Stoke City x Swansea City - P1 (LCH) - 31/08 - 15:45', 'Blackpool x Blackburn Rovers - P1 (LCH) - 31/08 - 16:00']

ones_list = [1] * 12
temp = []
temp1 = []
temp1_2 = []
temp0=[]
temp_classi = []
# print(x)

def p(choice ,index, positionr):
	global rows
	if choice == 0:
		points_1 = (temp1[index][2] - rows[positionr][2])
		# points_2 = (temp1[index+1][2] - rows[positionr][2])
		# return points_1, points_2
		return points_1
	elif choice == 1:
		posi_1 = (temp1[index][0] - rows[positionr][0])
		# posi_2 = (temp1[index+1][0] - rows[positionr][0])
		# return posi_1, posi_2
		return posi_1
	elif choice == 2:
		goals_1 = (temp1[index][3] - rows[positionr][3])
		# goals_2 = (temp1[index+1][3] - rows[positionr][3])
		# return goals_1, goals_2
		return goals_1
	elif choice == 3:
		points_1 = (temp1[index][2] - rows[positionr][2])
		# points_2 = (temp1[index+1][2] - rows[positionr][2])
		goals_1 = (temp1[index][3] - rows[positionr][3])
		# goals_2 = (temp1[index+1][3] - rows[positionr][3])
		# return points_1, points_2, goals_1, goals_2
		return points_1, goals_1

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM eng_championship_table")
rows = cursor.fetchall()

# for row in rows:
# 	print(row)

# for row in rows2:
# 	print(row)

for y in x:
	parts = y.split(" x ")
	part1 = parts[0]
	part2 = parts[1].split(" - ")
	part3 = part2[0]
	temp.append(part1)
	temp.append(part3)

# print(temp)
	# if part1 in
	# cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table")
	# resultado = cursor.fetchone()[0]

for index, j in enumerate(temp):
	# pdb.set_trace()
	if index % 2 == 0:
		# rodada 1
		if rows[0][4] == 0:
			if data['FIRST_ROUND_LCH']['TIME1'] in x[index//2]:
				# print('jorge')
				temp0.append(9)
			elif data['FIRST_ROUND_LCH']['TIME2'] in x[index//2]:
				temp0.append(8)
			elif data['FIRST_ROUND_LCH']['TIME3'] in x[index//2]:
				temp0.append(7)
			elif data['FIRST_ROUND_LCH']['TIME4'] in x[index//2]:
				temp0.append(6)
			elif data['FIRST_ROUND_LCH']['TIME5'] in x[index//2]:
				temp0.append(5)
			elif data['FIRST_ROUND_LCH']['TIME6'] in x[index//2]:
				temp0.append(4)
			elif data['FIRST_ROUND_LCH']['TIME7'] in x[index//2]:
				temp0.append(3)
			elif data['FIRST_ROUND_LCH']['TIME8'] in x[index//2]:
				temp0.append(2)
			else:
				temp0.append(1)
		# rodada 2 a 33
		if rows[0][4] >= 1:

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
			pointstosecond_1 = (temp1[index][2] - rows[1][2])
			pointstosecond_2 = (temp1[index+1][2] - rows[1][2])
			points1 = temp1[index][2]
			points2 = temp1[index+1][2]
			# print(pointstofirst_1)
			pointstofirst_2 = abs(temp1[index+1][2] - rows[0][2])
			# print(pointstofirst_2)
			positionto_3 = temp1[index][0] - rows[2][0]
			positionto_3_2 =  temp1[index+1][0] - rows[2][0]
			pointstothird_1 = (rows[2][2] - temp1[index][2])
			pointstothird_2 = (rows[2][2] - temp1[index+1][2])
			pointstosixth_1 = (rows[5][2] - temp1[index][2])
			pointstosixth_2 = (rows[5][2] - temp1[index+1][2])

			pointstoseventh_1 = (rows[6][2] - temp1[index][2])
			pointstoseventh_2 = (rows[6][2] - temp1[index+1][2])


			# rodada 2 a 12
			if rows[0][4] <=11:
				temp0.append(int(points1+points2))
				temp_classi.append(int(positionto_1))
				temp_classi.append(int(positionto_1_2))

				# if positionto_1 == 0 and diff <=3:

				# elif positionto_1_2 == 0 and diff <=3:
				# 	temp0.append(10)
				# elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
				# 	temp0.append(10)

			# rodada 13 a 23
			elif rows[0][4] < 23:


		#critehrio do primeiro colocado
				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(255)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
		#critehrio do segundo colocado
				elif 0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3):
					temp0.append(254)
		# critehrio do playoff
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and (p(1, index, 0) > 1 and p(1, index+1,0) > 1):
					temp0.append(253)
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3):
					temp0.append(253)

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					temp0.append(253)


		# critehrio da zona de rebaixamento
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) > 1 and p(1, index+1, 20) > 1):
					temp0.append(252)
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3):
					temp0.append(252)

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3):
					temp0.append(252)

		# critehrio de colocacao

				else:
					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))


		# rodada 24 a 44
			elif rows[0][4] < 44:


		#critehrio do primeiro colocado
				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(255)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
				elif (pointstofirst_1 <=5 and positionto_1_2 == 0) or (pointstofirst_2 <=5 and positionto_1 == 0):
					temp0.append(255)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

		#critehrio do segundo colocado
				elif 0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3):
					temp0.append(254)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
		# critehrio do playoff
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and (p(1, index, 0) > 1 and p(1, index+1,0) > 1):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P2")
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P2")

		# critehrio da zona de rebaixamento
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) > 1 and p(1, index+1, 20) > 1):
					temp0.append(252)
					if rows[0][4] >= 43:
						x[index//2] = x[index//2].replace("P1", "P2")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3):
					temp0.append(252)
					if rows[0][4] >= 43:
						x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3):
					temp0.append(252)
					if rows[0][4] >= 43:
						x[index//2] = x[index//2].replace("P1", "P2")
		# critehrio de colocacao

				else:
					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))


		# rodada 45
			elif rows[0][4] < 45:


		#critehrio do primeiro colocado
				if (pointstofirst_1 <= 3 and pointstofirst_2 <= 3):
					temp0.append(255)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

		#critehrio do segundo colocado
				elif 0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3):
					temp0.append(254)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
		# critehrio do playoff
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and (p(1, index, 0) > 1 and p(1, index+1,0) > 1):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P2")
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P2")

		# critehrio da zona de rebaixamento
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) > 1 and p(1, index+1, 20) > 1):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")
		# critehrio de colocacao

				else:
					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))


		# rodada 46
			elif rows[0][4] == 45:


		#critehrio do primeiro colocado
				if (pointstofirst_1 <= 3 and pointstofirst_2 <= 3) and (p(2, index, 0) >= (-6) and p(2, index+1, 0) >=(-6)):
					temp0.append(255)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
				elif (pointstofirst_1 <= 2 and pointstofirst_2 <= 2):
					temp0.append(255)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

		#critehrio do segundo colocado
				elif (0 >= pointstosecond_1 >= (-3) and 0 >= pointstosecond_2 >= (-3)) and (p(2, index, 1) >= (-6) and p(2, index+1, 1) >= (-6)):
					temp0.append(254)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

				elif (0 >= pointstosecond_1 >= (-2) and 0 >= pointstosecond_2 >= (-2)):
					temp0.append(254)
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

		# critehrio do playoff
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <= 3 and 0 <= p(0, index+1, 6) <= 3) and (p(2, index,6) >= 6 and p(2, index+1,6) >= 6 ) and (p(1, index, 0) > 1 and p(1, index+1,0) > 1):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P3")

				elif (0 <= p(0, index, 6) <=2 and 0 <= p(0, index+1, 6) <= 2) and (p(1, index, 0) > 1 and p(1, index+1,0) > 1):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P3")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and (p(2, index, 0)-p(2, index+1, 0)) <= 6) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and (p(2, index+1, 0)-p(2, index, 0)) <= 6):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P3")

				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P3")


			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE PLAYOFF
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)) and (p(2, index, 5) >= (-6) and p(2, index+1, 5) >= (-6)):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P3")

				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-2) and p(0, index+1, 5) >= (-2)):
					temp0.append(253)
					x[index//2] = x[index//2].replace("P1", "P3")

		# critehrio da zona de rebaixamento
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 >= p(0, index, 20) >= (-3) and 0 >= p(0, index+1, 20) >= (-3)) and (p(1, index, 20) > 1 and p(1, index+1, 20) > 1) and (p(2, index, 20) >= (-6) and p(2, index+1, 20) >= (-6)):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

				elif (0 >= p(0, index, 20) >= (-2) and 0 >= p(0, index+1, 20) >= (-2)) and (p(1, index, 20) > 1 and p(1, index+1, 20) > 1):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and (p(2, index+1, 0)-p(2, index, 0)) <= 6) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and (p(2, index, 0)-p(2, index+1, 0)) <= 6):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

				elif  (p(1, index, 20) > 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2) or (p(1, index+1, 20) > 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 3 and p(0, index+1, 21) <= 3) and (p(2, index, 21) <= 6 and p(2, index+1, 21) <= 6):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")

				elif(p(1, index, 20) <= 0 and p(1, index+1, 20) <= 0) and (p(0, index, 21) <= 2 and p(0, index+1, 21) <= 2):
					temp0.append(252)
					x[index//2] = x[index//2].replace("P1", "P2")
		# critehrio de colocacao

				else:
					temp0.append(149-int(min(p(1, index, 0), p(1, index, 0))))



		#critehrio do derbie
		if temp0[index//2] < 250 and  "P2" in x[index//2]:
			temp0[index//2] = 250
# print(temp)
# print(temp0)
tempoo = []
index2=0
# for index, y in enumerate(temp):
# 	if index%2 == 0:
# 		for z in x:
# 			if y in z:
# 				tempoo.append(z)
# temp0_sorted, x_sorted = zip(*sorted(zip(temp0, x), reverse=True))

# temp0_sorted, x_sorted = zip(*sorted(zip(temp0, x), reverse=True))
a = "z"
b = "z"
c = "z"
d = "z"
index2 = 0
sorted_values = sorted(zip(temp0, x), reverse=True)
temp0_sorted, x_sorted = map(list, zip(*sorted_values))
filtrado = []
# print(x_sorted[0])
# for u in x_sorted:
# 	filtrado.append(u)
# print(temp0_sorted)
# print(x_sorted)
if rows[0][4] <=11:
	if temp0_sorted[2] == temp0_sorted[3]:
		while index2 < 5:
			for indx in range(len(temp0_sorted)):
				if indx%2 == 0:
					if temp0_sorted[indx] == temp0_sorted[indx+1]:
						if min(temp_classi[int(indx*2)], temp_classi[int((indx*2)+1)]) > min(temp_classi[int((indx+1)*2)], temp_classi[int(((indx+1)*2)+1)]):
							a, b, c, d = temp0_sorted[indx], x_sorted[indx], temp_classi[int(indx*2)], temp_classi[int((indx*2)+1)]
							temp0_sorted[indx], x_sorted[indx], temp_classi[int(indx*2)], temp_classi[int((indx*2)+1)] = temp0_sorted[indx+1], x_sorted[indx+1], temp_classi[int((indx+1)*2)], temp_classi[int(((indx+1)*2)+1)]
							temp0_sorted[indx+1], x_sorted[indx+1], temp_classi[int((indx+1)*2)], temp_classi[int(((indx+1)*2)+1)] = a, b, c, d

				# if indx >= len(temp0_sorted) - 3:
				# 	break

			for indx in range(len(temp0_sorted)):
				if indx%2 == 1:
					if temp0_sorted[indx] == temp0_sorted[indx+1]:
						if min(temp_classi[int(indx*2)], temp_classi[int((indx*2)+1)]) > min(temp_classi[int((indx+1)*2)], temp_classi[int(((indx+1)*2)+1)]):
							a, b, c, d = temp0_sorted[indx], x_sorted[indx], temp_classi[int(indx*2)], temp_classi[int((indx*2)+1)]
							temp0_sorted[indx], x_sorted[indx], temp_classi[int(indx*2)], temp_classi[int((indx*2)+1)] = temp0_sorted[indx+1], x_sorted[indx+1], temp_classi[int((indx+1)*2)], temp_classi[int(((indx+1)*2)+1)]
							temp0_sorted[indx+1], x_sorted[indx+1], temp_classi[int((indx+1)*2)], temp_classi[int(((indx+1)*2)+1)] = a, b, c, d

				if indx >= len(temp0_sorted) - 3:
					break
			index2 = index2 + 1

# temp0_sorted, x_sorted = sorted((temp0, x), reverse=True)
# a_sorted, b_sorted, c_sorted = map(list, zip(*sorted_values))

# print(temp0)
# print(x)
# print("\n")
# print(temp0_sorted)
# print(filtrado[0:3])
for index, z in enumerate(x_sorted):
	print(z)
	if index==2:
		break
conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)