
import requests

data = {
    "orderAmount" : 43.0,
    "orderState" : "fulfilled",
    "paymentMethodRegistrationFailure" : "False",
    "paymentMethodType" : "card",
    "paymentMethodProvider" : "Mastercard",
    "paymentMethodIssuer" : "Vertex Bancorp",
    "transactionAmount" : 43,
    "transactionFailed" : True,
    "emailDomain" : "com",
    "emailProvider" : "other",
    "customerIPAddressSimplified" : "only_letters",
    "samecity" : "no",
    "samestate": "no"
}
#probar desde localhost
response = requests.post("http://127.0.0.1:7860/prediccion", json=data)
#probar desde docker
#response = requests.post("http://ip172-18-0-78-d1go4tol2o90008mjka0-7860.direct.labs.play-with-docker.com/prediccion", json=data)
print(response.json())


