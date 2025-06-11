from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import FunctionTransformer, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re
import numpy as np
import pandas as pd
import string

# Lista de palavras ofensivas (usa sua lista aqui)
palavras_ofensivas = [
    "lixo", "escória", "verme", "praga", "desgraçado", "miserável", "nojento", "podre",
    "retardado", "imbecil", "idiota", "estúpido", "animal", "burro", "anta", "jumento",
    "cavalo", "porco", "canalha", "safado", "safada", "vagabundo", "vagabunda", "pilantra",
    "corrupto", "corrupta", "ladrão", "ladra", "traidor", "traidora", "mentiroso", "mentirosa",
    "ridículo", "ridícula", "escroto", "escrota", "otário", "otária", "frouxo", "frouxa",
    "covarde", "infeliz", "fracassado", "fracassada", "babaca", "palhaço", "palhaça", "inútil",
    "maldito", "maldita", "peste", "satânico", "satânica", "condenado", "condenada", "marginal",
    "marginalzinha", "canalhice", "escrotice", "idiota do caralho", "filho da puta", "filha da puta",
    "vai tomar no cu", "vai se foder", "vai pra puta que pariu", "pau no cu", "arrombado",
    "arrombada", "corno", "corna", "chifrudo", "chifruda", "desgraça", "diabo", "satanás",
    "inferno", "malparido", "puta", "puto", "vagabunda de merda", "bosta", "bosta seca",
    "escória humana", "racista", "fascista", "comunista safado", "esquerdopata", "bolsominion",
    "petralha", "feminazi", "viadinho", "sapatão", "traveco", "macaco", "favelado", "analfabeto",
    "imundo", "ignorante", "nojenta"
]
# Função para extrair features manuais
def extrair_features_manuais(df):
    def conta(t):
        palavras = t.split()
        qtd_palavras = len(palavras)
        qtd_caracteres = len(t)
        qtd_maiusculas = sum(1 for p in palavras if p.isupper())
        qtd_exclamacoes = t.count("!")
        qtd_pontuacoes = sum(1 for c in t if c in string.punctuation)
        qtd_ofensivas = sum(1 for p in palavras if re.sub(r"[^\w\s]", "", p.lower()) in palavras_ofensivas)
        comeca_com_ofensiva = int(re.sub(r"[^\w\s]", "", palavras[0].lower()) in palavras_ofensivas) if qtd_palavras > 0 else 0
        contem_ofensiva = int(any(palavra in t.lower() for palavra in palavras_ofensivas))
        return [
            qtd_caracteres, qtd_palavras, qtd_maiusculas, qtd_exclamacoes,
            qtd_pontuacoes, qtd_ofensivas, comeca_com_ofensiva, contem_ofensiva
        ]
    return np.array([conta(t) for t in df["comentario"]])


# Criar pipeline de TF-IDF + features manuais
def selecionar_comentario(x):
    return x["comentario"]
    