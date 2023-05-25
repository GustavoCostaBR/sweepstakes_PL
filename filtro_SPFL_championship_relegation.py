import sys
import sqlite3
import var_dump
import pdb

conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

x = sys.argv[1:]
# x = ['Aberdeen x Hibernian - P2 (SPFL) - 20/05 - 15:45']
temp = []
temp1 = []
temp1_2 = []
temp0=[]
# print(x)

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table_relegation")
rows = cursor.fetchall()
cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table_championship")
rows2 = cursor.fetchall()
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
		#a partir da rodada 33
		if rows2[0][4] > 32:
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
			#Para o championship
			if z == 1:
				diff = abs(temp1[index][2]-temp1[index+1][2])
				positionto_1 = temp1[index][0] - rows2[0][0]
				positionto_1_2 =  temp1[index+1][0] - rows2[0][0]
				pointstofirst_1 = abs(temp1[index][2] - rows2[0][2])
				# print(pointstofirst_1)
				pointstofirst_2 = abs(temp1[index+1][2] - rows2[0][2])
				# print(pointstofirst_2)
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
			# Os 1000 escritos aqui são uma gambiarra para não confundir relegation com championship, tive que adapatar o código e essa foi a forma mais rápida de corrigir o problema sem pensar.

			#para o relegation
			if z == 0:
				diff = 1000
				positionto_1 = 1000
				positionto_1_2 =  1000
				pointstofirst_1 = 1000
				# print(pointstofirst_1)
				pointstofirst_2 = 1000
				# print(pointstofirst_2)
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


			#rodada 33 a 36
			if rows2[0][4] < 36:
				# print("aqui")
			# critehrio 3 pontos/uel
				if 0 <= positionto_3 <= 2 and 0 <= positionto_3_2 <= 2 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
					temp0.append(9)

			#critehrio primeiro colocado

				elif positionto_1 == 0 and diff <=5:
					# print(diff)
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=5:
					# print(diff)
					temp0.append(10)
				elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:

					temp0.append(10)

			# critehrio do ultimo colocado
				elif rows[0][4] > 34 and pointstolast_1 <= 3 and pointstolast_2 <= 3:
					temp0.append(8)

				else:
					temp0.append(1)
			#rodada 37

			elif rows2[0][4] == 36:

			# critehrio 3 pontos/uel
				if 0 <= positionto_3 <= 2 and 0 <= positionto_3_2 <= 2 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
					temp0.append(9)

			# critehrio do ultimo colocado
				elif rows[0][4] > 34 and pointstolast_1 <= 3 and pointstolast_2 <= 3:
					temp0.append(8)

			#critehrio primeiro colocado

				elif positionto_1 == 0 and diff <=3:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff <=3:
					temp0.append(10)
				elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					temp0.append(10)
				else:
					temp0.append(1)
			#rodada 38
			elif rows2[0][4] == 37:

			# critehrio 3 pontos/uel
			# Aqui eu abri espaço para 4 times na disputa do terceiro lugar, não faz sentido limitarmos isso, creio
				if 0 <= positionto_3 <= 3 and 0 <= positionto_3_2 <= 3 and pointstothird_1 <= 3 and pointstothird_2 <= 3:
					if goalstothird_1 <= 7 and goalstothird_2 <= 7:
						temp0.append(9)
					elif goalstothird_1 <= 7 and pointstothird_2 < 3:
						temp0.append(9)
					elif goalstothird_2 <= 7 and pointstothird_1 < 3:
						temp0.append(9)
					elif pointstothird_2 < 3 and pointstothird_1 < 3:
						temp0.append(9)
					else:
						temp0.append(1)
			# critehrio do ultimo colocado
				elif rows[0][4] > 34 and pointstolast_1 <= 3 and pointstolast_2 <= 3 and goalstolast_1 <= 7 and goalstolast_2 <= 7:
					temp0.append(8)

			#critehrio primeiro colocado

				elif positionto_1 == 0 and diff == 3 and goalstofirst_2 <= 7:
					temp0.append(10)
				elif positionto_1 == 0 and diff < 3:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff == 3 and goalstofirst_1 <= 7:
					temp0.append(10)
				elif positionto_1_2 == 0 and diff < 3:
					temp0.append(10)
				elif pointstofirst_1 <= 3 and pointstofirst_2 <= 3:
					if goalstofirst_2 <= 7 and goalstofirst_1 <= 7:
						temp0.append(10)
					elif pointstofirst_1 < 3 and pointstofirst_2 < 3:
						temp0.append(10)
					elif goalstofirst_2 <= 7 and pointstofirst_1 < 3:
						temp0.append(10)
					elif goalstofirst_1 <= 7 and pointstofirst_2 < 3:
						temp0.append(10)
					else:
						temp0.append(1)
				else:
					temp0.append(1)



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

print(temp0)
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