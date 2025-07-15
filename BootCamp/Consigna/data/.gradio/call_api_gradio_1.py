from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
#client = Client("Tomas-Madriz/Proyecto_Fraude") probar desde huggingface
result = client.predict(
		orderAmount=43.0,
		orderState="fulfilled",
		paymentMethodRegistrationFailure="False",
		paymentMethodType="card",
		paymentMethodProvider="Mastercard",
		paymentMethodIssuer="Vertex Bancorp",
		transactionAmount=43,
		transactionFailed="True",
		emailDomain="com",
		emailProvider="weird",
		customerIPAddressSimplified="only_letters",
		samecity="no",
		samestate="no",
		api_name="/prediccion"
)
print(result)