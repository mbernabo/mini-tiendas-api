import json

# Cadena JSON con caracteres Unicode escapados
json_string = "{\"id\": 6, \"name\": \"La Verduler\\u00eda\", \"description\": \"Tienda de respuestos\", \"user_id\": 1}"

# Decodificar la cadena JSON para recuperar los caracteres especiales
decoded_string = json_string.encode('utf-8').decode('unicode_escape')

# Convertir la cadena decodificada a un diccionario
data = json.loads(json_string)

# Imprimir el diccionario con los caracteres especiales
print(data)
