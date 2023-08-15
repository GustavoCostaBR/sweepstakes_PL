x = ['Liverpool x Brentford - P1 (PL) - 06/05 - 13:30']


sorted_Jogos = sorted(x, key=lambda s: tuple(s.split(' - ')[-2:]))

print(sorted_Jogos)