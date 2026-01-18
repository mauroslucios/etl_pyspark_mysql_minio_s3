import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')
random.seed(42)

cidades_rj = [
    'Petrópolis', 'Rio de Janeiro', 'Angra dos Reis', 'Aperibé', 'Araruama', 'Areal',
    'Armação dos Búzios', 'Arraial do Cabo', 'Barra do Piraí', 'Barra Mansa',
    'Belford Roxo', 'Bom Jardim', 'Bom Jesus do Itabapoana', 'Cabo Frio',
    'Cachoeiras de Macacu', 'Cambuci', 'Campos dos Goytacazes', 'Cantagalo',
    'Carapebus', 'Cardoso Moreira', 'Carmo', 'Casimiro de Abreu', 
    'Comendador Levy Gasparian', 'Conceição de Macabu', 'Cordeiro',
    'Duas Barras', 'Duque de Caxias', 'Engenheiro Paulo de Frontin',
    'Guapimirim', 'Iguaba Grande', 'Itaboraí', 'Itaguaí', 'Italva',
    'Itaocara', 'Itaperuna', 'Itatiaia', 'Japeri', 'Laje do Muriaé',
    'Macaé', 'Macuco', 'Magé', 'Mangaratiba', 'Maricá', 'Mendes',
    'Mesquita', 'Miguel Pereira', 'Miracema', 'Natividade', 'Nilópolis',
    'Niterói', 'Nova Friburgo', 'Nova Iguaçu', 'Paracambi', 
    'Paraíba do Sul', 'Paraty', 'Paty do Alferes', 'Pinheiral', 
    'Piraí', 'Porciúncula', 'Porto Real', 'Quatis', 'Queimados',
    'Quissamã', 'Resende', 'Rio Bonito', 'Rio Claro', 'Rio das Flores',
    'Rio das Ostras', 'Santa Maria Madalena', 'Santo Antônio de Pádua',
    'São Fidélis', 'São Francisco de Itabapoana', 'São Gonçalo',
    'São João da Barra', 'São João de Meriti', 'São José de Ubá',
    'São José do Vale do Rio Preto', 'São Pedro da Aldeia',
    'São Sebastião do Alto', 'Sapucaia', 'Saquarema', 'Seropédica',
    'Silva Jardim', 'Sumidouro', 'Tanguá', 'Teresópolis',
    'Trajano de Moraes', 'Três Rios', 'Valença', 'Varre-Sai',
    'Vassouras', 'Volta Redonda'
]

print("-- 1. ESTADO RJ")
print("INSERT INTO estado (nome, sigla) VALUES ('Rio de Janeiro', 'RJ');")
print()

print("-- 2. 92 CIDADES RJ")
for cidade in cidades_rj:
    print(f"INSERT INTO cidade (nome, id_estado) VALUES ('{cidade}', 1);")
print()

# Pré-gerar listas FORA dos f-strings
endereco_ids = list(range(1, 101))
paciente_ids = list(range(1, 101))
medico_ids = list(range(1, 101))
racas = ["Branca", "Parda", "Preta"]
especialidades = ["Clínico Geral", "Cardiologia", "Pediatria"]
dosagens = ["1x_dia", "2x_dia", "3x_dia"]
titulos = ["Dr. ", "Dra. "]

print("-- 3. 100 ENDEREÇOS")
for i in range(1, 101):
    print(f"INSERT INTO endereco (rua, numero, cep, id_cidade) VALUES ('{fake.street_name()}', '{random.randint(1,999)}', '{fake.postcode()}', {random.randint(1,92)});")
print()

print("-- 4. 100 DOENÇAS")
for i in range(1, 101):
    print(f"INSERT INTO doenca (nome, cid) VALUES ('Doença {i}', 'J{i:02d}');")
print()

print("-- 5. 100 PACIENTES")
for i in range(1, 101):
    cpf = fake.cpf().replace('.', '').replace('-', '')
    raca_escolhida = random.choice(racas)
    id_endereco = random.choice(endereco_ids)
    print(f"INSERT INTO paciente (nome, cpf, raca, id_endereco) VALUES ('{fake.name()}', '{cpf}', '{raca_escolhida}', {id_endereco});")
print()

print("-- 6. 100 MÉDICOS")
for i in range(1, 101):
    titulo_escolhido = random.choice(titulos)
    especialidade_escolhida = random.choice(especialidades)
    crm_numero = random.randint(10000,99999)
    id_cidade = random.randint(1,92)
    print(f"INSERT INTO medico (nome, crm, especialidade, id_cidade) VALUES ('{titulo_escolhido}{fake.name()}', 'CRM-RJ-{crm_numero:05d}', '{especialidade_escolhida}', {id_cidade});")
print()

print("-- 7. 100 MEDICAMENTOS")
for i in range(1, 101):
    print(f"INSERT INTO medicamento (nome) VALUES ('Medicamento {i} 500mg');")
print()

print("-- 8. 100 CONSULTAS")
for i in range(100):
    id_paciente = random.choice(paciente_ids)
    id_medico = random.choice(medico_ids)
    id_doenca = random.randint(1, 100)
    data_consulta = fake.date_between(start_date="-1y", end_date="today")
    data_sintoma = data_consulta - timedelta(days=random.randint(1, 30))
    print(f"INSERT INTO consulta (id_paciente, id_medico, id_doenca, data_inicial_sintoma, data_consulta, sintomas) VALUES ({id_paciente}, {id_medico}, {id_doenca}, '{data_sintoma}', '{data_consulta}', '{fake.sentence(nb_words=15)}');")
print()

print("-- 9. 100 RECEITAS")
for i in range(1, 101):
    data_receita = fake.date_between(start_date="-1y", end_date="today")
    print(f"INSERT INTO receita (id_consulta, data_receita) VALUES ({i}, '{data_receita}');")
print()

print("-- 10. 200 RECEITA_MEDICAMENTO")
for i in range(200):
    id_receita = (i//2)+1
    id_medicamento = random.randint(1,100)
    dosagem_escolhida = random.choice(dosagens)
    print(f"INSERT INTO receita_medicamento (id_receita, id_medicamento, dosagem) VALUES ({id_receita}, {id_medicamento}, '{dosagem_escolhida}');")
