import streamlit as st
import pandas as pd
from teste import enviar_email,enviar_email2
from fpdf import FPDF
from io import BytesIO
from datetime import datetime
import pytz
from Estatísticas import estatistica
from Adicionar_Imagens import adicionar_imagem
import  webbrowser
import requests
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import credentials, firestore,db
import time

@st.dialog(f"Deseja realmente excluir o Checklist? ")             
def escolha(data):    
                                                            
                                                            sim = st.button('Sim')
                                                            if sim:
            
            
                                                                            # Referência ao nó do usuário que você deseja excluir
                                                                            usuario_ref = db.reference(f'Checklists/{data}')
                                                                            
                                                                            # Exclui o usuário
                                                                            usuario_ref.delete()
                                                                            st.success(f'Conjunto  {data} excluido')
                                                            else:
                                                                st.info(f'Até o momento, o administrador opta por não excluir conjunto {data}')
                                                                
def baixar():
    time.sleep(0.5)
    msg = st.toast(f'Faça o Download do Checklist 📂')
   
lista_usuarios = [('Juan Zonho','1122'),('Jonatan Lima','1212'),('Cesar Fusel','1221'),('Luiz Felipe','2211')]
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
fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
agora_brasilia = datetime.now(fuso_horario_brasilia)
data_hora_formatada = agora_brasilia.strftime("%Y-%m-%d %H:%M:%S")

image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
seletor  = option_menu("Selecione uma opção", ["Novo Checklist", "Excluir Checklist"],icons = ['plus-circle-fill','trash'],menu_icon='menu-button-wide-fill')
if seletor == 'Novo Checklist':
            usuario = st.selectbox('', ['Juan Zonho', 'Jonatan Lima','Cesar Fusel','Luiz Felipe'],index=None,placeholder='Selecione um usuário para continuar')
            minha_variavel = f'{usuario}' 
            
            if usuario:
                        senha = st.text_input(label=f'',placeholder=f'Insira sua senha {usuario}',type='password')
                         
                        for i in lista_usuarios:
                                    login_2,senha_2 = i
                                    if usuario == login_2:
                                                if senha == senha_2:
                                                            st.divider()
                                                            st.success(f'Acesso autorizado. Seja Bem Vindo(a) {usuario}')
                                                            st.session_state.lista_qtd = []
                                                            st.session_state.lista_problemas = []
                                                            st.session_state.lista_imagens = []
                                                            st.session_state.mostrar_reclamacao = False
                                                            st.info('Novo Checklist Iniciado')
                                                           
            
                                                            def criar_pdf_em_memoria(dados):
                                                                lista2 = []        
                                                                df = pd.DataFrame(dados)
                                                                        
                                                                class PDF(FPDF):    
                                                                    def __init__(self):
                                                                        super().__init__()
                                                                        self.w = 210  
                                                                        self.h = 297                                
                                                                    def header(self):
                                                                        self.set_font('Arial', 'B', 12)
                                                                        self.cell(0, 10, f'Relatório de Checklist. Usuário: {usuario}. {data_hora_formatada}', 0, 1, 'C')
                                                            
                                                                    def add_table(self, df):
                                                                        self.set_font('Arial', '', 12)
                                                                        col_width = 95 
                                                                        for i in range(len(df)):
                                                                            for j in range(len(df.columns)):
                                                                                self.cell(col_width, 10, str(df.iloc[i, j]), 1)
                                                                            self.ln()             
                                                        
                                                                    def add_text(self, text, font_size=12):
                                                                               self.set_font('Arial', '', font_size)
                                                                               self.multi_cell(0, 10, text, 0, align='C')  
                                                                    def add_images_in_rows(self, imagens, num_images_per_row, x_start, y_start, width, height, spacing):
                                                                                
                                                                               
                                                                            x = x_start
                                                                            y = y_start
                                                                            for i, item in enumerate(imagens):
                                                                                if item == str('...'):
                                                                                    continue         
                                                                                self.image(item, x, y, width, height)
                                                                                x += width + spacing  
                                                                            
                                                                                if (i + 1) % num_images_per_row == 0:
                                                                                    
                                                                                
                                                                                    x = x_start
                                                                                    y += height + spacing  
                                                                pdf = PDF()
                                                                pdf.add_page()
                                                                pdf.add_table(df)
                                                                pdf.add_page()      
                                                                pdf.add_text('Imagens das observações abaixo')        
                                                                pdf.add_images_in_rows(st.session_state.lista_imagens, num_images_per_row=3, x_start=10, y_start=40, width=30, height=30, spacing=10)
                                                                pdf_buffer = BytesIO()
                                                                pdf_buffer.write(pdf.output(dest='S').encode('latin1'))
                                                                pdf_buffer.seek(0)
                                                                
                                                                return pdf_buffer
                                                            
                                                            
                                                                                                  
                                                                                                                                                     
                                                                                 
                                                            
                                                                    
                                                            # Inicializa as listas no estado da sessão
                                                            if 'lista_qtd' not in st.session_state:
                                                                st.session_state.lista_qtd = []
                                                            if 'lista_problemas' not in st.session_state:
                                                                st.session_state.lista_problemas = []
                                                            if 'senha_admin' not in st.session_state:
                                                                st.session_state.senha_admin = None                        
                                                            def reset_checkboxes():
                                                                for key in st.session_state.keys():
                                                                    if key.startswith('checkbox_'):
                                                                        st.session_state[key] = True
                                                            def preenchimento(normal, anormal, campo):
                                                                if normal or anormal:
                                                                    pass
                                                                else:
                                                                    st.warning(f'Você não Preencheu o campo de {campo}')
                                                            
                                                            
                                                            st.divider()
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            
                                                            with col1:
                                                                            st.write('Vazamento de óleo')
                                                            with col2:
                                                                            anormal_oleo = st.checkbox(label='Anormal', key='2')
                                                                            if anormal_oleo:
                                                                                    with col4:
                                                                                            reclamacao_oleo = st.text_input(label='Digite o Problema', key='texto_oleo')
                                                                                            adicionar_imagem(nome_texto='reclamacao_oleo',nome_link='reclamacao_oleo',lista=st.session_state.lista_imagens)    
                                                                                            if reclamacao_oleo != '':
                                                                                                    if reclamacao_oleo in  st.session_state.lista_problemas:
                                                                                                          pass
                                                                                                    else:            
                                                                                                            st.session_state.lista_problemas.append(reclamacao_oleo)
                                                                                                            st.session_state.lista_qtd.append(str('...'))
                                                                                                            
                                                                                                            st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                            normal_oleo = st.checkbox(label='Normal', key='1')
                                                                            if normal_oleo:
                                                                                    if 'Vazamento de óleo ok' not in st.session_state.lista_qtd:
                                                                                            st.session_state.lista_qtd.append('Vazamento de óleo ok')
                                                                                            st.session_state.lista_problemas.append(str('...'))
                                                                                            st.session_state.lista_imagens.append(str('...'))    
                                                                                    else:
                                                                                           pass
                                                                            else:
                                                                                    if 'Vazamento de óleo ok' in st.session_state.lista_qtd:
                                                                                            st.session_state.lista_qtd.remove('Vazamento de óleo ok')
                                                                                            st.session_state.lista_problemas.append(str('...'))
                                                                                            st.session_state.lista_imagens.append(str('...'))    
                                                            
                                                            preenchimento(normal=normal_oleo, anormal=anormal_oleo, campo='Vazamento de Óleo')
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            
                                                            with col1:
                                                                    st.write('Rodas')
                                                            with col2:
                                                                anormal_Rodas = st.checkbox(label='Anormal', key='2Rodas')
                                                                if anormal_Rodas:
                                                                    with col4:
                                                                        reclamacao_Rodas = st.text_input(label='Digite o Problema', key='texto_Rodas')
                                                                        adicionar_imagem(nome_texto='Rodas',nome_link='Rodas',lista=st.session_state.lista_imagens)         
                                                                        if reclamacao_Rodas != '':
                                                                            if reclamacao_Rodas in st.session_state.lista_problemas:
                                                                                  pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Rodas)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Rodas = st.checkbox(label='Normal', key='1Rodas')
                                                                    if normal_Rodas:
                                                                            if 'Rodas ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Rodas ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Rodas ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Rodas ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                            
                                                            preenchimento(normal=normal_Rodas, anormal=anormal_Rodas, campo='Rodas')
                                                            
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Chave liga/desliga')
                                                            with col2:
                                                                anormal_Chave = st.checkbox(label='Anormal', key='2Chave liga/desliga')
                                                                if anormal_Chave:
                                                                    with col4:
                                                                        reclamacao_Chave = st.text_input(label='Digite o Problema', key='texto_Chave liga/desliga')
                                                                        adicionar_imagem(nome_texto='Chave liga/desliga',nome_link='Chave liga_desliga',lista=st.session_state.lista_imagens) 
                                                                        if reclamacao_Chave != '':
                                                                            if reclamacao_Chave in st.session_state.lista_problemas:
                                                                                  pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Chave)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Chave = st.checkbox(label='Normal', key='1Chave liga/desliga')
                                                                    if normal_Chave:
                                                                            if 'Chave liga/desliga ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Chave liga/desliga ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Chave liga/desliga ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Chave liga/desliga ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                            
                                                            preenchimento(normal=normal_Chave, anormal=anormal_Chave, campo='Chave liga/desliga')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Bateria')
                                                            with col2:
                                                                anormal_Bateria = st.checkbox(label='Anormal', key='2bateria')
                                                                if anormal_Bateria:
                                                                    with col4:
                                                                        reclamacao_Bateria = st.text_input(label='Digite o Problema', key='texto_Bateria')
                                                                        adicionar_imagem(nome_texto='Bateria',nome_link='Bateria',lista=st.session_state.lista_imagens)         
                                                                        if reclamacao_Bateria !='':
                                                                            if reclamacao_Bateria in st.session_state.lista_problemas:
                                                                                  pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Bateria)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Bateria = st.checkbox(label='Normal', key='1Bateria')
                                                                    if normal_Bateria:
                                                                            if 'Bateria ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                                                        
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Bateria ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                                                    
                                                            
                                                            preenchimento(normal=normal_Bateria, anormal=anormal_Bateria, campo='Bateria')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Elevação dos Garfos')
                                                            with col2:
                                                                anormal_Elevação_dos_Garfos = st.checkbox(label='Anormal', key='2ellevação_dos_Garfossssss')
                                                                if anormal_Elevação_dos_Garfos:
                                                                    with col4:
                                                                        reclamacao_Elevação_dos_Garfos = st.text_input(label='Digite o Problema', key='texto_Elevvação_dos_gsarfos')
                                                                        adicionar_imagem(nome_texto='texto_Elevação_dos_gsarfos',nome_link='texto_Elevvação_dos_gsarfos',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Elevação_dos_Garfos != '':
                                                                            if reclamacao_Elevação_dos_Garfos in  st.session_state.lista_problemas:
                                                                                  pass
                                                                            else:
                                                                                  
                                                                                    st.session_state.lista_problemas.append(reclamacao_Elevação_dos_Garfos)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Elevação_dos_Garfos= st.checkbox(label='Normal', key='1ação arfos')
                                                                    if normal_Elevação_dos_Garfos:
                                                                            if 'Elevação dos Garfos ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Elevação dos Garfos ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))     
                                                                                    
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Elevação dos Garfos ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Elevação dos Garfos ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))            
                                                            preenchimento(normal=normal_Elevação_dos_Garfos, anormal=anormal_Elevação_dos_Garfos, campo='Elevação dos Garfos')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Trava da Bateria')
                                                            with col2:
                                                                anormal_Trava_da_Bateria = st.checkbox(label='Anormal', key='2travadaBateria')
                                                                if anormal_Trava_da_Bateria:
                                                                    with col4:
                                                                        reclamacao_Trava_da_Bateria = st.text_input(label='Digite o Problema', key='texto_Trava_da_bbBateria')
                                                                        adicionar_imagem(nome_texto='Trava da Bateria ',nome_link='Trava da Bateria ',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Trava_da_Bateria != '':
                                                                            if reclamacao_Trava_da_Bateria in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Trava_da_Bateria)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Trava_da_Bateria= st.checkbox(label='Normal', key='1TravadaBateria')
                                                                    if normal_Trava_da_Bateria:
                                                                            if 'Trava da Bateria ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Trava da Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                    pass
                                                                    else:
                                                                            if 'Trava da Bateria ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Trava da Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Trava_da_Bateria, anormal=anormal_Trava_da_Bateria, campo='Trava da Bateria')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Limpeza Externa')
                                                            with col2:
                                                                anormal_Limpeza_Externa = st.checkbox(label='Anormal', key='2mmpeza')
                                                                if anormal_Limpeza_Externa:
                                                                    with col4:
                                                                        reclamacao_Limpeza_Externa = st.text_input(label='Digite o Problema', key='texto_externa')
                                                                        adicionar_imagem(nome_texto='Limpeza Externa',nome_link='Limpeza Externa',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Limpeza_Externa != '':
                                                                            if reclamacao_Limpeza_Externa in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Limpeza_Externa)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Limpeza_Externa= st.checkbox(label='Normal', key='1Limpeza_Externnnnnna')
                                                                    if normal_Limpeza_Externa:
                                                                            if 'Limpeza Externa ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Limpeza Externa ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Limpeza Externa ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Limpeza Externa ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Limpeza_Externa, anormal=anormal_Limpeza_Externa, campo='Limpeza Externa')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Folga no acelerador')
                                                            with col2:
                                                                anormal_Folga_no_acelerador = st.checkbox(label='Anormal', key='2folgha no acelerador')
                                                                if anormal_Folga_no_acelerador:
                                                                    with col4:
                                                                        reclamacao_Folga_no_acelerador = st.text_input(label='Digite o Problema', key='texto_folgaa_noooo__aceleradorrrrrrr')
                                                                        adicionar_imagem(nome_texto='Folga no acelerador',nome_link='Folga no acelerador',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Folga_no_acelerador != '':
                                                                            if reclamacao_Folga_no_acelerador in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Folga_no_acelerador)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Folga_no_acelerador= st.checkbox(label='Normal', key='1Folga no acelerador')
                                                                    if normal_Folga_no_acelerador:
                                                                            if 'Folga no acelerador ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Folga no acelerador ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Folga no acelerador ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Folga no acelerador ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Folga_no_acelerador, anormal=anormal_Folga_no_acelerador, campo='Folga no acelerador')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Acionamento Hidráulico')
                                                            with col2:
                                                                anormal_Acionamento_Hidráulico = st.checkbox(label='Anormal', key='ionamento_Hiddro')
                                                                if anormal_Acionamento_Hidráulico:
                                                                    with col4:
                                                                        reclamacao_Acionamento_Hidráulico = st.text_input(label='Digite o Problema', key='texto_mento_lico')
                                                                        adicionar_imagem(nome_texto='Acionamento Hidráulico',nome_link='Acionamento Hidráulico',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Acionamento_Hidráulico != '':
                                                                            if reclamacao_Acionamento_Hidráulico in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Acionamento_Hidráulico)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Acionamento_Hidráulico= st.checkbox(label='Normal', key='1Accionamento Hidráulico')
                                                                    if normal_Acionamento_Hidráulico:
                                                                            if 'Acionamento Hidráulico ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Acionamento Hidráulico ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Acionamento Hidráulico ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Acionamento Hidráulico ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Acionamento_Hidráulico, anormal=anormal_Acionamento_Hidráulico, campo='Acionamento Hidráulico')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Horímetro')
                                                            with col2:
                                                                anormal_Horímetro = st.checkbox(label='Anormal', key='2hhorimetro')
                                                                if anormal_Horímetro:
                                                                    with col4:
                                                                        reclamacao_Horímetro = st.text_input(label='Digite o Problema', key='texto_Horrimetro')
                                                                        adicionar_imagem(nome_texto='Horímetro',nome_link='Horímetro',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Horímetro !='':
                                                                            if reclamacao_Horímetro in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Horímetro)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Horímetro= st.checkbox(label='Normal', key='1Hoorímetro')
                                                                    if normal_Horímetro:
                                                                            if 'Horímetro ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Horímetro ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Horímetro ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Horímetro ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Horímetro, anormal=anormal_Horímetro, campo='Horímetro')
                                                            
                                                            
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Chave Direcional')
                                                            with col2:
                                                                anormal_Chave_Direcional = st.checkbox(label='Anormal', key='2chave_DDirecional')
                                                                if anormal_Chave_Direcional:
                                                                    with col4:
                                                                        reclamacao_Chave_Direcional = st.text_input(label='Digite o Problema', key='texto_Chave_Dirrecional')
                                                                        adicionar_imagem(nome_texto='Chave Direcional',nome_link='Chave Direcional',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Chave_Direcional !='':
                                                                            if reclamacao_Chave_Direcional in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Chave_Direcional)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Chave_Direcional= st.checkbox(label='Normal', key='1Chave Direcional')
                                                                    if normal_Chave_Direcional:
                                                                            if 'Chave Direcional ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Chave Direcional ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))    
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Chave Direcional ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Chave Direcional ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Chave_Direcional, anormal=anormal_Chave_Direcional, campo='Chave Direcional')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Botão de Emergência')
                                                            with col2:
                                                                anormal_Botão_de_Emergência = st.checkbox(label='Anormal', key='2botão de Emergência')
                                                                if anormal_Botão_de_Emergência:
                                                                    with col4:
                                                                        reclamacao_Botão_de_Emergência = st.text_input(label='Digite o Problema', key='texto_Botão de Emergência')
                                                                        adicionar_imagem(nome_texto='Botão de Emergência',nome_link='Botão de Emergência',lista=st.session_state.lista_imagens)        
                                                                        if reclamacao_Botão_de_Emergência !='':
                                                                            if reclamacao_Botão_de_Emergência in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Botão_de_Emergência)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Botão_de_Emergência= st.checkbox(label='Normal', key='1Botão de Emergência')
                                                                    if normal_Botão_de_Emergência:
                                                                            if 'Botão de Emergência ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Botão de Emergência ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Botão de Emergência ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Botão de Emergência ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Botão_de_Emergência, anormal=anormal_Botão_de_Emergência, campo='Botão de Emergência')
                                                            
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Condição dos Garfos')
                                                            with col2:
                                                                anormal_Condição_dos_Garfos = st.checkbox(label='Anormal', key='2condiçãooooo_dos_Garfossssssss')
                                                                if anormal_Condição_dos_Garfos:
                                                                    with col4:
                                                                        reclamacao_Condição_dos_Garfos = st.text_input(label='Digite o Problema', key='texto_cccccondição_dos_garfooooooos')
                                                                        adicionar_imagem(nome_texto='Condição dos Garfos',nome_link='Condição dos Garfos',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Condição_dos_Garfos != '':
                                                                            if reclamacao_Condição_dos_Garfos in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Condição_dos_Garfos)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Condição_dos_Garfos= st.checkbox(label='Normal', key='1Condição dos Garfos')
                                                                    if normal_Condição_dos_Garfos:
                                                                            if 'Condição dos Garfos ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Condição dos Garfos ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Condição dos Garfos ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Condição dos Garfos ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Condição_dos_Garfos, anormal=anormal_Condição_dos_Garfos, campo='Condição dos Garfos')
                                                            
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Timão')
                                                            with col2:
                                                                anormal_Timão = st.checkbox(label='Anormal', key='2timão')
                                                                if anormal_Timão:
                                                                    with col4:
                                                                        reclamacao_Timão = st.text_input(label='Digite o Problema', key='texto_Timão')
                                                                        adicionar_imagem(nome_texto='Timão',nome_link='Timão',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Timão !='':
                                                                            if reclamacao_Timão in  st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Timão)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Timão= st.checkbox(label='Normal', key='1Timão')
                                                                    if normal_Timão:
                                                                            if 'Timão ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Timão ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Timão ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Timão ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Timão, anormal=anormal_Timão, campo='Timão')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Indicador de Bateria')
                                                            with col2:
                                                                anormal_Indicador_de_Bateria = st.checkbox(label='Anormal', key='2indicador de Bateria')
                                                                if anormal_Indicador_de_Bateria:
                                                                    with col4:
                                                                        reclamacao_Indicador_de_Bateria = st.text_input(label='Digite o Problema', key='texto_Indicador de Bateria')
                                                                        adicionar_imagem(nome_texto='Indicador de Bateria',nome_link='Indicador de Bateria',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Indicador_de_Bateria != '':
                                                                            if reclamacao_Indicador_de_Bateria in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                    st.session_state.lista_problemas.append(reclamacao_Indicador_de_Bateria)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Indicador_de_Bateria= st.checkbox(label='Normal', key='1Indicador_de_Bateria')
                                                                    if normal_Indicador_de_Bateria:
                                                                            if 'Indicador_de_Bateria ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Indicador de Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Indicador_de_Bateria ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Indicador de Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Indicador_de_Bateria, anormal=anormal_Indicador_de_Bateria, campo='Indicador de Bateria')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Freio de Serviço')
                                                            with col2:
                                                                anormal_Freio_de_Serviço = st.checkbox(label='Anormal', key='2freio de Serviço')
                                                                if anormal_Freio_de_Serviço:
                                                                    with col4:
                                                                        reclamacao_Freio_de_Serviço = st.text_input(label='Digite o Problema', key='texto_Freio de Serviço')
                                                                        adicionar_imagem(nome_texto='Freio de Serviço',nome_link='Freio de Serviço',lista=st.session_state.lista_imagens)          
                                                                        if reclamacao_Freio_de_Serviço != '':
                                                                            if reclamacao_Freio_de_Serviço in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Freio_de_Serviço)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Freio_de_Serviço= st.checkbox(label='Normal', key='1Freio de Serviço')
                                                                    if normal_Freio_de_Serviço:
                                                                            if 'Freio de Serviço ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Freio de Serviço ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Freio de Serviço ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Freio de Serviço ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                                                                            
                                                            
                                                            preenchimento(normal=normal_Freio_de_Serviço, anormal=anormal_Freio_de_Serviço, campo='Freio de Serviço')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Reversão')
                                                            with col2:
                                                                anormal_Reversão = st.checkbox(label='Anormal', key='2reversão')
                                                                if anormal_Reversão:
                                                                    with col4:
                                                                        reclamacao_Reversão = st.text_input(label='Digite o Problema', key='texto_Reversão')
                                                                        adicionar_imagem(nome_texto='Reversão',nome_link='Reversão',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Reversão !='':
                                                                            if reclamacao_Reversão in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Reversão)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Reversão= st.checkbox(label='Normal', key='1Reversão')
                                                                    if normal_Reversão:
                                                                            if 'Reversão ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Reversão ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Reversão ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Reversão ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            
                                                            preenchimento(normal=normal_Reversão, anormal=anormal_Reversão, campo='Reversão')
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Velocidade')
                                                            with col2:
                                                                anormal_Velocidade = st.checkbox(label='Anormal', key='2velocidade')
                                                                if anormal_Velocidade:
                                                                    with col4:
                                                                        reclamacao_Velocidade = st.text_input(label='Digite o Problema', key='texto_Velocidade')
                                                                        adicionar_imagem(nome_texto='Velocidade',nome_link='Velocidade',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Velocidade !='':
                                                                            if reclamacao_Velocidade in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Velocidade)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Velocidade= st.checkbox(label='Normal', key='1Velocidade')
                                                                    if normal_Velocidade:
                                                                            if 'Velocidade ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Velocidade ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Velocidade ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Velocidade ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Velocidade, anormal=anormal_Velocidade, campo='Velocidade')
                                                            
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Ruidos')
                                                            with col2:
                                                                anormal_Ruidos = st.checkbox(label='Anormal', key='2ruidos')
                                                                if anormal_Ruidos:
                                                                    with col4:
                                                                        reclamacao_Ruidos = st.text_input(label='Digite o Problema', key='texto_Ruidos')
                                                                        adicionar_imagem(nome_texto='Ruidos',nome_link='Ruidos',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Ruidos !='':
                                                                            if reclamacao_Ruidos in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Ruidos)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Ruidos= st.checkbox(label='Normal', key='1Ruidos')
                                                                    if normal_Ruidos:
                                                                            if 'Ruidos ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Ruidos ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Ruidos ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Ruidos ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Ruidos, anormal=anormal_Ruidos, campo='Ruidos')
                                                            
                                                            
                                                            col1, col2, col3, col4 = st.columns(4)
                                                            with col1:
                                                                    st.write('Tomadas e cabos da Bateria')
                                                            with col2:
                                                                anormal_Tomadas_e_cabos_da_Bateria = st.checkbox(label='Anormal', key='2tomadas e cabos da Bateria')
                                                                if anormal_Tomadas_e_cabos_da_Bateria:
                                                                    with col4:
                                                                        reclamacao_Tomadas_e_cabos_da_Bateria = st.text_input(label='Digite o Problema', key='texto_Tomadas e cabos da Bateria')
                                                                        adicionar_imagem(nome_texto='Tomadas e cabos da Bateria',nome_link='Tomadas e cabos da Bateria',lista=st.session_state.lista_imagens)
                                                                        if reclamacao_Tomadas_e_cabos_da_Bateria !='':
                                                                            if reclamacao_Tomadas_e_cabos_da_Bateria in st.session_state.lista_problemas:
                                                                                   pass
                                                                            else:
                                                                                   
                                                                                    st.session_state.lista_problemas.append(reclamacao_Tomadas_e_cabos_da_Bateria)
                                                                                    st.session_state.lista_qtd.append(str('...'))
                                                                                    st.warning('Problema relatado')
                                                            
                                                            with col3:
                                                                    normal_Tomadas_e_cabos_da_Bateria= st.checkbox(label='Normal', key='1Tomadas e cabos da Bateria')
                                                                    if normal_Tomadas_e_cabos_da_Bateria:
                                                                            if 'Tomadas e cabos da Bateria ok' not in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.append('Tomadas e cabos da Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                                            else:
                                                                                   pass
                                                                    else:
                                                                            if 'Tomadas e cabos da Bateria ok' in st.session_state.lista_qtd:
                                                                                    st.session_state.lista_qtd.remove('Tomadas e cabos da Bateria ok')
                                                                                    st.session_state.lista_problemas.append(str('...'))
                                                                                    st.session_state.lista_imagens.append(str('...'))
                                                            
                                                            preenchimento(normal=normal_Tomadas_e_cabos_da_Bateria, anormal=anormal_Tomadas_e_cabos_da_Bateria, campo='Tomadas e cabos da Bateria')
                                                            
                                                            max_length = max(len(st.session_state.lista_qtd), len(st.session_state.lista_problemas),len(st.session_state.lista_imagens))
                                                            st.session_state.lista_qtd.extend([''] * (max_length - len(st.session_state.lista_qtd)))
                                                            st.session_state.lista_problemas.extend([''] * (max_length - len(st.session_state.lista_problemas)))
                                                            st.session_state.lista_imagens.extend([''] * (max_length - len(st.session_state.lista_problemas)))
                                                            dict_resposta = {'Item ok': st.session_state.lista_qtd, 'Item Anormal': st.session_state.lista_problemas}
                                                            pdf_buffer = criar_pdf_em_memoria(dict_resposta)
                                                            
                                                            
                                                            
                                                            
                                                            col1,col2,col3 = st.columns(3)
                                                            with col1:
                                                                        botao_email = st.button('Enviar Cheklist')
                                                                        if botao_email:
                                                                                        enviar_emaail(dados=dict_resposta,usuario=usuario,pdf_buffer=pdf_buffer,lista = st.session_state.lista_imagens)       
                                                                                        #enviar_emaail2(dados=dict_resposta,usuario=usuario,pdf_buffer=pdf_buffer,lista = st.session_state.lista_imagens)        
                                                                                        estatistica(nao=st.session_state.lista_problemas,sim=st.session_state.lista_qtd,usuario=usuario,data=data_hora_formatada,imagem=st.session_state.lista_imagens)        
                                                                                        st.session_state.lista_qtd = []
                                                                                        st.session_state.lista_problemas = []
                                                                                        st.session_state.lista_imagens = []        
                                                                                        st.session_state.mostrar_reclamacao = False
                                                                                        reset_checkboxes()
                                                                                        st.success('Relatório Enviado')
                                                                                        baixar()
                                                                                        with col2:
                                                                                                    @st.cache_data
                                                                                                    def convert_df(df):    
                                                                                                  
                                                                                                                    data_str = {key: str(value) for key, value in df.items()}        
                                                                                                                    df = pd.DataFrame(df)    
                                                                                                                    return df.to_csv(index=False)
                                                                                                    with st.popover("📂"):               
                                                                                                                            arquivo = convert_df(dict_resposta)
                                                                                                                            
                                                                                                                            download = st.download_button(
                                                                                                                                label="Faça o download do checklist no formato csv",
                                                                                                                                data=arquivo,
                                                                                                                                file_name="checklist.csv",
                                                                                                                                mime="text/csv",
                                                                                                                                                    )
                                                                                                                            if download:
                                                                                                                                        st.success('Arquivo csv baixado com sucesso')
                                                                            

elif seletor == 'Excluir Checklist':
            
            texto_excluir = st.text_input(label = 'Insira a Senha do Administrador',type = 'password')
            if texto_excluir == str(2314):
                        lista2 = []
                        usuario2 = st.selectbox('Usuário', ['Juan Zonho', 'Jonatan Lima','Cesar Fusel','Luiz Felipe'],index=None,placeholder='Insira um usuário para exclusão')
                        if usuario2:
                          try:
                            requiscao = requests.get('https://bancodedadosroteirooficial-default-rtdb.firebaseio.com/.json')
                          
                            
                            roteiro = requiscao.json()
                            dados = roteiro['Checklists']
                            for item in dados:          
                                                                        
                                                              Checklist = dados[f'{item}']
                                                              for elemento in Checklist:
                                                                       espec = Checklist[f'{elemento}']
                                                                       usuario = espec['Usuário']
                                                                       if usuario == usuario2:
                                                                                   lista2.append(item)
                                                                       else:
                                                                                   pass
                            data = st.selectbox('Data', lista2)
                            if data:
                              excluir = st.button('Excluir Checklist')
                              if excluir: 
                                    escolha(data)                  
                                                      
                              else:
                                          pass
                          except:
                              st.error('Não há checklists para excluir')
            elif texto_excluir == '':
                        st.info('Você ainda não inseriu a senha')
            else:
                        st.error('Acesso Negado')
