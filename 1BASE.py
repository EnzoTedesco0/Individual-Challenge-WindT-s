#inclui a biblioteca pandas para manipulação de dados
import pandas as pd
#armazena o valor de horas em um ano
horas_ano = 365 * 24

#criar uma variável que armazena a função de leitura do arquivo csv, utilizando o pandas, e ignorando as linhas que começam com "#"
status = pd.read_csv("Status_Kelmarsh_1_2019-01-01_-_2020-01-01_228.csv",
                     comment=("#"))
#usado no começo para descobrir os nomes das colunas
print(status.columns)

#converter a coluna "Timestamp start" para o formato de data e hora
status["Timestamp start"] = pd.to_datetime(status["Timestamp start"])
#cria uma coluna "delta" que calcula a diferença entre o próximo timestamp e o timestamp atual, utilizando a função shift
status["delta"] = status["Timestamp start"].shift(-1) - status["Timestamp start"]
#checa quando o status da turbina é de operação e armazena esses dados em uma nova variável chamada "operando", que marca na tabela delta quais sao os valores de tempo em que a turbina estava operando
operando = status[status["IEC category"] == "Full Performance"]
#calcula o tempo total de operação ao somar os valores da coluna "delta" da tabela "operando"
tempo_total = operando["delta"].sum()
#converte o tempo total de operação para horas e arredonda o resultado para 2 casas decimais
tempo_horas = round(tempo_total.total_seconds() / 3600,2)
#calcula a taxa de tempo em operação em um ano 
taxa = round((tempo_horas / horas_ano) * 100, 2)
#fornece o resultado, mostrando ao usuário o tempo de operação da turbina e a taxa anual de operação
print("TURBINA 1 — 2019")
print("Horas em operação:", tempo_horas)
print("Taxa de tempo em operação:", taxa, "%")