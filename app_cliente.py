import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="CashChopp - Meu Saldo", page_icon="🍺")

# Link direto para exportar a sua planilha como CSV
SHEET_URL = "https://docs.google.com/spreadsheets/d/1MVw8K8TwUmZPuS8F8rA4fnXFZQzN9nZB0vaUKemcICQ/export?format=csv"

st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; height: 3em; }
    .saldo-box { background-color: #333; padding: 30px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; }
    .stTextInput>div>div>input { text-align: center; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

def limpar_texto(txt):
    return re.sub(r'\D', '', str(txt)).strip()

st.title("🍺 CashChopp")
st.subheader("Consulte seu saldo de fidelidade")

cpf_digitado = st.text_input("Digite seu CPF (apenas números):")

if st.button("CONSULTAR MEU SALDO"):
    if not cpf_digitado:
        st.warning("Por favor, digite o seu CPF.")
    else:
        try:
            # Lê a planilha e remove espaços dos nomes das colunas
            df = pd.read_csv(SHEET_URL)
            df.columns = df.columns.str.strip().str.upper() # Garante que tudo vire NOME, CPF, SALDO
            
            busca = limpar_texto(cpf_digitado)
            
            # Cria uma lista de CPFs limpos para comparar
            df['CPF_LIMPO'] = df['CPF'].astype(str).apply(limpar_texto)
            
            # Procura o cliente
            cliente = df[df['CPF_LIMPO'] == busca]

            if not cliente.empty:
                res = cliente.iloc[0]
                nome = str(res['NOME']).split()[0]
                # Converte saldo tratando possíveis vírgulas da planilha
                saldo_str = str(res['SALDO']).replace(',', '.')
                saldo = float(saldo_str)
                
                st.markdown(f"### Olá, **{nome.upper()}**!")
                st.markdown(f"""
                    <div class="saldo-box">
                        <p style="font-size: 18px; color: #bbb;">Seu Saldo Disponível:</p>
                        <h1 style="margin: 0; font-size: 55px; color: #ffcc00;">R$ {saldo:.2f}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                if saldo > 0: st.balloons()
            else:
                st.error(f"CPF {cpf_digitado} não encontrado na base.")
        except Exception as e:
            st.error(f"Erro ao acessar a planilha: {e}")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
