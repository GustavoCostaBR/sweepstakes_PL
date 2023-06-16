import sys
import sqlite3
import var_dump
import pdb

conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

def p(choice ,index, positionr):
	global rows0
	global temp1
	if choice == 0:
		points_1 = (temp1[index][2] - rows0[positionr][2])
		# points_2 = (temp1[index+1][2] - rows[positionr][2])
		# return points_1, points_2
		return points_1
	elif choice == 1:
		posi_1 = (temp1[index][0] - rows0[positionr][0])
		# posi_2 = (temp1[index+1][0] - rows[positionr][0])
		# return posi_1, posi_2
		return posi_1
	elif choice == 2:
		goals_1 = (temp1[index][3] - rows0[positionr][3])
		# goals_2 = (temp1[index+1][3] - rows[positionr][3])
		# return goals_1, goals_2
		return goals_1
	elif choice == 3:
		points_1 = (temp1[index][2] - rows0[positionr][2])
		# points_2 = (temp1[index+1][2] - rows[positionr][2])
		goals_1 = (temp1[index][3] - rows0[positionr][3])
		# goals_2 = (temp1[index+1][3] - rows[positionr][3])
		# return points_1, points_2, goals_1, goals_2
		return points_1, goals_1

x = sys.argv[1:]
# x = ['Aberdeen x Hibernian - P2 (SPFL) - 20/05 - 15:45']
temp = []
temp1 = []
div = []
orgdiv = []
temp0=[]
# print(x)


cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM premiere_league_table")
rows0 = cursor.fetchall()

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM eng_championship_table")
rows1 = cursor.fetchall()

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM league_one_table")
rows2 = cursor.fetchall()

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM league_two_table")
rows3 = cursor.fetchall()

cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM national_league_table")
rows4 = cursor.fetchall()

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


for index, j in enumerate(temp):
	if index % 2 == 0:

		for row in rows0:
			if j in row:
				temp1.append(row)
				div.append(1)
			elif temp[index+1] in row:
				temp1.append(row)
				div.append(1)

		for row in rows1:
			if j in row:
				temp1.append(row)
				div.append(2)
			elif temp[index+1] in row:
				temp1.append(row)
				div.append(2)

		for row in rows2:
			if j in row:
				temp1.append(row)
				div.append(3)
			elif temp[index+1] in row:
				temp1.append(row)
				div.append(3)

		for row in rows3:
			if j in row:
				temp1.append(row)
				div.append(4)
			elif temp[index+1] in row:
				temp1.append(row)
				div.append(4)

		for row in rows4:
			if j in row:
				temp1.append(row)
				div.append(5)
			elif temp[index+1] in row:
				temp1.append(row)
				div.append(5)

		# Garantindo que se o time for da sexta divisão vai apender alguma coisa
		while (index+1) > len(div):
			div.append(6)
		#
		# Verificando se é um confronto top 6 da liga
		if div[index] == 1 and div[index+1] == 1:
			if p(1, index, 0) <= 5 and p(1, index+1, 0) <= 5:
				x[index//2] = x[index//2].replace("P1", "P2")

		#critehrio do derbie (considerarah confreonto top 6 como derbie, mas isso não vai fazer diferença nenhuma pra nos)
		orgdiv.append(int(div[index]+div[index+1]))
		if "P2" in x[index//2]:
			orgdiv[index//2] = 1


tempoo = []
index2=0

temp0_sorted, x_sorted = zip(*sorted(zip(orgdiv, x)))

# temp0_sorted, x_sorted = zip(*sorted(zip(temp0, x), reverse=True))

# sorted_values = sorted(zip(temp0, x), reverse=True)
# temp0_sorted, x_sorted = map(list, zip(*sorted_values))
# filtrado = []
# print(x_sorted[0])
# for u in x_sorted:
# 	filtrado.append(u)


# temp0_sorted, x_sorted = sorted((temp0, x), reverse=True)
# a_sorted, b_sorted, c_sorted = map(list, zip(*sorted_values))

# for index, z in enumerate(x):
# 	print(z)
# print(temp0_sorted)

for index, z in enumerate(x_sorted):
	print(z)
	if index==9:
		break
conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)