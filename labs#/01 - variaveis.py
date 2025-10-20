custo = 600
faturamento = 1100

print("Faturamento", faturamento)
novas_vendas = 1000

faturamento = faturamento + novas_vendas
imposto = 0.15 * faturamento  #é um float
print(imposto)
lucro = faturamento - custo - imposto

print("Faturamento", faturamento)
print("Custo", custo)
print("Lucro", faturamento - custo)

""" int = numeros inteiros
float = numeros com casas decimais
strings = textos
booleans = booleanos (True False)  
"""

mensagem = "O faturamento da loja foi de 2100 reais"  #string
teve_lucro = False  #boolean

margem_lucro = lucro / faturamento  #float
print("Margem", margem_lucro)

""" operadores especiais
mod -/> %
resto da divisão de um número pelo outro
floor division divisao inteira -/> //
"""