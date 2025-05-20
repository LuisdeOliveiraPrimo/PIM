import json
import os
import re
from datetime import datetime
import statistics
from collections import Counter

# Arquivo JSON
arquivo_json = "usuarios.json"

# Lista de Cursos Disponíveis
cursos = ['JAVA', 'PYTHON', 'CSS', 'HTML', 'C', 'SQL']

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
print(f"Cursos disponíveis: {', '.join(cursos)}")
while True:
    curso = input("Qual curso você deseja se inscrever? ").strip().upper()
    if curso in cursos:
        break
    print("Curso não disponível. Tente novamente.")

# Data de cadastro e tempo de uso
data_cadastro = datetime.today()
tempo_de_uso_dias = 0

# Estrutura final dos dados
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

# Verificar se o arquivo existe e carregar os dados
if os.path.exists(arquivo_json):
    with open(arquivo_json, "r", encoding="utf-8") as arquivo:
        try:
            lista_usuarios = json.load(arquivo)
        except json.JSONDecodeError:
            lista_usuarios = []
else:
    lista_usuarios = []

# Adicionar novo usuário
lista_usuarios.append(dados_usuario)

# Salvar no arquivo
with open(arquivo_json, "w", encoding="utf-8") as arquivo:
    json.dump(lista_usuarios, arquivo, indent=4, ensure_ascii=False)
