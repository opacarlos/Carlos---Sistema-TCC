from flask import Flask, render_template
import folium
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

cities = [
    {'name': 'Fortaleza', 'location': [-3.7364419466541583, -38.524770437782074], 'img': 'Precipitação_Fortaleza.png'},
    {'name': 'Belém', 'location': [-1.4587276649923475, -48.50181712356305], 'img': 'Precipitação_Belém.png'},
    {'name': 'Manaus', 'location': [-3.119385530637084, -60.01931048636225], 'img': 'Precipitação_Manaus.png'},
    {'name': 'João Pessoa', 'location': [-7.118666920739596, -34.87233308724278], 'img': 'Precipitação_João Pessoa.png'}
]

my_map = folium.Map(location=[-3.7172, -38.5433], zoom_start=5)

@app.route('/')
def index():

    for city in cities:

        caminho_arquivo = 'Cidades/'+city['name']+'.xlsx'
        df = pd.read_excel(caminho_arquivo)
        df_t = pd.read_excel(caminho_arquivo, sheet_name='Teste T Precipitação')
        
        #Teste T de Precipitação:
        com_chuva = df_t['Com chuva']
        sem_chuva = df_t['Sem chuva']
        t_statistic, p_value = stats.ttest_ind(com_chuva, sem_chuva)

        #Gráfico de Precipitação:
        x = df['Data']
        y1 = df['Falhas']
        y2 = df['Precipitação']
        plt.figure(figsize=(6.5,3))
        plt.plot(x, y1, label='Falhas', color = 'red')
        plt.plot(x, y2, label='Precipitação')
        plt.legend()
        plt.savefig('static/imagens/Precipitação_'+ city['name'] +'.png', dpi = 600)
        
        popup_content = f"""<img src="static/imagens/Precipitação_{city['name']}.png" width=300px><br><center>Teste T: {p_value}</center>"""
        folium.Marker(location = city['location'],
                  tooltip = city['name'],
                  popup = folium.Popup(popup_content,max_width = 1000)).add_to(my_map)

    map_html = my_map._repr_html_()

    return render_template('index.html', map_html=map_html)

@app.route('/temperatura')
def temperatura():

    for city in cities:
        
        caminho_arquivo = 'Cidades/'+city['name']+'.xlsx'
        df = pd.read_excel(caminho_arquivo)
        df_t = pd.read_excel(caminho_arquivo, sheet_name='Teste T Temperatura')

        #Teste T de Temperatura:
        com_chuva = df_t['Até 30']
        sem_chuva = df_t['Acima de 30']
        t_statistic, p_value = stats.ttest_ind(com_chuva, sem_chuva)
        
        #Gráfico de Temperatura:
        x = df['Data']
        y1 = df['Falhas']
        y2 = df['Temperatura Máxima']
        plt.figure(figsize=(6.5,3))
        plt.plot(x, y1, label='Falhas', color = 'red')
        plt.plot(x, y2, label='Temperatura Máxima')
        plt.legend()
        plt.savefig('static/imagens/Temperatura_'+ city['name'] +'.png', dpi = 600)

        popup_content = f"""<img src="static/imagens/Temperatura_{city['name']}.png" width=300px><br><center>Teste T: {p_value}</center>"""
        folium.Marker(location = city['location'],tooltip = city['name'],
                      popup = folium.Popup(popup_content,max_width = 1000)).add_to(my_map)

    map_html = my_map._repr_html_()

    return render_template('index.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
