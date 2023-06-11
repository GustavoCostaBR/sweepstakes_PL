import yaml

with open('Rivals.yml', 'r') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

with open('Configuracoes.yml', 'r') as f:
	data2 = yaml.load(f, Loader=yaml.FullLoader)

# Assuming you have the YAML data as a string stored in the 'yaml_data' variable

# Parse the YAML data into a Python dictionary
# parsed_data = yaml.safe_load(data)

# Access the 'Rivalidades_Inglaterra' dictionary
# Rivalidades_Inglaterra = parsed_data['Rivalidades_Inglaterra']

Rivalidades_Inglaterra = data['Rivalidades_Inglaterra']
Rivalidades_Escocia = data['Rivalidades_Escocia']
Times_sem_rivais = data['Times_sem_rivais']
Inicio_Rodada = data2['Inicio_Rodada']

Rivalidades= [Rivalidades_Inglaterra, Rivalidades_Escocia, Times_sem_rivais]

# Now you can access the dictionary in the normal way
print(Rivalidades_Inglaterra['Aldershot Town'])  # Output: ['Reading']
print(Rivalidades_Inglaterra['Arsenal'])  # Output: ['Chelsea', 'Manchester United', 'Tottenham Hotspur']
print(Rivalidades)
print(Inicio_Rodada)
