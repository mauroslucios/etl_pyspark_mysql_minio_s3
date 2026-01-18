# generate_fk_data.py
import random
from faker import Faker

fake = Faker('pt_BR')
random.seed(42)  # Reprodutível

# Dados RJ
cidades_rj = ['Rio de Janeiro', 'Niterói', 'Petrópolis', 'Volta Redonda', 'Campos dos Goytacazes']
racas = ['Branca', 'Parda', 'Preta', 'Amarela', 'Indígena']
especialidades = ['Clínico Geral', 'Cardiologia', 'Pediatria', 'Ginecologia', 'Ortopedia']

print("-- 1. ESTADO RJ")
print("INSERT INTO estado (nome, sigla) VALUES ('Rio de Janeiro', 'RJ');\n")

print("-- 2. 5 CIDADES RJ")
for i, cidade in enumerate(cidades_rj, 1):
    print(f"INSERT INTO cidade (nome, id_estado) VALUES ('{cidade}', 1);")
print("\n")

print("-- 3. 100 ENDEREÇOS")
enderecos = []
for i in range(100):
    rua = fake.street_name()
    numero = random.randint(1, 999)
    cep = fake.postcode()
    id_cidade = random.randint(1, 5)
    enderecos.append(i+1)  # Guarda IDs
    print(f"INSERT INTO endereco (rua, numero, cep, id_cidade) VALUES ('{rua}', '{numero}', '{cep}', {id_cidade});")
print("\n")

print("-- 4. 300 PACIENTES (FK endereco 1-100)")
for i in range(300):
    nome = fake.name()
    cpf = fake.cpf().replace('.', '').replace('-', '')
    raca = random.choice(racas)
    id_endereco = random.choice(enderecos)  # ✅ FK VÁLIDO!
    print(f"INSERT INTO paciente (nome, cpf, raca, id_endereco) VALUES ('{nome}', '{cpf}', '{raca}', {id_endereco});")
print("\n")

print("-- 5. 200 MÉDICOS (FK cidade 1-5)")
for i in range(200):
    nome = f"D{random.choice(['r.', 'ra.'])} {fake.name()}"
    crm = f"CRM-RJ-{random.randint(10000, 99999):05d}"
    especialidade = random.choice(especialidades)
    id_cidade = random.randint(1, 5)  # ✅ FK VÁLIDO!
    print(f"INSERT INTO medico (nome, crm, especialidade, id_cidade) VALUES ('{nome}', '{crm}', '{especialidade}', {id_cidade});")
