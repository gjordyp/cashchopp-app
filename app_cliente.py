import streamlit as st
import pandas as pd
import re
import requests
import hashlib

st.set_page_config(page_title="CashChopp - Fidelidade", page_icon="🍺")

# LINK DA SUA API (O mesmo que você usa no PC)
URL_API = "https://script.google.com/macros/s/AKfycbwfOpeCvM-osCHjYh-JTh8noJ0RFE17ZvGunSlxySvkH2KD9Qq9xMpZKJpgGL1qtE8i/exec"

# Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; height: 3em; }
    .saldo-box { background-color: #333; padding: 30px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

def limpar(txt):
    return re.sub(r'\D', '', str(txt)).strip()

# Menu Lateral
menu = st.sidebar.selectbox("O que deseja fazer?", ["Consultar Saldo", "Cadastrar Novo Cliente"])

if menu == "Consultar Saldo":
    st.title("🍺 Meu Saldo")
    cpf_input = st.text_input("Digite seu CPF (apenas números):")
    
    if st.button("VER SALDO"):
        if not cpf_input:
            st.warning("Digite o CPF.")
        else:
            try:
                # Pega os dados da API
                res = requests.get(URL_API, timeout=15)
                if res.status_code == 200:
                    dados = res.json()
                    busca = limpar(cpf_input).zfill(11)
                    
                    # Procura o cliente na lista da nuvem
                    cliente = next((item for item in dados if str(item['cpf']).replace("'","").zfill(11) == busca), None)
                    
                    if cliente:
                        nome = str(cliente['nome']).split()[0].upper()
                        saldo = float(cliente['saldo'])
                        st.markdown(f"### Olá, **{nome}**!")
                        st.markdown(f"""<div class="saldo-box">
                            <p style="color: #bbb;">Seu Saldo:</p>
                            <h1 style="color: #ffcc00; font-size: 50px;">R$ {saldo:.2f}</h1>
                        </div>""", unsafe_allow_html=True)
                        if saldo > 0: st.balloons()
                    else:
                        st.error("CPF não encontrado. Faça seu cadastro!")
            except Exception as e:
                st.error(f"Erro ao conectar: {e}")

else:
    st.title("📝 Cadastro CashChopp")
    st.write("Preencha os dados abaixo para começar a ganhar cashback!")
    
    with st.form("form_cadastro"):
        novo_nome = st.text_input("Nome Completo:").upper()
        novo_cpf = st.text_input("CPF (apenas números):", max_chars=11)
        nova_nasc = st.text_input("Data de Nascimento (DD/MM/AAAA):", placeholder="Ex: 31/07/1993")
        novo_email = st.text_input("E-mail:")
        
        enviar = st.form_submit_button("FINALIZAR CADASTRO")
        
        if enviar:
            cpf_limpo = limpar(novo_cpf)
            if len(cpf_limpo) != 11 or not novo_nome or len(nova_nasc) < 10:
                st.error("Por favor, preencha todos os campos corretamente.")
            else:
                # Gera o ID Digital igual ao seu app do PC
                idd = hashlib.md5(cpf_limpo.encode()).hexdigest()[:6].upper()
                
                # Monta o pacote para enviar para a planilha
                pacote = {
                    "mode": "update",
                    "cpf": "'" + cpf_limpo,
                    "nome": novo_nome,
                    "saldo": 0,
                    "id_digital": idd,
                    "nascimento": nova_nasc,
                    "email": novo_email.lower()
                }
                
                try:
                    r = requests.post(URL_API, json=pacote, timeout=15)
                    if r.status_code == 200:
                        st.success("✅ Cadastro realizado com sucesso!")
                        st.info(f"Seu ID Digital para resgates é: **{idd}**")
                        st.warning("Apresente seu CPF ao atendente na hora da compra!")
                    else:
                        st.error("Erro no servidor da planilha.")
                except Exception as e:
                    st.error(f"Falha ao enviar cadastro: {e}")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
