import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import ssl
import pdb
import yaml
import subprocess

def main_TABELA_CAMPEONATOS(a0):
	# Ignore SSL certificate errors
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	# connect to the database
	conn = sqlite3.connect('championships.db')

	# create a cursor object
	cursor = conn.cursor()

	with open('tabelas.yml', 'r') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)

	links = data['Links']
	table_names = data['Table_Names']
	replaces = []
	replaces.extend([data['RODADA_PL'], data['RODADA_SPFL'], data['RODADA_LCH'], data['RODADA_SPFL_CHAMPIONSHIP'], data['RODADA_SPFL_RELEGATION'], data['RODADA_LEAGUE_ONE'], data['RODADA_LEAGUE_TWO'], data['RODADA_NATIONAL_LEAGUE']])


	for index2,table in enumerate(table_names):
		# create the table with an auto-generated position column
		cursor.execute(f'''DROP TABLE IF EXISTS {table}''')
		cursor.execute(f'''CREATE TABLE {table}
						(position INTEGER PRIMARY KEY,
						[Nome do time] TEXT UNIQUE,
						[Número de jogos] INTEGER,
						vitórias INTEGER,
						empates INTEGER,
						derrotas INTEGER,
						[gols pró] INTEGER,
						[gols contra] INTEGER,
						[saldo de gols] INTEGER,
						pontos INTEGER)''')

		headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'}
		if (replaces[index2]-1) == 0:
			if "z99" in links[index2]:
				url = links[index2].replace("z99", str(replaces[index2]))
			else:
				url = links[index2]
		else:
			if "z99" in links[index2]:
				url = links[index2].replace("z99", str(replaces[index2]-1))
			else:
				url = links[index2]
		req = urllib.request.Request(url, headers=headers)
		html1 = urllib.request.urlopen(req, context=ctx).read()
		zz=0
		f=0
		soup = BeautifulSoup(html1, 'lxml')
		body = soup.findAll('table')
		infos_tab = {}
		contador1 = 0
		for tags in body:
			# try:
			# print(tags)
			# pdb.set_trace()

			# pdb.set_trace()
			t2 = tags.find_all('tr')
			for index, it in enumerate(t2):
				it2 = it.find_all('td')
				if index < len(t2) and t2[index] is not None and t2[index].find_next_sibling() is not None:
					p2=t2[index].find_next_sibling()
					p3=p2.find('td')
					# print(p3)

				zz = 0
				try:
					if int(it2[0].text) < 100 and int(it2[0].text) > 0:
						f=1
				except:
					try:
						if infos_tab:
							p2=t2[index].find_previous_sibling()
						else:
							p2=t2[index].find_next_sibling()
						p3=p2.find('td')
						if int(p3.text) < 100 and int(p3.text) > 0 :
							# print("aboboras")
							f=1
						else:
							# print('a' + it2[0].text + 'a')
							f=0
					except:
						try:
							while zz == 0:
								p2=p2.find_previous_sibling() #era next mudei para previous
								p3=p2.find('td')
								try:
									if int(p3.text) < 100 and int(p3.text) > 0 :
										# print("aboboras")
										f=1
									else:
										# print('a' + it2[0].text + 'a')
										f=0
									zz = 1
									# print(p3)
									# pdb.set_trace()
								except:
									continue
						except:
							continue
				for contador in range(len(it2)):
					# pdb.set_trace()
					if f == 1:
						try:
							times = it2[contador].find('a').text
							if times is not None:
								if "AFC " in times:
									times2 = times.replace("AFC ", "")
								elif " AFC" in times:
									times2 = times.replace(" AFC", "")
								elif "FC " in times:
									times2 = times.replace("FC ", "")
								elif " FC" in times:
									times2 = times.replace(" FC", "")
								else:
									times2 = times
							infos_tab[(contador1)] = []
							infos_tab[(contador1)].append(times2)
						except:
							try:
								if ":" in it2[contador].text:
									parts = it2[contador].text.split(":")
									infos_tab[(contador1)].append(parts[0])
									infos_tab[(contador1)].append(parts[1])
								else:
									infos_tab[(contador1)].append(it2[contador].text)
							except:
								continue
				contador1 = contador1 + 1

		for row in range(len(infos_tab)):
			cursor.execute(f"INSERT INTO {table} ([Nome do time], [Número de jogos], vitórias, empates, derrotas, [gols pró], [gols contra], [saldo de gols], pontos) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", infos_tab[(row+1)])
			conn.commit()


		# # # select the data from the table with an ordered position column
		cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols] FROM {table}")

		#print the results
		if a0 == 1:
			rows = cursor.fetchall()
			for row in rows:
				print(row)

		# # commit the changes and close the connection
		conn.commit()
	conn.commit
	conn.close()