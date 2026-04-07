import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="CashChopp - Meu Saldo", page_icon="🍺")

# Link da sua planilha
SHEET_ID = "1MVw8K8TwUmZPuS8F8rA4fnXFZQzN9nZB0vaUKemcICQ"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

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

st.title("🍺 CashChopp")
st.subheader("Consulte seu saldo de fidelidade")

cpf_input = st.text_input("Digite seu CPF (apenas números):")

if st.button("CONSULTAR MEU SALDO"):
    if not cpf_input:
        st.warning("Por favor, digite o CPF.")
    else:
        try:
            # Lê a planilha sem frescura
            df = pd.read_csv(SHEET_URL, dtype=str)
            busca = limpar(cpf_input)

            # --- LÓGICA POR POSIÇÃO (A=0, B=1, C=2) ---
            # Coluna 0 (A) deve ser o CPF
            # Coluna 1 (B) deve ser o NOME
            # Coluna 2 (C) deve ser o SALDO
            
            df['IDENTIFICADOR'] = df.iloc[:, 0].astype(str).apply(limpar)
            
            # Filtra todas as linhas desse CPF (caso haja duplicados)
            registros = df[df['IDENTIFICADOR'] == busca]

            if not registros.empty:
                # Soma o saldo de todas as ocorrências
                total_saldo = 0.0
                for _, row in registros.iterrows():
                    try:
                        # Pega o valor da terceira coluna (índice 2)
                        s = str(row.iloc[2]).replace(',', '.')
                        total_saldo += float(s)
                    except:
                        continue
                
                # Pega o nome na segunda coluna (índice 1)
                nome_completo = str(registros.iloc[0, 1]).upper()
                nome_exibir = nome_completo.split()[0]

                st.markdown(f"### Olá, **{nome_exibir}**!")
                st.markdown(f"""
                    <div class="saldo-box">
                        <p style="font-size: 18px; color: #bbb;">Seu Saldo Total:</p>
                        <h1 style="margin: 0; font-size: 55px; color: #ffcc00;">R$ {total_saldo:.2f}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                if total_saldo > 0:
                    st.balloons()
            else:
                st.error("CPF não encontrado na base de dados.")
        
        except Exception as e:
            st.error(f"Erro ao processar dados: {e}")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
