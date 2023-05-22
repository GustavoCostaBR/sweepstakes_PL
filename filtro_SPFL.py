import sys
import sqlite3
import var_dump

conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

# x = sys.argv[1:]
x = ['Inverness CT x St. Johnstone - P2 (SPFL - playoff) - 20/05 - 15:45', 'St. Johnstone x Inverness CT - P2 (SPFL - playoff) - 23/05 - 15:45']
temp = []
temp1 = []
temp1_2 = []
temp0=[]
cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table")
rows = cursor.fetchall()
cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table_championship")
rows2 = cursor.fetchall()
for row in rows:
	print(row)

for y in x:
	parts = y.split(" x ")
	part1 = parts[0]
	part2 = parts[1].split(" - ")
	part3 = part2[0]
	temp.append(part1)
	temp.append(part3)


	# if part1 in
	# cursor.execute("SELECT [Número de jogos] FROM scottish_premiership_table")
	# resultado = cursor.fetchone()[0]

for index, j in enumerate(temp):
	if index % 2 == 0:
		# rodada 2 a 33
		if rows[0][4] > 2 and rows[0][4] < 33:
			for row in rows:
				if j in row:
					temp1.append(row)
				elif temp[index+1] in row:
					temp1.append(row)
			diff = abs(temp1[index][2]-temp1[index+1][2])
			positionto_1 = temp1[index][0] - rows[0][0]
			positionto_1_2 =  temp1[index+1][0] - rows[0][0]
			pointstofirts_1 = abs(temp1[index][2] - rows[0][2])
			pointstofirst_2 = abs(temp1[index+1][2] - rows[0][2])

			# rodada 3 a 11
			if rows[0][4] <11:
				if positionto_1 == 0 and diff <=3:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=3:
					temp0.append(10)
				elif pointstofirts_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(10)

			# rodada 11 a 33
			elif rows[0][4] > 10 and rows[0][4] <33:
				if positionto_1 == 0 and diff <=5:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=5:
					temp0.append(10)
				elif pointstofirts_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(10)

		#a partir da rodada 33
		elif rows2[0][4] > 32 and rows2[0][4] < 38:
			for row in rows2:
				if j in row:
					temp1.append(row)
				elif temp[index+1] in row:
					temp1.append(row)
			diff = abs(temp1[index][2]-temp1[index+1][2])
			positionto_1 = temp1[index][0] - rows2[0][0]
			positionto_1_2 =  temp1[index+1][0] - rows2[0][0]
			pointstofirts_1 = (temp1[index][2] - rows2[0][2])
			pointstofirst_2 = (temp1[index+1][2] - rows2[0][2])
			goalstofirts_1 = (temp1[index][3] - rows2[0][3])
			goalstofirts_2 = (temp1[index+1][3] - rows2[0][3])

			#rodada 33 a 36
			if rows2[0][4] < 36:
				if positionto_1 == 0 and diff <=5:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=5:
					temp0.append(10)
				elif pointstofirts_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(10)

			#rodada 37
			elif rows2[0][4] == 36:

				if positionto_1 == 0 and diff <=3:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=3:
					temp0.append(10)
				elif pointstofirts_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(10)

			#rodada 38
			elif rows2[0][4] == 37:

				if positionto_1 == 0 and diff <=3 and goalstofirts_2 <= 7:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=3 and goalstofirts_1 <= 7:
					temp0.append(10)
				elif pointstofirts_1 <= 3 and pointstofirst_2 <= 3 and goalstofirts_2 <= 7 and goalstofirts_1 <= 7:
					temp0.append(10)

# 			if rows[0][4] > 22 and rows[0][4] <33:
# 				for row in rows:
# 					if j in row:
# 						temp1.append(row)
# 					elif temp[index+1] in row:
# 						temp1.append(row)
# conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)