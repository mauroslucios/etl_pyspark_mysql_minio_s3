# generate_400_inserts_rj.py
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker('pt_BR')
random.seed(42)

# Listas de referência
cidades_rj = ['Angra dos Reis', 'Aperibé', 'Araruama', 'Areal', 'Armação dos Búzios', 'Arraial do Cabo', 
              'Barra do Piraí', 'Barra Mansa', 'Belford Roxo', 'Bom Jardim'][:92]  # 92 cidades

racas = ['Branca', 'Parda', 'Preta', 'Amarela', 'Indígena']
especialidades = ['Clínico Geral', 'Cardiologia', 'Pediatria', 'Ginecologia', 'Ortopedia', 
                  'Neurologia', 'Dermatologia', 'Psiquiatria', 'Oftalmologia', 'Otorrino']

doencas = ['Hipertensão', 'Diabetes', 'Gripe', 'Dengue', 'COVID-19', 'Asma', 'Gastrite', 
           'Alergia', 'Rinite', 'Sinusite', 'Bronquite', 'Otite', 'Conjuntivite']

medicamentos = ['Paracetamol', 'Ibuprofeno', 'Amoxicilina', 'Losartana', 'Metformina', 
                'Omeprazol', 'Prednisona', 'Cetirizina', 'Salbutamol', 'Enalapril']

print("-- 1. 100 DOENÇAS")
for i, doenca in enumerate(doencas * 10, 1):  # Repete para 100
    cid = f"{random.choice(['A', 'B', 'J', 'E', 'K'])}0{i:02d}"
    print(f"INSERT INTO doenca (nome, cid) VALUES ('{doenca}', '{cid}');")
print("\n")

print("-- 2. 100 ENDEREÇOS (todas 92 cidades RJ)")
endereco_ids = []
for i in range(100):
    rua = fake.street_name()
    numero = str(random.randint(1, 999))
    cep = fake.postcode()
    cidade_id = random.randint(1, 92)  # Todas cidades RJ
    endereco_ids.append(i+1)
    print(f"INSERT INTO endereco (rua, numero, cep, id_cidade) VALUES ('{rua}', '{numero}', '{cep}', {cidade_id});")
print("\n")

print("-- 3. 100 PACIENTES")
paciente_ids = []
for i in range(100):
    nome = fake.name()
    cpf = fake.cpf().replace('.', '').replace('-', '')
    raca = random.choice(racas)
    id_endereco = random.choice(endereco_ids)
    paciente_ids.append(i+1)
    print(f"INSERT INTO paciente (nome, cpf, raca, id_endereco) VALUES ('{nome}', '{cpf}', '{raca}', {id_endereco});")
print("\n")

print("-- 4. 100 MÉDICOS (todas cidades RJ)")
medico_ids = []
for i in range(100):
    nome = f"D{random.choice(['r.', 'ra.'])} {fake.name()}"
    crm = f"CRM-RJ-{random.randint(10000, 99999):05d}"
    especialidade = random.choice(especialidades)
    id_cidade = random.randint(1, 92)  # Todas cidades RJ
    medico_ids.append(i+1)
    print(f"INSERT INTO medico (nome, crm, especialidade, id_cidade) VALUES ('{nome}', '{crm}', '{especialidade}', {id_cidade});")
print("\n")

print("-- 5. 100 CONSULTAS (todas FK válidas)")
for i in range(100):
    id_paciente = random.choice(paciente_ids)
    id_medico = random.choice(medico_ids)
    id_doenca = random.randint(1, 100)
    
    # Datas realistas (sintoma antes da consulta)
    data_consulta = fake.date_between(start_date='-1y', end_date='today')
    data_sintoma = data_consulta - timedelta(days=random.randint(1, 30))
    
    sintomas = fake.text(max_nb_chars=200)
    
    print(f"INSERT INTO consulta (id_paciente, id_medico, id_doenca, data_inicial_sintoma, data_consulta, sintomas) VALUES ({id_paciente}, {id_medico}, {id_doenca}, '{data_sintoma}', '{data_consulta}', '{sintomas}');")
