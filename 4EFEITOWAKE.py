import pandas as pd
#importa a biblioteca numpypara fazer operações matemáticas otimizadas
import numpy as np
#importa a biblioteca matplotlib para fazer gráficos das informações obtidas
import matplotlib.pyplot as plt


anos = [
    ("2019", "2019-01-01_-_2020-01-01"),
    ("2020", "2020-01-01_-_2021-01-01"),
    ("2021", "2021-01-01_-_2022-01-01")
]


#define qual é a direção que o vento tem que vir, em relação a N sentido horário, para que a turbina 2 esteja na direção do vento em relação a turbina 3, ou seja, para que a turbina 3 esteja no "wake" da turbina 2
WAKE_DIRECTION = 255
#define uma margem de 30 graus para mais ou para menos para considerar os valores também
MARGIN = 30


#variáveis que vão armazenar os dados de cada turbina para cada ano, para depois concatenar tudo e fazer a análise considerando o período total
todos_t2 = []
todos_t3 = []

for ano, periodo in anos:

    arquivo_t2 = f"Turbine_Data_Kelmarsh_2_{periodo}_229.csv"
    arquivo_t3 = f"Turbine_Data_Kelmarsh_3_{periodo}_230.csv"
#aqui vem um detalhe importante deste código. O nome de cada coluna, no código, começa com um símbolo de comentário, entao o pd pularia essa coluna. O que foi necessário fazer é com que ele pulasse automaticamente as 9 primeiras colunas que tem esse símbolo e depois substituir esse simbolo na décima linha para um espaço vazio. Assim, a linha pode ser lida normalmente e as colunas ficam com os nomes corretos para serem usadas depois
    t2 = pd.read_csv(arquivo_t2, skiprows=9)
    t3 = pd.read_csv(arquivo_t3, skiprows=9)
#aqui faz parte do procedimento anterior
    t2.columns = t2.columns.str.replace("#", "").str.strip()
    t3.columns = t3.columns.str.replace("#", "").str.strip()
#ceia uma variável para identificar qual é a coluna que contém os timestamps
    time_col = [c for c in t2.columns if "Date" in c][0]

    t2[time_col] = pd.to_datetime(t2[time_col])
    t3[time_col] = pd.to_datetime(t3[time_col])
   #adiciona os dados de cada ano em um array para depois concatenar
    todos_t2.append(t2)
    todos_t3.append(t3)

#concatena todos os dados de cada ano em um único DataFrame para cada turbina, para depois fazer a análise considerando o período total
t2 = pd.concat(todos_t2)
t3 = pd.concat(todos_t3)

#combina duas tabelas utilizando a coluna de timestamp como chave, para que cada linha do DataFrame resultante tenha os dados de ambas as turbinas para o mesmo timestamp
df = pd.merge(t2, t3, on=time_col, suffixes=("_T2", "_T3"))

#filtro para identificar a direção do vento para poder calcular se há wake
df = df[
    (df["Wind direction (°)_T2"] >= WAKE_DIRECTION - MARGIN) &
    (df["Wind direction (°)_T2"] <= WAKE_DIRECTION + MARGIN)
]


#função que lê no dataset se as turbinas estão disponíveis para geração, já que temos que desconsiderar quadno não estão 
availability = (
    (df["Available Capacity for Production (kW)_T2"] > 0) &
    (df["Available Capacity for Production (kW)_T3"] > 0)
)
#aplica o filtro para descobrir quando estavam ambas disponíveis
df = df[availability]


#checa os pitchs das turbinas, para garantir que estavam disponíveis para geração naquele momento
pitch_ok = (
    (df["Blade angle (pitch position) A (°)_T2"] <= 5) &
    (df["Blade angle (pitch position) B (°)_T2"] <= 5) &
    (df["Blade angle (pitch position) C (°)_T2"] <= 5) &
    (df["Blade angle (pitch position) A (°)_T3"] <= 5) &
    (df["Blade angle (pitch position) B (°)_T3"] <= 5) &
    (df["Blade angle (pitch position) C (°)_T3"] <= 5)
)
#aplica o filtro de angulação de pitch
df = df[pitch_ok]

#cria intervalos de velocidade do vento para calcular a média de potência gerada em cada intervalo, para depois plotar a curva de potência de cada turbina e comparar o efeito wake
bins = np.arange(0, 25, 1)
#separa os dados para cada intervalo
df["bin"] = pd.cut(df["Wind speed (m/s)_T2"], bins)
#calcula a potência média para cada intervalo de velocidade para cada turbina, quando t3 em wake de t2
curve_T2 = df.groupby("bin")["Power (kW)_T2"].mean()
curve_T3 = df.groupby("bin")["Power (kW)_T3"].mean()

bin_centers = (bins[:-1] + bins[1:]) / 2

#cria uma janela de gráfico, que será a output do código
plt.figure(figsize=(10,6))
#cria o gráfico da curva de potencia de t2 e t3 para t3 em wake de t2 e indica o que cada um representa
plt.plot(bin_centers[:len(curve_T2)], curve_T2.values, label="Turbine 2 (upstream)")
plt.plot(bin_centers[:len(curve_T3)], curve_T3.values, label="Turbine 3 (wake)")
#define os eixos do gráfico
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Power (kW)")
plt.title("Wake Effect: Turbine 2 → Turbine 3")
#adiciona linhas de grade para facilitar a leitura
plt.grid(True)
plt.legend()
#renderiza o gráfico na tela
plt.show()