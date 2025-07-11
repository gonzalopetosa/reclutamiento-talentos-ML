import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import joblib

ruta = Path('Curriculum-Vitae.csv').resolve()

df = pd.read_csv(ruta)


def normalizar_texto (texto):
    texto = str( texto ).lower()
    texto= re.sub(r'[*:(,&"]', '', texto)
    texto= re.sub(r'\\', ' ', texto)
    texto= re.sub(r'[/-]', ' ', texto)
    texto= re.sub(r'[â¢]', '', texto)
    return texto

puesto = df['Category'].apply(normalizar_texto)
informacion = df['Resume'].apply(normalizar_texto)

x_train, x_test, y_train, y_test = train_test_split(informacion, puesto, test_size=0.2, random_state=42, stratify = puesto)

vectorizador = TfidfVectorizer( max_features=5000 ,min_df=2 , max_df= 0.8)

X_train_vectorized = vectorizador.fit_transform(x_train)
X_test_vectorized = vectorizador.transform(x_test)

modelo_lr = LogisticRegression(max_iter=1000)
modelo_lr.fit(X_train_vectorized, y_train)

y_pred = modelo_lr.predict(X_test_vectorized)

joblib.dump( {'modelo': modelo_lr,
            'vectorizador': vectorizador},
            'lr_model_v1.joblib')