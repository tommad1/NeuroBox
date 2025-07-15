from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
		orderAmount=18.0,
		orderState="pending",
		paymentMethodRegistrationFailure="True",
		paymentMethodType="card",
		paymentMethodProvider="JCB 16 digit",
		paymentMethodIssuer="Citizens First Banks",
		transactionAmount=18,
		transactionFailed="False",
		emailDomain="com",
		emailProvider="yahoo",
		customerIPAddressSimplified="only_letters",
		samecity="yes",
		samestate="yes",
		api_name="/prediccion"
)
print(result)