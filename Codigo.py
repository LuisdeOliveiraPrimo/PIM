import json
import os
import re
from datetime import datetime
import statistics
from collections import Counter
import webbrowser  # Para abrir links de cursos

# Arquivo JSON
arquivo_json = "usuarios.json"

# Lista de Cursos Disponíveis
cursos_disponiveis = ['JAVA', 'PYTHON', 'CSS', 'HTML', 'C', 'SQL']

# Função de validação para e-mail
def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Função para calcular idade
def calcular_idade(data_nasc_str):
    nascimento = datetime.strptime(data_nasc_str, "%d/%m/%Y")
    hoje = datetime.today()
    return (hoje - nascimento).days // 365

# Coleta de dados do usuário
print("Bem-vindo ao sistema de cadastro de alunos!")
nome = input("Digite seu nome completo: ").strip().title()

# Validação de CPF
while True:
    cpf = input("Digite seu CPF (apenas números): ").strip()
    if cpf.isdigit() and len(cpf) == 11:
        break
    print("CPF inválido. Ele deve conter exatamente 11 dígitos.")

# Sexo
while True:
    sexo = input("Qual seu sexo? [M]asculino / [F]eminino: ").strip().upper()
    if sexo in ['M', 'F']:
        break
    print("Opção inválida. Digite apenas 'M' ou 'F'.")

# Data de nascimento
while True:
    nascimento = input("Digite sua data de nascimento (DD/MM/AAAA): ")
    try:
        idade = calcular_idade(nascimento)
        break
    except ValueError:
        print("Data inválida. Tente novamente no formato DD/MM/AAAA.")

# Estado (UF)
while True:
    estado = input("Digite a sigla do seu estado (ex: SP, RJ, MG): ").strip().upper()
    if len(estado) == 2 and estado.isalpha():
        break
    print("Digite uma sigla válida com duas letras.")

# Cidade
cidade = input("Digite sua cidade: ").strip().title()

# E-mail
while True:
    email = input("Digite seu e-mail: ").strip()
    if validar_email(email):
        break
    print("Formato de e-mail inválido.")

# Telefone
telefone = input("Digite seu telefone com DDD: ").strip()

# Escolaridade
escolaridade = input("Qual sua escolaridade atual? (Ex: Ensino Médio, Superior Incompleto, etc): ").strip().title()

# Experiência prévia
experiencia = input("Você já teve alguma experiência com programação? (Sim/Não): ").strip().title()

# Curso de interesse
print(f"Cursos disponíveis: {', '.join(cursos_disponiveis)}")
while True:
    curso = input("Qual curso você deseja se inscrever? ").strip().upper()
    if curso in cursos_disponiveis:
        break
    print("Curso não disponível. Tente novamente.")

# Data de cadastro e tempo de uso
data_cadastro = datetime.today()
tempo_de_uso_dias = 0

# Dados do usuário
dados_usuario = {
    "nome": nome,
    "cpf": cpf,
    "sexo": sexo,
    "nascimento": nascimento,
    "idade": idade,
    "estado": estado,
    "cidade": cidade,
    "email": email,
    "telefone": telefone,
    "escolaridade": escolaridade,
    "experiencia_programacao": experiencia,
    "curso": curso,
    "data_cadastro": data_cadastro.strftime("%d/%m/%Y"),
    "tempo_de_uso_dias": tempo_de_uso_dias
}

# Carregar usuários anteriores (se houver)
if os.path.exists(arquivo_json):
    with open(arquivo_json, "r", encoding="utf-8") as arquivo:
        try:
            lista_usuarios = json.load(arquivo)
        except json.JSONDecodeError:
            lista_usuarios = []
else:
    lista_usuarios = []

# Atualizar tempo de uso dos usuários
for u in lista_usuarios:
    try:
        data_cad = datetime.strptime(u["data_cadastro"], "%d/%m/%Y")
        u["tempo_de_uso_dias"] = (datetime.today() - data_cad).days
    except:
        u["tempo_de_uso_dias"] = 0

# Adicionar novo usuário
lista_usuarios.append(dados_usuario)

# Salvar no arquivo
with open(arquivo_json, "w", encoding="utf-8") as arquivo:
    json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)

print(f"\nCadastro concluído com sucesso! Obrigado por se registrar, {nome}.")

# === RELATÓRIO ESTATÍSTICO ===
print("\n=== RELATÓRIO DE ESTATÍSTICAS ===")

idades = [u["idade"] for u in lista_usuarios if "idade" in u and isinstance(u["idade"], (int, float))]
print(f"\n1. Estatísticas Gerais:")
print(f"Total de usuários: {len(lista_usuarios)}")
print(f"Idade média: {statistics.mean(idades):.2f}")
print(f"Idade mediana: {statistics.median(idades)}")
try:
    print(f"Idade moda: {statistics.mode(idades)}")
except statistics.StatisticsError:
    print("Idade moda: Não há uma moda única.")

# Curso mais popular
cursos_geral = [u["curso"] for u in lista_usuarios if u["curso"]]
curso_mais_comum = Counter(cursos_geral).most_common(1)
if curso_mais_comum:
    curso_nome, total = curso_mais_comum[0]
    idades_do_curso = [u["idade"] for u in lista_usuarios if u["curso"] == curso_nome]
    media_idade = statistics.mean(idades_do_curso)
    print(f"\n2. Curso mais popular no geral:")
    print(f"O curso mais escolhido é '{curso_nome}' com {total} alunos.")
    print(f"Média de idade dos alunos do curso: {media_idade:.2f}")
else:
    print("Nenhum curso foi escolhido ainda.")

# Curso mais escolhido por estado
print(f"\n3. Curso mais escolhido por estado:")
estados = set(u["estado"] for u in lista_usuarios)
for estado in estados:
    cursos_estado = [u["curso"] for u in lista_usuarios if u["estado"] == estado and u["curso"]]
    if cursos_estado:
        curso_mais = Counter(cursos_estado).most_common(1)[0][0]
        idades_estado = [u["idade"] for u in lista_usuarios if u["estado"] == estado]
        media_idade_estado = statistics.mean(idades_estado)
        print(f"Em {estado}: curso mais escolhido foi '{curso_mais}' e a média de idade é {media_idade_estado:.2f}")
    else:
        print(f"Em {estado}: Nenhum curso escolhido.")

# Cidade com mais inscritos no curso Python
cidades_python = [u["cidade"] for u in lista_usuarios if u["curso"] == "PYTHON"]
if cidades_python:
    cidade_top_python, qtd = Counter(cidades_python).most_common(1)[0]
    print(f"\n4. Cidade com mais alunos no curso Python:")
    print(f"{cidade_top_python} é a cidade com mais inscritos no curso Python ({qtd} aluno(s)).")
else:
    print("\n4. Nenhum aluno inscrito no curso Python.")

# Faixa etária mais comum
try:
    moda_idade = statistics.mode(idades)
    print(f"\n5. Faixa etária mais comum:")
    print(f"A idade mais comum entre os usuários é {moda_idade} ano(s).")
except statistics.StatisticsError:
    print("\n5. Faixa etária mais comum:")
    print("Não há uma idade que se repete o suficiente para definir uma moda.")

# === MENU DE CURSOS COM LINKS ===

cursos_links = {
    "1": ("Curso de Java", "https://youtu.be/3u1fu6f8Hto"),
    "2": ("Curso de Python", "https://youtu.be/S9uPNppGsGo?si=Lw3wAyS7Tr0GZqOV"),
    "3": ("Curso de C++", "https://youtu.be/_bYFu9mBnr4"),
    "4": ("Curso de HTML", "https://youtu.be/epDCjksKMok"),
}

print("\n=== Escolha um curso para acessar o conteúdo ===")
while True:
    print("\nMenu de Cursos:")
    for chave, (nome_curso, _) in cursos_links.items():
        print(f"{chave}. {nome_curso}")

    opcao = input("Opção: ")
    if opcao in cursos_links:
        nome_curso, link = cursos_links[opcao]
        print(f"\nVocê escolheu: {nome_curso}")
        print(f"Acesse o curso aqui: {link}")
        webbrowser.open(link)
        break
    else:
        print("Opção inválida. Tente novamente.")
