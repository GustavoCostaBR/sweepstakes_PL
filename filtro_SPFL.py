import sys
import sqlite3
import var_dump
import pdb

conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

x = sys.argv[1:]
# x = ['Livingston x Rangers - P1 (SPFL) - 30/07 - 08:00', 'Kilmarnock x Dundee United - P1 (SPFL) - 30/07 - 11:00', 'Heart of Midlothian x Ross County - P1 (SPFL) - 30/07 - 11:00', 'St. Johnstone x Hibernian - P1 (SPFL) - 30/07 - 11:00', 'St. Mirren x Motherwell - P1 (SPFL) - 31/07 - 11:00', 'Celtic x Aberdeen - P1 (SPFL) - 31/07 - 12:30']
# x = ['Aberdeen x Hibernian - P2 (SPFL) - 20/05 - 15:45']
temp = []
temp1 = []
temp1_2 = []
temp0=[]
# print(x)


cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table")
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
		# rodada inicial
		if rows[0][4] == 0:
			if "Celtic" in x[index//2]:
				temp0.append(9)
			elif "Rangers" in x[index//2]:
				temp0.append(8)
			elif "Aberdeen" in x[index//2]:
				temp0.append(7)
			elif "Heart of Midlothian" in x[index//2]:
				temp0.append(6)
			elif "Hibernian" in x[index//2]:
				temp0.append(5)
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
			# print(pointstofirst_1)
			pointstofirst_2 = abs(temp1[index+1][2] - rows[0][2])
			# print(pointstofirst_2)
			positionto_3 = temp1[index][0] - rows[2][0]
			positionto_3_2 =  temp1[index+1][0] - rows[2][0]
			pointstothird_1 = (rows[2][2] - temp1[index][2])
			pointstothird_2 = (rows[2][2] - temp1[index+1][2])
			# rodada 3 a 11

			if rows[0][4] <11:
			# critehrio do primeiro colocado
				if positionto_1 == 0 and diff <=3:
					temp0.append(12)
				elif positionto_1_2 == 0 and diff <=3:
					temp0.append(12)
				elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(12)

			# rodada 11 a 33
			elif rows[0][4] > 10 and rows[0][4] <33:

			# critehrio 3 pontos/uel
				if 0 <= positionto_3 <= 2 and 0 <= positionto_3_2 <= 2 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
					if rows[0][4] > 22:
						temp0.append(11)
					else:
						temp0.append(1)
			#critehrio primeiro colocado
				elif positionto_1 == 0 and diff <=5:
					temp0.append(12)
				elif positionto_1_2 == 0 and diff <=5:
					temp0.append(12)
				elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(12)

				else:
					temp0.append(1)

		# jogo do primeiro colocado
			if positionto_1 == 0 or positionto_1_2 == 0:
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

sorted_values = sorted(zip(temp0, x), reverse=True)
temp0_sorted, x_sorted = map(list, zip(*sorted_values))
filtrado = []
# print(x_sorted[0])
# for u in x_sorted:
# 	filtrado.append(u)


# temp0_sorted, x_sorted = sorted((temp0, x), reverse=True)
# a_sorted, b_sorted, c_sorted = map(list, zip(*sorted_values))

# print(temp0)
# print(x)
# print("\n")
# print(temp0_sorted)
# print(filtrado[0:3])
# print(temp0_sorted)
for index, z in enumerate(x_sorted):
	print(z)
	if index==2:
		break
conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)