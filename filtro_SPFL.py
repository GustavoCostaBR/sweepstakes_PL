import sys
import sqlite3
import var_dump
conn = sqlite3.connect('championships.db')
cursor = conn.cursor()

# x = sys.argv[1:]
x = ['Inverness CT x St. Johnstone - P2 (SPFL - playoff) - 20/05 - 15:45', 'St. Johnstone x Inverness CT - P2 (SPFL - playoff) - 23/05 - 15:45']
temp = []
temp2 = []
cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols], [Número de jogos]  FROM scottish_premiership_table_championship")
rows = cursor.fetchall()
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
		for row in rows:
			if row[4] > 3:
				if j in row:
					temp2.append(row)
				elif temp[index+1] in row:
					temp2.append(row)
					row[2]
		temp2




conn.close()
# var_dump.var_dump(part1)
# var_dump.var_dump(part3)