import requests;

url = "https://www.paguemenos.com.br/inalador-nebulizador-pague-menos-portatil-ultrassonico-mesh-nb1100/p?skuId=100141";

response = requests.get(url);

print(response.text);