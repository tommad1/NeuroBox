import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os


# Cargar modelo
MAIN_FOLDER = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MAIN_FOLDER, "../model/modelo_proyecto_final.pickle")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Cargar columnas esperadas
COLUMNS_PATH = os.path.join(MAIN_FOLDER, "../model/categories_ohe_without_fraudulent.pickle")
with open(COLUMNS_PATH, "rb") as f:
    ohe_tr = pickle.load(f)

# Cargar bins
BINS_ORDER = os.path.join(MAIN_FOLDER, "../model/saved_bins_order.pickle")
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

BINS_TRANSACTION = os.path.join(MAIN_FOLDER, "../model/saved_bins_transaction.pickle")
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)


# App FastAPI
app = FastAPI(title="Predicción de Fraude")

class FraudInput(BaseModel):
    orderAmount: float
    orderState: str
    paymentMethodRegistrationFailure: str
    paymentMethodType: str
    paymentMethodProvider: str
    paymentMethodIssuer: str
    transactionAmount: int
    transactionFailed: bool
    emailDomain: str
    emailProvider: str
    customerIPAddressSimplified: str
    samecity: str
    samestate: str

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido al API de Detección de Fraude"}

@app.post("/prediccion")
def predict_fraud_customer(input_data: FraudInput):
    input_dict = input_data.dict()
    single_instance = pd.DataFrame.from_dict([input_dict])

    # Aplicar bins
    single_instance["orderAmount"] = pd.cut(
        single_instance["orderAmount"].astype(float),
        bins=new_saved_bins_order,
        include_lowest=True
    )

    single_instance["transactionAmount"] = pd.cut(
        single_instance["transactionAmount"].astype(int),
        bins=new_saved_bins_transaction,
        include_lowest=True
    )

    # One-hot encoding
    single_instance_ohe = pd.get_dummies(single_instance).reindex(columns=ohe_tr, fill_value=0)

    # Predicción
    prediction = int(model.predict(single_instance_ohe)[0])
    probas = model.predict_proba(single_instance_ohe)[0]

    
    # Diccionario de significados
    tipo_fraude_map = {
        0: "False (No es fraude)",
        1: "True (Fraude confirmado)",
        2: "Warning (Transacción sospechosa)"
    }

    return {
        "Tipo de fraude": prediction,
        "Significado": tipo_fraude_map[prediction],
        "Probabilidades": {
            "False": round(probas[0], 3),
            "True": round(probas[1], 3),
            "Warning": round(probas[2], 3)
        }
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7860, reload=True)
