import sys
import sqlite3
import var_dump
import pdb
import yaml
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
# x = ['Manchester City x Arsenal - P1 (FAC) - 27/01 - 16:00 zzz1:0 (0:0) ', 'Walsall x Leicester City - P1 (FAC) - 28/01 - 08:30 zzz0:1 (0:0) ', 'Accrington Stanley x Leeds United - P1 (FAC) - 28/01 - 08:30 zzz1:3 (0:1) ', 'Southampton x Blackpool - P1 (FAC) - 28/01 - 11:00 zzz2:1 (1:0) ', 'Ipswich Town x Burnley - P1 (FAC) - 28/01 - 11:00 zzz0:0 (0:0) ', 'Luton Town x Grimsby Town - P1 (FAC) - 28/01 - 11:00 zzz2:2 (0:1) ', 'Sheffield Wednesday x Fleetwood Town - P1 (FAC) - 28/01 - 11:00 zzz1:1 (0:0) ', 'Fulham x Sunderland - P1 (FAC) - 28/01 - 11:00 zzz1:1 (0:1) ', 'Bristol City x West Bromwich Albion - P1 (FAC) - 28/01 - 11:00 zzz3:0 (2:0) ', 'Blackburn Rovers x Birmingham City - P1 (FAC) - 28/01 - 11:00 zzz2:2 (1:1) ', 'Preston North End x Tottenham Hotspur - P1 (FAC) - 28/01 - 14:00 zzz0:3 (0:0) ', 'Manchester United x Reading - P1 (FAC) - 28/01 - 16:00 zzz3:1 (0:0) ', 'Brighton & Hove Albion x Liverpool - P1 (FAC) - 29/01 - 09:30 zzz2:1 (1:1) ', 'Stoke City x Stevenage - P1 (FAC) - 29/01 - 10:00 zzz3:1 (1:0) ', 'Wrexham x Sheffield United - P1 (FAC) - 29/01 - 12:30 zzz3:3 (0:1) ', 'Derby County x West Ham United - P1 (FAC) - 30/01 - 15:45 zzz0:2 (0:1) ']

temp = []
temp1 = []
div = []
orgdiv = []
temp0=[]
best_div = []
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

		best_div.append(min(div[index], div[index+1]))

		# Ordenamaneto dos jogos por divisao
		orgdiv.append(int(div[index]+div[index+1]))

		#critehrio do derbie (considerarah confreonto top 6 como derbie, mas isso não vai fazer diferença nenhuma pra nos)
		if "P2" in x[index//2]:
			orgdiv[index//2] = 1


tempoo = []
index2=0

temp0_sorted_tuple, jogos_sorted, best_div_sorted_tuple = zip(*sorted(zip(orgdiv, x, best_div)))
x_sorted = []
best_div_sorted = []
temp0_sorted = []
x_sorted.extend(jogos_sorted)
best_div_sorted.extend(best_div_sorted_tuple)
temp0_sorted.extend(temp0_sorted_tuple)
# print(x_sorted)
# temp0_sorted, x_sorted = zip(*sorted(zip(temp0, x), reverse=True))

while index2<5:
	for index in range(len(x_sorted)-1):
		if temp0_sorted[index] == temp0_sorted[index+1]:
			if best_div_sorted[index] > best_div_sorted[index+1]:
				x_sorted[index], temp0_sorted[index], best_div_sorted[index], x_sorted[index+1], temp0_sorted[index+1], best_div_sorted[index+1] = x_sorted[index+1], temp0_sorted[index+1], best_div_sorted[index+1], x_sorted[index], temp0_sorted[index], best_div_sorted[index]

	index2 = index2 +1


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
# Jogos que nao vao e o replay posterior deve ser desconsiderado:
if "zzz" in x_sorted[0]:
	x_not_sorted= []
	x_not_sorted.extend(x_sorted[10:])
	with open("replays.yaml", "w", encoding="utf-8") as f:
		yaml.dump(x_not_sorted, f)

else:
	with open('replays.yaml', 'r') as f:
		data3 = yaml.load(f, Loader=yaml.FullLoader)
		# print(data3)
	index = 0
	while index<=5:
		for o in x_sorted:
			for o2 in range(len(data3)):
				if o.split(" x ")[0] in data3[o2] and o.split(" x ")[1].split(" - ")[0] in data3[o2]:
					x_sorted.remove(o)
		index = index + 1

for index, z in enumerate(x_sorted):
	print(z)
	if index==9:
		break
conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)