import json
import pandas as pd
import requests
import streamlit as st


# Configurações Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"

# Carregar Dados

perfil = json.load(open('./data/perfil_investidor.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))


# Contexto

contexto = f'''
CLIENTE: {perfil["nome"]}, {perfil["idade"]} anos, profissão: {perfil["perfil_investidor"]}
OBJETIVO: {perfil["objetivo_principal"]}
PATRIMONIO: R$ {perfil["patrimonio_total"]} | RESERVA: R$ {perfil["reserva_emergencia_atual"]}

TRANSACOES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONIVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
'''

# System Prompt
system_prompt = f'''
Você é um assistente virtual amigável e didático.
OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples usando os dados do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos específicos, apenas explique como funcionam.
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais.
    Quando acontecer, responda: "Desculpe, não posso ajudar com isso."
- USE os dados do cliente para contextualizar suas explicações.
- USE Linguaguem simples e acessível, evitando jargões técnicos.
- Seja empático e encorajador, reconhecendo o esforço do cliente em aprender.
- Se não souber algo, admita: "Não sei a resposta para isso, mas posso ajudar com outros conceitos de finanças pessoais."
- Sempre pergunte se o cliente entendeu;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
'''
# Chamar Ollama


def perguntar(msg):
    prompt = f'''
    {system_prompt}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}'''

    r = requests.post(OLLAMA_URL, json={
                      "model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']


# Interface


st.title("Assistente Virtual de Finanças Pessoais")

if pergunta := st.chat_input("Faça sua pergunta sobre finanças pessoais:"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
