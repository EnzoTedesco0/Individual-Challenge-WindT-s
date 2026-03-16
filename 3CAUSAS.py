import pandas as pd 

anos = [
    ("2019", "2019-01-01_-_2020-01-01"),
    ("2020", "2020-01-01_-_2021-01-01"),
    ("2021", "2021-01-01_-_2022-01-01")
]
#função que calcula as principais causas de parada, recebendo o numero da turbina como parâmetro
def principais_paradas(turbina):
#array para armazenar os dados de todos os anos antes de juntar
    todos_dados = []

    for ano, periodo in anos:

        id_arquivo = 227 + turbina

        arquivo = f"Status_Kelmarsh_{turbina}_{periodo}_{id_arquivo}.csv"

        status = pd.read_csv(arquivo, comment="#")

        status["Timestamp start"] = pd.to_datetime(status["Timestamp start"])
        status = status.sort_values("Timestamp start")

        status["delta"] = status["Timestamp start"].shift(-1) - status["Timestamp start"]
#armazena os de parada de cada ano em um array, para depois juntar todos os dados e calcular as principais causas de parada considerando o período total de análise
        todos_dados.append(status)
#concatena os dados de todos os anos em um único DataFrame para facilitar a análise das causas de parada
    dados = pd.concat(todos_dados)

    dados["delta"] = dados["delta"].fillna(pd.Timedelta(0))
#armazena todos os dados de quando o status era diferente de funcionando
    paradas = dados[dados["IEC category"] != "Full Performance"]
#aqui, vai somar todos os tempos de parada para cada categoria de parada, agrupando os dados por categoria e somando os valores da coluna "delta" para cada grupo
    soma_paradas = paradas.groupby("IEC category")["delta"].sum()
#soma o total de tempo parado para calcular a taxa por tipo de parada
    total_parado = soma_paradas.sum()
    total_parado_horas = total_parado.total_seconds() / 3600
#ordena as classificações de parada, para que o proximo comando pegue os 3 com maior valor de tempo
    soma_paradas = soma_paradas.sort_values(ascending=False)
#este comando seleciona as 3 principais causas de parada com base no tempo de parada relacionado a acada uma
    top3 = soma_paradas.head(3)

    print(f"\nTURBINA {turbina}")
    print("Principais causas de parada:")
#repetição que percorre as 3 principais causas de parada e mostra quanto tempo está relacionado a cada uma
    for causa, tempo in top3.items():

        horas = tempo.total_seconds() / 3600

        print(causa, "-", round(horas,2), "horas")
        print("taxa de parada:", round((horas / total_parado_horas) * 100, 2), "%")


for turbina in range(1,7):

    principais_paradas(turbina)