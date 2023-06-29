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

# x = ['Time1 x Time10 - P1 (PL) - 20/05 - 08:30', 'Time2 x Time15 - P1 (PL) - 20/05 - 08:30', 'Time3 x Time4 - P1 (PL) - 20/05 - 08:30','Time5 x Time6 - P1 (PL) - 20/05 - 08:30','Time7 x Time17 - P1 (PL) - 20/05 - 08:30','Time8 x Time14 - P1 (PL) - 20/05 - 08:30','Time9 x Time13 - P1 (PL) - 20/05 - 08:30','Time11 x Time12 - P1 (PL) - 20/05 - 08:30','Time16 x Time20 - P1 (PL) - 20/05 - 08:30','Time18 x Time19 - P1 (PL) - 20/05 - 08:30']

# x = ['Time1 x Time2 - P1 (PL) - 20/05 - 08:30', 'Time3 x Time4 - P1 (PL) - 20/05 - 08:30', 'Time5 x Time6 - P1 (PL) - 20/05 - 08:30','Time7 x Time8 - P1 (PL) - 20/05 - 08:30','Time9 x Time10 - P1 (PL) - 20/05 - 08:30','Time11 x Time12 - P1 (PL) - 20/05 - 08:30','Time13 x Time14 - P1 (PL) - 20/05 - 08:30','Time15 x Time16 - P1 (PL) - 20/05 - 08:30','Time17 x Time18 - P1 (PL) - 20/05 - 08:30','Time19 x Time20 - P1 (PL) - 20/05 - 08:30']



ones_list = [1] * 12
temp = []
temp1 = []
temp1_2 = []
temp0=[]
temp_classi = []
# print(x)

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

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM premiere_league_table")
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

		# rodada 2 a 33
		if rows[0][4] >= 1:

			for row in rows:
				if j in row:
					temp1.append(row)
				elif temp[index+1] in row:
					temp1.append(row)
			# print(temp1)
			# pdb.set_trace()
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


			# if temp[index] == "Tottenham Hotspur":
			# 	pdb.set_trace()

			# Primeiro turno
			if 4 <= rows[0][4] <= 18:
			#critehrio do primeiro colocado
				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# Critehrio do top6
				elif (p(1, index, 0) <= 5 and p(1, index+1,0) <= 5) or (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P2")

			# critehrio do EUROPA_LEAGUE

			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and p(1, index, 6) < 0 and p(1, index+1, 6) < 0:
					x[index//2] = x[index//2].replace("P1", "P2")
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and (p(1, index+1, 0) >= 6)) or ((1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) and (p(1, index, 0) >= 6)) :
					x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE EUROPA_LEAGUE
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P2")


			# rodada 19 a 36
			elif 4 <=rows[0][4] <= 35:

			#critehrio do primeiro colocado
				# 3 pontos
				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

				#  5 pontos desde que um seja o lider de fato
				elif (pointstofirst_1 <=5 and positionto_1_2 == 0) or (pointstofirst_2 <=5 and positionto_1 == 0):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# Critehrio do top6
				elif (p(1, index, 0) <= 5 and p(1, index+1,0) <= 5) or (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P2")



			# critehrio do EUROPA_LEAGUE

			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and p(1, index, 6) < 0 and p(1, index+1, 6) < 0:
					x[index//2] = x[index//2].replace("P1", "P2")
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and (p(1, index+1, 0) >= 6)) or ((1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3) and (p(1, index, 0) >= 6)) :
					x[index//2] = x[index//2].replace("P1", "P2")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE EUROPA_LEAGUE
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P2")





			# forçando para sempre verificar
				if rows[0][4] >= 33:

			# critehrio da zona de rebaixamento
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
					if (0 >= p(0, index, 16) >= (-3) and 0 >= p(0, index+1, 16) >= (-3)) and (p(1, index, 16) >= 1 and p(1, index+1, 16) >= 1):
						x[index//2] = x[index//2].replace("P1", "P2")
						if rows[0][4] >= 35:
							x[index//2] = x[index//2].replace("P2", "P3")


				# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
					elif  (p(1, index, 17) >= 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and p(1, index+1, 17) < 0) or (p(1, index+1, 17) >= 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and p(1, index, 17) < 0):
						x[index//2] = x[index//2].replace("P1", "P2")
						if rows[0][4] >= 35:
							x[index//2] = x[index//2].replace("P2", "P3")

				# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
					elif(p(1, index, 16) <= 0 and p(1, index+1, 16) <= 0) and (p(0, index, 17) <= 3 and p(0, index+1, 17) <= 3):
						x[index//2] = x[index//2].replace("P1", "P2")
						if rows[0][4] >= 35:
							x[index//2] = x[index//2].replace("P2", "P3")








					if rows[0][4] == 35:

					# critehrio do champions
					# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
						if (0 <= p(0, index, 4) <=3 and 0 <= p(0, index+1, 4) <= 3) and p(1, index, 4) < 0 and p(1, index+1, 4) < 0:
							x[index//2] = x[index//2].replace("P1", "P3")
							x[index//2] = x[index//2].replace("P2", "P3")
					# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
						elif  (1 < p(1, index, 0) < 4 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and p(1, index+1, 0) >= 4) or (1 < p(1, index+1, 0) < 4 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and p(1, index, 0) >= 4):
							x[index//2] = x[index//2].replace("P1", "P3")
							x[index//2] = x[index//2].replace("P2", "P3")

					# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE CHAMPIONS
						elif(p(1, index, 3) > 0 and p(1, index+1, 3) > 0) and (p(0, index, 3) >= (-3) and p(0, index+1, 3) >= (-3)):
							x[index//2] = x[index//2].replace("P1", "P3")
							x[index//2] = x[index//2].replace("P2", "P3")

					# critehrio do EUROPA_LEAGUE

					# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
						elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and p(1, index, 6) < 0 and p(1, index+1, 6) < 0:
							x[index//2] = x[index//2].replace("P1", "P3")
							x[index//2] = x[index//2].replace("P2", "P3")
					# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
						elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and p(1, index+1, 0) >= 6) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and p(1, index, 0) >= 6):
							x[index//2] = x[index//2].replace("P1", "P3")
							x[index//2] = x[index//2].replace("P2", "P3")

					# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE EUROPA_LEAGUE
						elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
							x[index//2] = x[index//2].replace("P1", "P3")
							x[index//2] = x[index//2].replace("P2", "P3")


			# RODADA 37
			elif rows[0][4] == 36:

			#critehrio do primeiro colocado
				# 3 pontos
				if pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


		# critehrio da zona de rebaixamento
		# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 >= p(0, index, 16) >= (-3) and 0 >= p(0, index+1, 16) >= (-3)) and (p(1, index, 16) >= 1 and p(1, index+1, 16) >= 1):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (p(1, index, 17) >= 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and p(1, index+1, 17) < 0) or (p(1, index+1, 17) >= 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and p(1, index, 17) < 0):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
				elif(p(1, index, 16) <= 0 and p(1, index+1, 16) <= 0) and (p(0, index, 17) <= 3 and p(0, index+1, 17) <= 3):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


			# critehrio da champions
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 4) <=3 and 0 <= p(0, index+1, 4) <= 3) and p(1, index, 4) < 0 and p(1, index+1, 4) < 0:
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 4 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and p(1, index+1, 0) >= 4) or (1 < p(1, index+1, 0) < 4 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and p(1, index, 0) >= 4):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE CHAMPIONS
				elif(p(1, index, 3) > 0 and p(1, index+1, 3) > 0) and (p(0, index, 3) >= (-3) and p(0, index+1, 3) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# critehrio do EUROPA_LEAGUE

			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (0 <= p(0, index, 6) <=3 and 0 <= p(0, index+1, 6) <= 3) and p(1, index, 6) < 0 and p(1, index+1, 6) < 0:
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")
			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (1 < p(1, index, 0) < 6 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 3 and p(1, index+1, 0) >= 6) or (1 < p(1, index+1, 0) < 6 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 3 and p(1, index, 0) >= 6):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE EUROPA_LEAGUE
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# Critehrio do top6
				elif (p(1, index, 0) <= 5 and p(1, index+1,0) <= 5) or (p(0, index, 5) >= (-3) and p(0, index+1, 5) >= (-3)):
					x[index//2] = x[index//2].replace("P1", "P2")



			# RODADA 38
			elif rows[0][4] == 37:
				# if index == 6:
					# pdb.set_trace()
			#critehrio do primeiro colocado
				if ((pointstofirst_1 <= 3 and p(2, index, 0) >= (-7)) or (pointstofirst_1 <= 2)) and ((pointstofirst_2 <= 3 and p(2, index+1, 0) >=(-7)) or (pointstofirst_2 <= 2)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# critehrio da zona de rebaixamento
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif (((0 >= p(0, index, 16) == (-3) and p(2, index, 16) >= (-7)) or (0 >= p(0, index, 16) >= (-2))) and ((0 >= p(0, index+1, 16) == (-3) and p(2, index+1, 16) >= (-7)) or (0 >= p(0, index+1, 16) >= (-2))) and (p(1, index, 16) >= 1 and p(1, index+1, 16) >= 1)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  (((p(1, index, 17) >= 0 and (p(2, index+1, 0)-p(2, index, 0)) <= 7 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) == 3) or (p(1, index, 17) >= 0 and 0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2)) and (p(1, index+1, 17) < 0)) or (((p(1, index+1, 17) >= 0 and (p(2, index, 0)-p(2, index+1, 0)) <= 7 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) == 3) or (p(1, index+1, 17) >= 0 and 0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2)) and (p(1, index, 17) < 0)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DA DEGOLA
				elif ((p(1, index, 16) <= 0 and p(0, index, 17) == 3 and p(2, index, 17) <= 7) or (p(1, index, 16) <= 0 and p(0, index, 17) <= 2)) and ((p(0, index+1, 17) == 3 and p(1, index+1, 16) <= 0 and p(2, index+1, 17) <= 7) or (p(1, index+1, 16) <= 0 and p(0, index+1, 17) <= 2)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")



			# critehrio da champions
			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif ((0 <= p(0, index, 4) ==3 and p(2, index,4) <= 7) or 0 <= p(0, index, 4) <=2) and ((0 <= p(0, index+1, 4) == 3 and p(2, index+1,4) <= 7) or 0 <= p(0, index+1, 4) <=2) and (p(1, index, 4) < 0 and p(1, index+1, 4) < 0):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")

			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  ((1 < p(1, index, 0) < 4 and p(1, index+1, 0) >= 4) and ((0 <= (p(0, index, 0)-p(0, index+1, 0)) == 3 and (p(2, index, 0)-p(2, index+1, 0)) <= 7) or ((0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2)))) or ((1 < p(1, index+1, 0) < 4 and p(1, index, 0) >= 4) and ((0 <= (p(0, index+1, 0)-p(0, index, 0)) == 3 and (p(2, index+1, 0)-p(2, index, 0)) <= 7) or ((0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2)))):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE CHAMPIONS
				elif(p(1, index, 3) > 0 and p(1, index+1, 3) > 0) and ((p(0, index, 3) == (-3) and p(2, index, 3) >= (-7)) or p(0, index, 3) >= (-2)) and ((p(0, index+1, 3) == (-3) and p(2, index+1, 3) >= (-7)) or p(0, index+1, 3) >= (-2)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")



			# critehrio do EUROPA_LEAGUE

			# OS DOIS TIMES DENTRO SEPARADOS DO PRIMEIRO FORA DELA POR ATÉ 3 PONTOS
				elif ((0 <= p(0, index, 6) == 3 and p(2, index, 6) <= 7) or 0 <= p(0, index, 6) <=2) and ((0 <= p(0, index+1, 6) == 3 and p(2, index+1,6) <= 7) or 0 <= p(0, index+1, 6) <=2) and (p(1, index, 6) < 0 and p(1, index+1, 6) < 0):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


			# UM DENTRO E OUTRO FORA SEPARADOS POR ATÉ 3 PONTOS
				elif  ((1 < p(1, index, 0) < 6 and p(1, index+1, 0) >= 6) and ((0 <= (p(0, index, 0)-p(0, index+1, 0)) == 3 and (p(2, index, 0)-p(2, index+1, 0)) <= 7) or ((0 <= (p(0, index, 0)-p(0, index+1, 0)) <= 2)))) or ((1 < p(1, index+1, 0) < 6 and p(1, index, 0) >= 6) and ((0 <= (p(0, index+1, 0)-p(0, index, 0)) == 3 and (p(2, index+1, 0)-p(2, index, 0)) <= 7) or ((0 <= (p(0, index+1, 0)-p(0, index, 0)) <= 2)))):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


			# OS DOIS FORA COM ATÉ 3 PONTOS PARA ENTRAR NA ZONA DE EUROPA_LEAGUE
				elif(p(1, index, 5) > 0 and p(1, index+1, 5) > 0) and ((p(0, index, 5) == (-3) and p(2, index, 5) >= (-7)) or p(0, index, 5) >= (-2)) and ((p(0, index+1, 5) == (-3) and p(2, index+1, 5) >= (-7)) or p(0, index+1, 5) >= (-2)):
					x[index//2] = x[index//2].replace("P1", "P3")
					x[index//2] = x[index//2].replace("P2", "P3")


			# Critehrio do top6
				elif (p(1, index, 0) <= 5 and p(1, index+1,0) <= 5) or (((p(0, index, 5) == (-3) and p(2, index, 5) >= (-7)) or (p(0, index, 5) >= (-3))) and ((p(0, index+1, 5) == (-3) and p(2, index+1, 5) >= (-7)) or p(0, index+1, 5) >= (-2))):
					x[index//2] = x[index//2].replace("P1", "P2")



for index, z in enumerate(x):
	print(z)
conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)