import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st

password2 = st.secrets["firebase"]["senha_email"]

def enviar_email(dados, usuario, pdf_buffer, lista):
    df = pd.DataFrame(dados)
    tabela_html = df.to_html(index=False)

    sender_email = "juanpablozonho@gmail.com"
    receiver_email = "juanzsalca@outlook.com"
    password = password2

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Tabela de Dados"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""
    <html>
    <body>
        <p>Usuário: {usuario}<br>
        Aqui está a tabela de dados:<br>
        </p>
        {tabela_html}
    </body>
    </html>
    """
    for item in lista:
        caminho_imagem = item
        imagem_html = f'<img src="{caminho_imagem}" alt="Imagem {item}">'
        tabela_html = tabela_html.replace(f"<td>{item}</td>", f"<td>{imagem_html}</td>")

    part = MIMEText(html, "html")
    msg.attach(part)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="relatorio.pdf"')
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def enviar_email2(dados, usuario, pdf_buffer, lista):
    df = pd.DataFrame(dados)
    tabela_html = df.to_html(index=False)

    sender_email = "juanpablozonho@gmail.com"
    receiver_email = "Jonatan.lima@thule.com"
    password = st.secrets["firebase"]["password"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Tabela de Dados"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""
    <html>
    <body>
        <p>Usuário: {usuario}<br>
        Aqui está a tabela de dados:<br>
        </p>
        {tabela_html}
    </body>
    </html>
    """

    part = MIMEText(html, "html")
    msg.attach(part)
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="relatorio.pdf"')
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
