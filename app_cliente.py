import streamlit as st
import pandas as pd
import re
import requests
import hashlib

# 1. Configuração de Página
st.set_page_config(page_title="CashChopp - Fidelidade", page_icon="🍺")

# LINK DA SUA API (Mantenha o seu link atual aqui)
URL_API = "https://script.google.com/macros/s/AKfycbwfOpeCvM-osCHjYh-JTh8noJ0RFE17ZvGunSlxySvkH2KD9Qq9xMpZKJpgGL1qtE8i/exec"

# 2. Estilo Visual Simétrico e Moderno
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; margin-bottom: 5px; }
    h3 { color: white; text-align: center; margin-top: 0px; }
    
    /* Ajuste de Simetria dos Botões */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.2em; 
        font-weight: bold;
        font-size: 15px;
        border: 2px solid #ffcc00;
        transition: 0.3s;
    }
    
    /* Caixa de Saldo e ID */
    .saldo-box { 
        background-color: #333; 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px solid #ffcc00; 
        text-align: center; 
        margin-top: 15px;
    }
    .id-badge {
        background-color: #ffcc00;
        color: black;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
    }
    
    /* Remove espaços extras do Streamlit */
    .block-container { padding-top: 2rem; }
    [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

def limpar(txt):
    return re.sub(r'\D', '', str(txt)).strip()

# Cabeçalho
st.title("🍺 CashChopp")
st.markdown("### Seu Fidelidade Digital")

# 3. Navegação Simétrica (Abas)
if 'aba' not in st.session_state:
    st.session_state.aba = 'login'

# Colunas com pouco espaço entre elas para simetria
c1, c2 = st.columns(2, gap="small")

with c1:
    if st.button("🔍 VER SALDO"):
        st.session_state.aba = 'login'

with c2:
    if st.button("📝 CADASTRAR"):
        st.session_state.aba = 'cadastro'

st.markdown("---")

# 4. Conteúdo das Telas
if st.session_state.aba == 'login':
    cpf_input = st.text_input("Digite seu CPF para consultar:", placeholder="Apenas números")
    
    if st.button("VERIFICAR"):
        if not cpf_input:
            st.warning("Informe seu CPF.")
        else:
            with st.spinner('Consultando barril...'):
                try:
                    res = requests.get(URL_API, timeout=15)
                    if res.status_code == 200:
                        dados = res.json()
                        busca = limpar(cpf_input).zfill(11)
                        
                        cliente = next((item for item in dados if str(item['cpf']).replace("'","").zfill(11) == busca), None)
                        
                        if cliente:
                            nome = str(cliente['nome']).split()[0].upper()
                            saldo = float(cliente['saldo'])
                            idd = str(cliente.get('id_digital', '---')).upper()
                            
                            st.markdown(f"### Olá, **{nome}**!")
                            st.markdown(f"""
                                <div class="saldo-box">
                                    <p style="color: #bbb; margin-bottom: 0;">Seu Saldo:</p>
                                    <h1 style="color: #ffcc00; font-size: 50px; margin: 0;">R$ {saldo:.2f}</h1>
                                    <p style="color: #bbb; margin-top: 15px; font-size: 14px;">Seu ID para Resgate:</p>
                                    <div class="id-badge">{idd}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            if saldo > 0: st.balloons()
                        else:
                            st.error("CPF não encontrado. Faça seu cadastro ao lado!")
                except:
                    st.error("Erro de conexão. Tente novamente.")

else:
    st.subheader("Novo Cadastro")
    with st.form("form_cad"):
        n_nome = st.text_input("Nome Completo:").upper()
        n_cpf = st.text_input("CPF (Apenas números):", max_chars=11)
        n_nasc = st.text_input("Nascimento (DD/MM/AAAA):")
        n_email = st.text_input("E-mail:")
        
        btn_cad = st.form_submit_button("CADASTRAR AGORA")
        
        if btn_cad:
            c_limpo = limpar(n_cpf)
            if len(c_limpo) != 11 or not n_nome:
                st.error("Preencha os dados corretamente.")
            else:
                idd_novo = hashlib.md5(c_limpo.encode()).hexdigest()[:6].upper()
                pacote = {
                    "mode": "update",
                    "cpf": "'" + c_limpo,
                    "nome": n_nome,
                    "saldo": 0,
                    "id_digital": idd_novo,
                    "nascimento": n_nasc,
                    "email": n_email.lower()
                }
                try:
                    r = requests.post(URL_API, json=pacote, timeout=15)
                    if r.status_code == 200:
                        st.success("✅ Tudo pronto! Agora é só beber.")
                        st.markdown(f"""
                            <div class="saldo-box">
                                <p style="color: white;">Guarde seu ID de Resgate:</p>
                                <div class="id-badge" style="font-size: 25px;">{idd_novo}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    else: st.error("Erro ao salvar dados.")
                except: st.error("Erro de conexão.")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
