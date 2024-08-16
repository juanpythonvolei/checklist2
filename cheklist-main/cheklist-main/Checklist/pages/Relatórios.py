import streamlit as st
from streamlit_option_menu import option_menu
import requests
import time
import google.generativeai as genai
import pandas as pd
from Adicionar_Imagens import exibir_imagem


opcoes = ['Dados Gerais', 'Assitência', 'Ver Checklists']
GOOGLE_API_KEY = 'AIzaSyB2uaEtcP8T2_Fy6bhmXC3828qysZEqjNQ'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])

css_style = """
.my-square {
    background-color:#ff0000;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
}
"""


st.markdown(f"<style>{css_style}</style>", unsafe_allow_html=True)
lista_item_repetido = []
lista_normais = []
lista = []
lista_problema = []
image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')


seletor2 = option_menu(
    menu_title="Selecione uma Opção",
    options=opcoes,
    menu_icon='menu-button-wide-fill',icons=['bar-chart-fill','alexa','card-checklist']# Sem parênteses
)



try:
    lista_nomes = []
    
    
    requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
    roteiro = requiscao.json()
    dados = roteiro['Checklists']
    if seletor2 == 'Dados Gerais':    
                              time.sleep(0.5)
                              msg1 = st.toast('Seja Bem vindo (a)')
                              time.sleep(1)  
                              msg2 = st.toast('Nessa aba, você pode Vizualiar dados Gerais acerca do checklist.')  
                              for item in dados:          
                                                          lista.append(item)          
                                                          Checklist = dados[f'{item}']
                                                          for elemento in Checklist:
                                                                   espec = Checklist[f'{elemento}']
                                                                   Data = espec['Data']
                                                                   lista_ok  = espec['ok']
                                                                   for item in lista_ok:
                                                                        if item  != '...':
                                                                          lista_normais.append(item)
                                                                   lista_anormal = espec['Anormais'] 
                                                                   for item in lista_anormal:
                                                                        if item  != '...':
                                                                          lista_problema.append(item) 
                           
                             
                              
                              percentual = float((len(lista_normais)/(len(lista_normais)+len(lista_problema)))*100)
                              Total_positivas = len(lista_normais)
                              Total_negativas = len(lista_problema)
                              Total = len(lista)
                              
                              
                              
                              metrica4 = st.metric(label="Checklists Encontrados", value=Total)          
                              st.divider()          
                              metrica1 = st.metric(label="Total de Observações Positivas", value=Total_positivas)
                              st.divider()          
                              metrica2 = st.metric(label="Total Observações Negativas", value=Total_negativas)   
                              tab1, tab2 = st.tabs(["Percentual de Normalidade", "Gráfico de Normalidade"])            
                              with tab1:          
                                          metrica3 = st.metric(label="Normalidade Geral", value=f'{percentual:.2f} %')          
                              with tab2:         
                                          local = st.container(height=400)         
                                          variaveis = pd.DataFrame({'Condição':['Normal','Anormal'],'Total de Verificações':[Total_positivas,Total_negativas]})                      
                                          with local:          
                                                      st.bar_chart(variaveis.set_index('Condição'))
                                          
    
    
    elif seletor2 == 'Assitência':  
                  time.sleep(0.5)  
                  msg1 = st.toast('Olá. Sou seu assistente personalizado')    
                  time.sleep(1)
                  msg2=st.toast('Aqui, você pode obter informções personalizadas acerca dos checklist de sua equipe e suas informações')    
                  lista_item_repetido =[]
                  lista_normais = []
                  lista = []
                  lista_problema = []
                  texto_problemas = ''
                  requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                  roteiro = requiscao.json() 
                  dados = roteiro['Checklists']          
                  for item in dados:          
                                                            lista.append(item)          
                                                            Checklist = dados[f'{item}']
                                                            for elemento in Checklist:
                                                                     espec = Checklist[f'{elemento}']
                                                                     Data = espec['Data']
                                                                     lista_ok  = espec['ok']
                                                                     usuario = espec['Usuário']    
                                                                                   
                                                                     for item in lista_ok:
                                                                          if item  != '...':
                                                                            lista_normais.append(item)
                                                                     lista_anormal = espec['Anormais'] 
                                                                     for item in lista_anormal:
                                                                          if item  != '...':
                                                                            lista_problema.append(item) 
                                                            texto_problemas += f'usuario:{usuario},itens ok:{lista_normais},itens_anormais:{lista_problema},Data:{Data}'                          
                  for item in lista_problema:                                                            
                                texto_problemas += item
                  
                  comando = st.text_input(label = '',placeholder='Pergunte-me algo',autocomplete = 'on')          
                  if comando:  
                              response = chat.send_message(f'Você receberá a seguir um ou varios relatórios de inspeção de uma empilhadeira. Por favor responda o que for possível conforme o solicitado. Segue a pergunta:{comando}\n\n{texto_problemas}\n')
                              resposta = response.text
                              st.info(f'{resposta}')                                                                                                                                     
                                                    
                                                     
                                                             
                  
                             
    elif seletor2 == 'Ver Checklists':
                              time.sleep(0.5)      
                              msg1 = st.toast('Seja Bem vindo(a). Nessa aba, você pode inspecionar checklists  e vizualizar suas imagens')                  
                              st.divider()          
                              lista = []          
                              requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                              roteiro = requiscao.json()
                              dados = roteiro['Checklists']
                              seletor  = option_menu("Usuários", ["Juan Zonho", "Jonatan Lima","Cesar Fusel","Luiz Felipe"],menu_icon='people')
                              for item in dados:   
                                                            Checklist = dados[f'{item}']
                                                            for elemento in Checklist:
                                                                   espec = Checklist[f'{elemento}']
                                                                   usuario = espec['Usuário']      
                                                                   if usuario == seletor:
                                                                            lista.append(item)   
                              data = st.selectbox("Selecione uma data",lista,index=None,placeholder='Selecione uma data e horário')
                              if data:     
                                            
                                          lista_item_repetido =[]
                                          lista_normais = []
                                          lista_imagens = []
                                          lista_problema = []
                                          texto_problemas = ''
                                          outra_lista = []
                                          
                                          requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                                          roteiro = requiscao.json()
                                          dados = roteiro['Checklists']
                                          for item in dados:          
                                                                          lista.append(item)          
                                                                          Checklist = dados[f'{item}']
                                                                          for elemento in Checklist:
                                                                                   espec = Checklist[f'{elemento}']
                                                                                   usuario = espec['Usuário'] 
                                                                                   Data = espec['Data'] 
                                                                                   if usuario == seletor and Data == data: 
                                                                                     
                                                                                       lista_ok  = espec['ok']
                                                                                       for item in lista_ok:
                                                                                              lista_normais.append(item)
                                                                                       lista_anormal = espec['Anormais'] 
                                                                                       for item in lista_anormal:
                                                                                              lista_problema.append(item) 
                                                                                                 
                                                                                       lista1 = espec['Imagens']
                                                                                       for item in lista1:         
                                                                                                    if item != '...':           
                                                                                                                lista_imagens.append(item)
                                                                                       
                                                  
                                          dict = {'Itens ok':lista_normais,'Itens Anormais':lista_problema}
                                          tabela = pd.DataFrame(dict)
                                          st.table(tabela) 
                                          caracter = './captured_image_'
                                          caracter2 = '.jpg'
                                          caracter3 = '_'          
                                          if len(lista_imagens) > 0:
                                                      
                                                      botao = st.button('Ver Imagens do Checklist')
                                                      if botao:
                                                                  
                                                                  for item in lista_imagens:
                                                                              try:
                                                                                          nome = item.replace(caracter,'')
                                                                                          nome = nome.replace(caracter2,'')
                                                                                          if caracter3 in nome:
                                                                                                      nome = nome.replace(caracter3,' ')
                                                                                                      exibir_imagem(item,nome)
                                                                                          else:
                                                                                                 exibir_imagem(item,nome)     
                                                                                                    
                                                                                          
                                                                              except:
                                                                                          pass
except:
    st.error('Não foi possível carregar checklists')
    
