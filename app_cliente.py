import streamlit as st
import pandas as pd
import re
import requests
import hashlib

# 1. Configuração de Página
st.set_page_config(page_title="CashChopp - Fidelidade", page_icon="🍺")

# LINK DA SUA API (O mesmo que você usa no PC)
URL_API = "https://script.google.com/macros/s/AKfycbwfOpeCvM-osCHjYh-JTh8noJ0RFE17ZvGunSlxySvkH2KD9Qq9xMpZKJpgGL1qtE8i/exec"

# 2. Estilo Visual Personalizado
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; margin-bottom: 0px; }
    h3 { color: white; text-align: center; }
    /* Estilo dos Botões de Navegação */
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3.5em; 
        font-weight: bold;
        font-size: 16px;
    }
    /* Caixa de Saldo */
    .saldo-box { 
        background-color: #333; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #ffcc00; 
        text-align: center; 
        margin-top: 20px;
    }
    /* Esconder o menu lateral original do Streamlit para ficar mais limpo */
    [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

def limpar(txt):
    return re.sub(r'\D', '', str(txt)).strip()

# Título Principal
st.title("🍺 CashChopp")
st.markdown("---")

# 3. Botões de Navegação no Topo (Lado a Lado)
col1, col2 = st.columns(2)

# Usamos o "session_state" para saber qual aba está ativa
if 'aba' not in st.session_state:
    st.session_state.aba = 'login'

with col1:
    if st.button("🔍 VER SALDO"):
        st.session_state.aba = 'login'

with col2:
    if st.button("📝 CADASTRE-SE"):
        st.session_state.aba = 'cadastro'

st.markdown("---")

# 4. Lógica das Telas
if st.session_state.aba == 'login':
    st.subheader("Consulte seu saldo")
    cpf_input = st.text_input("Digite seu CPF:", placeholder="000.000.000-00")
    
    if st.button("VER MEU SALDO AGORA"):
        if not cpf_input:
            st.warning("Por favor, informe o CPF.")
        else:
            with st.spinner('Buscando seu chopp...'):
                try:
                    res = requests.get(URL_API, timeout=15)
                    if res.status_code == 200:
                        dados = res.json()
                        busca = limpar(cpf_input).zfill(11)
                        
                        cliente = next((item for item in dados if str(item['cpf']).replace("'","").zfill(11) == busca), None)
                        
                        if cliente:
                            nome = str(cliente['nome']).split()[0].upper()
                            saldo = float(cliente['saldo'])
                            st.markdown(f"### Olá, **{nome}**! 🍻")
                            st.markdown(f"""<div class="saldo-box">
                                <p style="color: #bbb; margin-bottom: 5px;">Você tem acumulado:</p>
                                <h1 style="color: #ffcc00; font-size: 55px; margin: 0;">R$ {saldo:.2f}</h1>
                            </div>""", unsafe_allow_html=True)
                            if saldo > 0: st.balloons()
                        else:
                            st.error("CPF não encontrado. Clique em CADASTRE-SE no topo!")
                except:
                    st.error("Erro ao conectar com o servidor. Tente novamente.")

else:
    st.subheader("Novo Cadastro")
    with st.form("form_cad"):
        n_nome = st.text_input("Nome Completo:").upper()
        n_cpf = st.text_input("CPF (apenas números):", max_chars=11)
        n_nasc = st.text_input("Nascimento (DD/MM/AAAA):")
        n_email = st.text_input("E-mail:")
        
        btn_cad = st.form_submit_button("FINALIZAR E GANHAR CASHBACK")
        
        if btn_cad:
            c_limpo = limpar(n_cpf)
            if len(c_limpo) != 11 or not n_nome:
                st.error("Preencha os dados corretamente!")
            else:
                idd = hashlib.md5(c_limpo.encode()).hexdigest()[:6].upper()
                pacote = {
                    "mode": "update",
                    "cpf": "'" + c_limpo,
                    "nome": n_nome,
                    "saldo": 0,
                    "id_digital": idd,
                    "nascimento": n_nasc,
                    "email": n_email.lower()
                }
                try:
                    r = requests.post(URL_API, json=pacote, timeout=15)
                    if r.status_code == 200:
                        st.success("✅ Cadastro concluído!")
                        st.info(f"Seu ID Digital: **{idd}**")
                        st.balloons()
                    else: st.error("Erro ao salvar.")
                except: st.error("Erro de conexão.")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
