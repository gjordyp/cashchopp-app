import streamlit as st
import pandas as pd
import re
import requests
import hashlib

# 1. Configuração de Página
st.set_page_config(page_title="CashChopp - Fidelidade", page_icon="🍺")

URL_API = "https://script.google.com/macros/s/AKfycbwfOpeCvM-osCHjYh-JTh8noJ0RFE17ZvGunSlxySvkH2KD9Qq9xMpZKJpgGL1qtE8i/exec"

# 2. Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: white; text-align: center; margin-top: 0px; }
    div.stButton > button {
        width: 160px; border-radius: 8px; height: 3.2em; 
        font-weight: bold; font-size: 14px; border: 2px solid #ffcc00;
        transition: 0.3s; margin: 0 auto; display: block;
    }
    .saldo-box { 
        background-color: #333; padding: 20px; border-radius: 15px; 
        border: 2px solid #ffcc00; text-align: center; margin-top: 15px;
    }
    .id-badge {
        background-color: #ffcc00; color: black; padding: 5px 15px;
        border-radius: 20px; font-weight: bold; display: inline-block;
        margin-top: 10px; font-size: 18px;
    }
    .block-container { padding-top: 2rem; }
    [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

def limpar(txt):
    return re.sub(r'\D', '', str(txt)).strip()

def validar_cpf(cpf):
    cpf = limpar(cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]): return False
    return True

# Cabeçalho
st.title("🍺 CashChopp")
st.markdown("### Seu Fidelidade Digital")

if 'aba' not in st.session_state: st.session_state.aba = 'login'

col_e, col_c1, col_c2, col_d = st.columns([1, 2, 2, 1])
with col_c1:
    if st.button("🔍 VER SALDO"): st.session_state.aba = 'login'
with col_c2:
    if st.button("📝 CADASTRAR"): st.session_state.aba = 'cadastro'

st.markdown("---")

if st.session_state.aba == 'login':
    cpf_input = st.text_input("Digite seu CPF para consultar:", placeholder="Apenas números")
    _, col_v, _ = st.columns([1, 2, 1])
    with col_v: btn_verificar = st.button("VERIFICAR")

    if btn_verificar:
        if not validar_cpf(cpf_input):
            st.error("CPF Inválido! Verifique os números.")
        else:
            with st.spinner('Consultando seu chopp...'):
                try:
                    res = requests.get(URL_API, timeout=15)
                    dados = res.json()
                    busca = limpar(cpf_input).zfill(11)
                    cliente = next((item for item in dados if str(item['cpf']).replace("'","").zfill(11) == busca), None)
                    
                    if cliente:
                        nome = str(cliente['nome']).split()[0].upper()
                        saldo = float(cliente['saldo'])
                        idd = str(cliente.get('id_digital', '---')).upper()
                        st.markdown(f"### Olá, **{nome}**!")
                        st.markdown(f"""<div class="saldo-box">
                            <p style="color: #bbb; margin-bottom: 0;">Seu Saldo:</p>
                            <h1 style="color: #ffcc00; font-size: 50px; margin: 0;">R$ {saldo:.2f}</h1>
                            <p style="color: #bbb; margin-top: 15px; font-size: 14px;">Seu ID para Resgate:</p>
                            <div class="id-badge">{idd}</div>
                        </div>""", unsafe_allow_html=True)
                        if saldo > 0: st.balloons()
                    else:
                        st.error("CPF não encontrado no sistema.")
                except: st.error("Erro de conexão.")

else:
    st.subheader("Novo Cadastro")
    with st.form("form_cad"):
        n_nome = st.text_input("Nome Completo:").upper()
        n_cpf = st.text_input("CPF (Apenas números):", max_chars=11)
        n_cpf2 = st.text_input("Confirme o CPF:", max_chars=11)
        n_nasc = st.text_input("Nascimento (DD/MM/AAAA):")
        n_email = st.text_input("E-mail:")
        btn_cad = st.form_submit_button("CADASTRAR AGORA")
        
        if btn_cad:
            if n_cpf != n_cpf2:
                st.error("Os CPFs digitados não são iguais!")
            elif not validar_cpf(n_cpf):
                st.error("Este número de CPF é inválido!")
            elif not n_nome or len(n_nasc) < 10:
                st.error("Preencha todos os campos.")
            else:
                c_limpo = limpar(n_cpf)
                idd_novo = hashlib.md5(c_limpo.encode()).hexdigest()[:6].upper()
                pacote = {"mode": "update", "cpf": "'" + c_limpo, "nome": n_nome, "saldo": 0, "id_digital": idd_novo, "nascimento": n_nasc, "email": n_email.lower()}
                try:
                    r = requests.post(URL_API, json=pacote, timeout=15)
                    st.success("✅ Cadastro concluído!")
                    st.markdown(f"""<div class="saldo-box"><p style="color: white;">ID de Resgate:</p><div class="id-badge">{idd_novo}</div></div>""", unsafe_allow_html=True)
                    st.balloons()
                except: st.error("Erro de conexão.")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
