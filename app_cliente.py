import streamlit as st
import json
import os
import re

st.set_page_config(page_title="CashChopp - Meu Saldo", page_icon="🍺")

# Estilo Visual
st.markdown("<style>.main { background-color: #1a1a1a; } h1 { color: #ffcc00; text-align: center; } .saldo-box { background-color: #333; padding: 30px; border-radius: 15px; border: 2px solid #ffcc00; text-align: center; }</style>", unsafe_allow_html=True)

def limpar_cpf(txt):
    return re.sub(r'\D', '', str(txt))

def carregar_dados():
    caminho = 'banco_clientes_v6.json'
    if not os.path.exists(caminho): return {}
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except: return {}

st.title("🍺 CashChopp")
st.subheader("Consulte seu saldo")

cpf_digitado = st.text_input("Digite seu CPF (apenas números):")

if st.button("VER MEU SALDO"):
    dados = carregar_dados()
    busca = limpar_cpf(cpf_digitado)
    cliente = None

    # LÓGICA DE BUSCA DUPLA:
    # 1. Tenta achar o CPF como CHAVE do dicionário (Igual ao seu print)
    if busca in dados:
        cliente = dados[busca]
    else:
        # 2. Se não achou na chave, procura dentro dos dados (caso o CPF esteja lá)
        for chave, valor in dados.items():
            if isinstance(valor, dict):
                cpf_interno = limpar_cpf(valor.get('cpf', valor.get('CPF', '')))
                if cpf_interno == busca:
                    cliente = valor
                    break

    if cliente:
        nome = str(cliente.get('nome', 'Cliente')).split()[0]
        saldo = float(cliente.get('saldo', 0))
        
        st.markdown(f"### Olá, **{nome.upper()}**!")
        st.markdown(f"""<div class="saldo-box">
            <p style="font-size: 18px; color: #bbb;">Saldo Disponível:</p>
            <h1 style="font-size: 55px; color: #ffcc00;">R$ {saldo:.2f}</h1>
        </div>""", unsafe_allow_html=True)
        if saldo > 0: st.balloons()
    else:
        st.error("CPF não encontrado. Verifique se digitou corretamente.")