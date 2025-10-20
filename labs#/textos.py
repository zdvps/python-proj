faturamento = 1000
custo = 600

lucro = faturamento - custo

# concatenação mais dificil texto = "o lucro foi de" + str(lucro) + "e o faturamento foi de" + str(faturamento)"
# concatenção mais facil com f-strings
texto =  f"o lucro foi de {lucro} e o faturamento foi de {faturamento} "
print(texto)

email = "zn-dv@outlook.com"

email = email.lower() # colocar em letra minuscula
email = email.strip() # remover espaços vazios no começo e no final
print(email)

# tamanho
tamanho = len(email)
print(tamanho)

# posição
posição = email.find("@")
print(posição)

# pedaços do texto
servidor = email[posição:]
print(servidor)   # vai do @ até o final

# email completo

# trocar um pedaço do texto
novo_email = email.replace("outlook","gmail")
print(novo_email)

nome = "zenio almeida"
nome = nome.capitalize() # primeira letra maiuscula
print(nome)
nome = nome.title() # primeira letra de cada palavra maiuscula
print(nome)

# faturação númerica
faturamento = 1_000_000
custo = 600

lucro = faturamento - custo
margem = lucro / faturamento
texto =  f"o lucro foi de {lucro:,.2f} e o faturamento foi de {faturamento:,.2f} e a margem foi de {margem:.0%} "
print(texto)

# exercício
nome = "zenio almeida"
email = "zn-dv@outlook.com"

# descubra o servidor do email
posição = email.find("@")
servidor = email[posição:]
print(servidor)
# descubra o 1o nome do usuário
posição_espaco = nome.find(" ")
primeiro_nome = nome[:posição_espaco]
primeiro_nome = primeiro_nome.capitalize()
print(primeiro_nome)
# criar uma mensagem personalizada dizendo "Usuário tal foi cadastrado com sucesso no email tal"
mensagem = f"Usuário {primeiro_nome} foi cadastrado com sucesso no email {email}"
print(mensagem)
