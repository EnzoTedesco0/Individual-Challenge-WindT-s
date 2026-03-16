import pandas as pd

horas_ano = 365 * 24
#array que armazena a tupla de anos e seus respectivos períodos para leitura dos arquivos
anos = [
    ("2019", "2019-01-01_-_2020-01-01"),
    ("2020", "2020-01-01_-_2021-01-01"),
    ("2021", "2021-01-01_-_2022-01-01")
]
#função que será utilizada para calcular o tempo de operação. Recebe como parâmetroso arquivo a ser analisado, o número da turbina e o ano a ser analisado.
def calcular_operacao(arquivo, turbina, ano):

    status = pd.read_csv(arquivo, comment="#")

    status["Timestamp start"] = pd.to_datetime(status["Timestamp start"])
#ordena os dados por data e hora para garantir que a coluna "delta" seja calculada corretamente
    status = status.sort_values("Timestamp start")

    status["delta"] = status["Timestamp start"].shift(-1) - status["Timestamp start"]
#preenche os valores nulos da coluna "delta" com 0, para evitar problemas no cálculo
    status["delta"] = status["delta"].fillna(pd.Timedelta(0))

    operando = status[status["IEC category"] == "Full Performance"]

    tempo_total = operando["delta"].sum()

    tempo_horas = round(tempo_total.total_seconds() / 3600,2)

    taxa = round((tempo_horas / horas_ano) * 100, 2)
#printa, dependendo dos valores que estão sendo analisados, seus respectivos resultados, especificando o período
    print(f"TURBINA {turbina} — {ano}")
    print("Horas em operação:", tempo_horas)
    print("Taxa de tempo em operação:", taxa, "%")
    print("-----------------------------------")

#estrutura simples de repetição que vai mudar os valores com base no elemento de [anos] que está sendo analisado na hora de fornecer o nome dos arquivos, essa foi uma das principais mudanças necessárias para realizar a automação da análise dos dados.
#essa instrução ordena que o processo se repita uma vez para cada tupla em [anos]
for ano, periodo in anos:

    for turbina in range(1, 7):
#como cada turbina tem um número, essa foi uma forma de calcular o número que estará presente no nome do arquivo.
        id_arquivo = 227 + turbina
        #define o nome do próximo arquiivo a ser analisado. Isso automatiza o processo, pois permite que todos os dados necessários sejam analisados ao alterar apenas os elementos dos nomes dos arquivos que os diferenciam.
        arquivo = f"Status_Kelmarsh_{turbina}_{periodo}_{id_arquivo}.csv"
#aqui é onde a função é executada, recebendo todos os parametros que foram definidos anteriormente, bem como o valor a eles atribuído.
        calcular_operacao(arquivo, turbina, ano)