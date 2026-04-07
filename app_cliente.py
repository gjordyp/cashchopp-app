import streamlit as st
import pandas as pd
import re

# 1. Configuração da página
st.set_page_config(page_title="CashChopp - Meu Saldo", page_icon="🍺")

# 2. Link da sua Planilha (Formatado para exportação CSV)
SHEET_ID = "1MVw8K8TwUmZPuS8F8rA4fnXFZQzN9nZB0vaUKemcICQ"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# 3. Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; }
    h3 { color: #ffffff; text-align: center; }
    .stButton>button { width: 100%; background-color: #ffcc00; color: black; font-weight: bold; border-radius: 10px; height: 3em; border: none; }
    .saldo-box { background-color: #333; padding: 30px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; margin-top: 20px; }
    .stTextInput>div>div>input { text-align: center; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

def limpar_cpf(txt):
    return re.sub(r'\D', '', str(txt))

# 4. Função para carregar dados direto do Google Sheets
def carregar_dados_online():
    try:
        # Lê a planilha usando o Pandas
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com a planilha: {e}")
        return None

st.title("🍺 CashChopp")
st.subheader("Consulte seu saldo de fidelidade")

cpf_digitado = st.text_input("Digite seu CPF (apenas números):", placeholder="Ex: 05220962396")

if st.button("CONSULTAR MEU SALDO"):
    if not cpf_digitado:
        st.warning("Por favor, digite o seu CPF.")
    else:
        df = carregar_dados_online()
        if df is not None:
            # Limpa o CPF digitado e os CPFs da planilha para comparar
            busca = limpar_cpf(cpf_digitado)
            
            # Ajusta os nomes das colunas para minúsculo para evitar erro
            df.columns = [str(col).lower().strip() for col in df.columns]
            
            # Procura o cliente (ajuste 'cpf' se o nome da coluna for outro na planilha)
            # Criamos uma coluna temporária limpa para a busca
            df['cpf_limpo'] = df['cpf'].astype(str).apply(limpar_cpf)
            cliente = df[df['cpf_limpo'] == busca]

            if not cliente.empty:
                # Pega os dados da primeira linha encontrada
                dados = cliente.iloc[0]
                nome = str(dados['nome']).split()[0]
                saldo = float(dados['saldo'])
                
                st.markdown(f"### Olá, **{nome.upper()}**!")
                st.markdown(f"""
                    <div class="saldo-box">
                        <p style="font-size: 18px; color: #bbb; margin-bottom: 5px;">Seu Saldo Disponível:</p>
                        <h1 style="margin: 0; font-size: 55px; color: #ffcc00;">R$ {saldo:.2f}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                if saldo > 0:
                    st.balloons()
            else:
                st.error("CPF não encontrado na base do Google Sheets.")
        else:
            st.error("Não foi possível acessar a planilha agora.")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
