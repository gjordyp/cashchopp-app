import streamlit as st
import pandas as pd
import re

# 1. Configuração Básica
st.set_page_config(page_title="CashChopp - Meu Saldo", page_icon="🍺")

# Link da sua planilha (ID: 1MVw8K8TwUmZPuS8F8rA4fnXFZQzN9nZB0vaUKemcICQ)
# O final "&gid=0" garante que ele pegue a primeira aba da planilha
SHEET_ID = "1MVw8K8TwUmZPuS8F8rA4fnXFZQzN9nZB0vaUKemcICQ"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. Estilo Visual (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #1a1a1a; }
    h1 { color: #ffcc00; text-align: center; font-weight: bold; }
    h3 { color: #ffffff; text-align: center; }
    .stButton>button { 
        width: 100%; 
        background-color: #ffcc00; 
        color: black; 
        font-weight: bold; 
        border-radius: 10px; 
        height: 3em; 
        border: none;
    }
    .saldo-box { 
        background-color: #333; 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #ffcc00; 
        text-align: center; 
        margin-top: 20px; 
    }
    .stTextInput>div>div>input { text-align: center; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

def limpar_texto(txt):
    # Remove tudo que não for número e espaços sobrando
    return re.sub(r'\D', '', str(txt)).strip()

st.title("🍺 CashChopp")
st.subheader("Consulte seu saldo de fidelidade")

# Campo de CPF
cpf_digitado = st.text_input("Digite seu CPF (apenas números):", placeholder="Ex: 05220962396")

if st.button("CONSULTAR MEU SALDO"):
    if not cpf_digitado:
        st.warning("Por favor, digite o seu CPF.")
    else:
        try:
            # Lendo a planilha (forçando as colunas CPF e NOME como texto)
            df = pd.read_csv(SHEET_URL, dtype=str)
            
            # Limpando nomes das colunas (tira espaços e deixa em maiúsculo)
            df.columns = [str(c).strip().upper() for c in df.columns]
            
            # Prepara a busca
            busca = limpar_texto(cpf_digitado)
            
            # Cria coluna de comparação na planilha (limpa pontos e traços)
            if 'CPF' in df.columns:
                df['CPF_LIMPO'] = df['CPF'].apply(limpar_texto)
                
                # Procura o cliente exato
                cliente = df[df['CPF_LIMPO'] == busca]

                if not cliente.empty:
                    res = cliente.iloc[0]
                    nome_completo = str(res['NOME']).upper()
                    primeiro_nome = nome_completo.split()[0]
                    
                    # Converte o saldo para número (tratando vírgula ou ponto)
                    try:
                        saldo_raw = str(res['SALDO']).replace(',', '.')
                        saldo_final = float(saldo_raw)
                    except:
                        saldo_final = 0.0
                    
                    st.markdown(f"### Olá, **{primeiro_nome}**!")
                    st.markdown(f"""
                        <div class="saldo-box">
                            <p style="font-size: 18px; color: #bbb; margin-bottom: 5px;">Seu Saldo Disponível:</p>
                            <h1 style="margin: 0; font-size: 55px; color: #ffcc00;">R$ {saldo_final:.2f}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    if saldo_final > 0:
                        st.balloons()
                else:
                    st.error(f"CPF {cpf_digitado} não encontrado na base.")
                    # Ajuda para entender o erro
                    with st.expander("🔍 Detalhes da Busca (Ajuda)"):
                        st.write("Colunas lidas na planilha:", list(df.columns))
                        st.write("Primeiro CPF da lista:", df['CPF_LIMPO'].iloc[0] if not df.empty else "Vazio")
            else:
                st.error("A coluna 'CPF' não foi encontrada na planilha. Verifique o nome na linha 1.")

        except Exception as e:
            st.error(f"Erro ao conectar com os dados: {e}")

st.markdown("---")
st.caption("Fidelidade CashChopp - São Luís/MA")
