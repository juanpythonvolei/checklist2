import qrcode
import streamlit as st
from PIL import Image
import tempfile
import time


image = st.image('https://www.logolynx.com/images/logolynx/fe/fe346f78d111e1d702b44186af59b568.jpeg')
time.sleep(0.2)
msg1 = st.toast('Seja Bem vindo a aba de endereços')
time.sleep(1)
msg2= st.toast('Aqui, Você pode ser direcionado para os apps de checklists ou Gerenciamento logístico')
url = 'https://appchecklistthulee.streamlit.app/?embed_options=dark_theme'


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)


img_qrcode = qr.make_image(fill_color="black", back_color="white")


with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
    img_qrcode.save(tmpfile.name)
    tmpfile_path = tmpfile.name
url2 = 'https://gerenciamentologisticoapp.streamlit.app/?embed_options=dark_theme'

# Cria o QR code
qr2 = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr2.add_data(url2)
qr2.make(fit=True)


img_qrcode2 = qr2.make_image(fill_color="black", back_color="white")


with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile_second:
    img_qrcode2.save(tmpfile_second.name)
    tmpfile_path_second = tmpfile_second.name

with st.popover("🔍"):
    st.markdown("Olá. O QRCODE abaixo leva a esse aplicativo que você está utilizando")
    st.image(tmpfile_path)
    st.divider()
    st.markdown('E esse QRCODE leva ao aplicativo de gerenciamento logístico')
    st.image(tmpfile_path_second)
    st.link_button("Acessar app 🚪", url2)

















    
   


