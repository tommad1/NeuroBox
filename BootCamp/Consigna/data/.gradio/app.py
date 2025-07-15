import gradio as gr
import pandas as pd
import pickle
import os

# === Cargar modelo y configuraciones ===
MAIN_FOLDER = os.path.dirname(__file__)

# Modelo
MODEL_PATH = os.path.join(MAIN_FOLDER, "../model/modelo_proyecto_final.pickle")
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Columnas esperadas por el modelo
COLUMNS_PATH = os.path.join(MAIN_FOLDER, "../model/categories_ohe_without_fraudulent.pickle")
with open(COLUMNS_PATH, "rb") as f:
    ohe_tr = pickle.load(f)

# Bins
BINS_ORDER = os.path.join(MAIN_FOLDER, "../model/saved_bins_order.pickle")
with open(BINS_ORDER, 'rb') as handle:
    new_saved_bins_order = pickle.load(handle)

BINS_TRANSACTION = os.path.join(MAIN_FOLDER, "../model/saved_bins_transaction.pickle")
with open(BINS_TRANSACTION, 'rb') as handle:
    new_saved_bins_transaction = pickle.load(handle)

def predecir_fraude(orderAmount, orderState, paymentMethodRegistrationFailure,
                    paymentMethodType, paymentMethodProvider, paymentMethodIssuer,
                    transactionAmount, transactionFailed, emailDomain, emailProvider,
                    customerIPAddressSimplified, samecity, samestate):

    input_dict = {
        "orderAmount": float(orderAmount),
        "orderState": str(orderState),
        "paymentMethodRegistrationFailure": str(paymentMethodRegistrationFailure),
        "paymentMethodType": str(paymentMethodType),
        "paymentMethodProvider": str(paymentMethodProvider),
        "paymentMethodIssuer": str(paymentMethodIssuer),
        "transactionAmount": int(transactionAmount),
        "transactionFailed": str(transactionFailed).lower() in ["true", "1"],
        "emailDomain": str(emailDomain),
        "emailProvider": str(emailProvider),
        "customerIPAddressSimplified": str(customerIPAddressSimplified),
        "samecity": str(samecity),
        "samestate": str(samestate)
    }

    df = pd.DataFrame([input_dict])

    df["orderAmount"] = pd.cut(df["orderAmount"], bins=new_saved_bins_order, include_lowest=True)
    df["transactionAmount"] = pd.cut(df["transactionAmount"], bins=new_saved_bins_transaction, include_lowest=True)

    df_ohe = pd.get_dummies(df).reindex(columns=ohe_tr, fill_value=0)

    # ✅ DEBUG: Comprobar columnas generadas
    print("📌 Columnas generadas por get_dummies + reindex:")
    print(df_ohe.columns.tolist())

    print("📌 Columnas esperadas por el modelo:")
    print(ohe_tr)

    # Predicción
    probas = model.predict_proba(df_ohe)[0]
    pred = int(model.predict(df_ohe)[0])

    # Diccionario de salida
    tipo_fraude_map = {
    0: "False (No es fraude)",
    1: "True (Fraude confirmado)",
    2: "Warning (Transacción sospechosa)"
}


    return {
        "Tipo de fraude": tipo_fraude_map[pred],
        "Probabilidades": {
            "False": round(probas[0], 3),
            "True": round(probas[1], 3),
            "Warning": round(probas[2], 3)
        }
    }

# === Componentes Gradio ===
orderAmount = gr.Slider(0, 343, value=43.0, label="Order amount")
orderState = gr.Radio(["failed", "fulfilled", "pending"], label="Order state")
paymentMethodRegistrationFailure = gr.Radio(["True", "False"], label="Payment Method Registration Failure")
paymentMethodType = gr.Radio(["apple pay", "bitcoin", "card", "paypal"], label="Payment Method Type")
paymentMethodProvider = gr.Dropdown([
    "JCB 16 digit", "VISA 16 digit", "Voyager", "Diners Club / Carte Blanche",
    "Maestro", "VISA 13 digit", "Discover", "American Express", "JCB 15 digit", "Mastercard"
], label="Payment Method Provider")
paymentMethodIssuer = gr.Dropdown([
    "Citizens First Banks", "Solace Banks", "Vertex Bancorp", "His Majesty Bank Corp.",
    "Bastion Banks", "Her Majesty Trust", "Fountain Financial Inc.",
    "Grand Credit Corporation", "weird", "Bulwark Trust Corp.", "Rose Bancshares"
], label="Payment Method Issuer")
transactionAmount = gr.Slider(0, 343, value=43, label="Transaction amount")
transactionFailed = gr.Radio(["True", "False"], label="Transaction Failed", value="False")
emailDomain = gr.Radio(["com", "info", "org", "biz", "net", "weird"], label="Email Domain")
emailProvider = gr.Radio(["yahoo", "other", "gmail", "hotmail", "weird"], label="Email Provider")
customerIPAddressSimplified = gr.Radio(["digits_and_letters", "only_letters"], label="Customer IP Address")
samecity = gr.Radio(["yes", "no", "unknown"], label="Same city")
samestate = gr.Radio(["yes", "no", "unknown"], label="Same state")

# Botón de predicción + endpoint API
predict_btn = gr.Interface(
    fn=predecir_fraude,
    inputs=[
        orderAmount,
        orderState,
        paymentMethodRegistrationFailure,
        paymentMethodType,
        paymentMethodProvider,
        paymentMethodIssuer,
        transactionAmount,
        transactionFailed,
        emailDomain,
        emailProvider,
        customerIPAddressSimplified,
        samecity,
        samestate
    ],
    outputs="json",
    title="Detección de Fraude",
    description="Predice si una transacción es fraudulenta.",
    api_name="prediccion"
)

predict_btn.launch()
