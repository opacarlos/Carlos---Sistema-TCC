#Importando bibliotecas
from flask import Flask, render_template
import folium
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

#Armazenando o nome de cidade, localização com latitude e longitude, e imagem gerada do gráfico
cities = [
    {'name': 'Fortaleza', 'location': [-3.7364419466541583, -38.524770437782074], 'img': 'Precipitação_Fortaleza.png'},
    {'name': 'Belém', 'location': [-1.4587276649923475, -48.50181712356305], 'img': 'Precipitação_Belém.png'},
    {'name': 'Manaus', 'location': [-3.119385530637084, -60.01931048636225], 'img': 'Precipitação_Manaus.png'},
    {'name': 'João Pessoa', 'location': [-7.118666920739596, -34.87233308724278], 'img': 'Precipitação_João Pessoa.png'}
]

#Criando o mapa
my_map = folium.Map(location=[-3.7172, -38.5433], zoom_start=5)

#Acessando Index
@app.route('/')
def index():

    #Uma repetição para cada cidade
    for city in cities:
        #Capturando caminho do arquivo a ser lido
        caminho_arquivo = 'cidades/'+city['name']+'.xlsx'
        #Lendo o arquivo com Pandas
        df = pd.read_excel(caminho_arquivo)
        #Lendo o arquivo para Teste T da precipitação com Pandas
        df_t = pd.read_excel(caminho_arquivo, sheet_name='Teste T Precipitação')
        
        #Selecionando colunas
        com_chuva = df_t['Com chuva']
        sem_chuva = df_t['Sem chuva']
        #Calculando Teste T de Precipitação com Scipy
        t_statistic, p_value = stats.ttest_ind(com_chuva, sem_chuva)

        #Gráfico de Precipitação:

        #Selecionando eixos
        x = df['Data']
        y1 = df['Falhas']
        y2 = df['Precipitação']

        #Criando gráfico com Matplotlib
        plt.figure(figsize=(6.5,3))
        plt.plot(x, y1, label='Falhas', color = 'red')
        plt.plot(x, y2, label='Precipitação')
        plt.legend()

        #Salvando imagem do gráfico gerada
        plt.savefig('static/imagens/Precipitação_'+ city['name'] +'.png', dpi = 600)

        #Criando conteúdo a ser mostrado no popup
        popup_content = f"""<img src="static/imagens/Precipitação_{city['name']}.png" width=300px><br><center>Teste T: {p_value}</center>"""

        #Marcando as cidades no mapa
        folium.Marker(location = city['location'],
                  tooltip = city['name'],
                  popup = folium.Popup(popup_content,max_width = 1000)).add_to(my_map)

    #Para renderizar o mapa
    map_html = my_map._repr_html_()
    
    #Renderizando o mapa do index.html
    return render_template('index.html', map_html=map_html)

@app.route('/temperatura')
def temperatura():

    #Uma repetição para cada cidade
    for city in cities:
        #Capturando caminho do arquivo a ser lido
        caminho_arquivo = 'Cidades/'+city['name']+'.xlsx'
        #Lendo o arquivo com Pandas
        df = pd.read_excel(caminho_arquivo)
        #Lendo o arquivo para Teste T da precipitação com Pandas
        df_t = pd.read_excel(caminho_arquivo, sheet_name='Teste T Temperatura')

        #Selecionando colunas
        com_chuva = df_t['Até 30']
        sem_chuva = df_t['Acima de 30']
        #Calculando Teste T de Precipitação com Scipy
        t_statistic, p_value = stats.ttest_ind(com_chuva, sem_chuva)
        
        #Gráfico de Temperatura:

        #Selecionando eixos
        x = df['Data']
        y1 = df['Falhas']
        y2 = df['Temperatura Máxima']

        #Criando gráfico com Matplotlib
        plt.figure(figsize=(6.5,3))
        plt.plot(x, y1, label='Falhas', color = 'red')
        plt.plot(x, y2, label='Temperatura Máxima')
        plt.legend()
        #Salvando imagem do gráfico gerada
        plt.savefig('static/imagens/Temperatura_'+ city['name'] +'.png', dpi = 600)
        
        #Criando conteúdo a ser mostrado no popup
        popup_content = f"""<img src="static/imagens/Temperatura_{city['name']}.png" width=300px><br><center>Teste T: {p_value}</center>"""
        #Marcando as cidades no mapa
        folium.Marker(location = city['location'],tooltip = city['name'],
                      popup = folium.Popup(popup_content,max_width = 1000)).add_to(my_map)
    #Para renderizar o mapa
    map_html = my_map._repr_html_()

    #Renderizando o mapa do index.html
    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
