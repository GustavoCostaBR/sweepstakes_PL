# import requests

# # Specify the form ID or URL
# form_id = "1evCwfGX7yXPw9bNwvBouGzYTw2a7JNqRH3LmehFzBss"

# # Specify your authentication credentials
# api_key = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCnGyKbtpBhr6ix\n33LtSBgrw2hlh7qW8XhW+AlZJoVL8ixK030wMfdYVWCfesSi+JxGWV6V+KUdSDcx\nRoU4OOgYFzB7zQCE+uNT/Zs1kKybxBmSnKNJBq6ueM6peqJHauQdElLNIHOiROZY\nMPNOTOM2SeWjWvDdBNqTkFTQ2KniMA1Gfm9RHjeB3re+Rdg8TRjZ/eG3LdpcR602\nLXu51mjUaEiyT4TcE9+3D8DfDB3UwaFgz3/EkAVOmhhJNAg2JhkVyn4G13sskqMo\nAlyV2eDkH4TcNx3/W2ZC37Kc7qEfk8zsHqEFFizA2e6Kz4b43cB5rNLi45BwsUhJ\nu7Kz//exAgMBAAECggEAIIwpubv9k7VHzXtY8mv2H0IEebAN0PwPxRqzEWzuDgyJ\ngXp/We2FgGxCsVVTau2y3IXoJRxEprcr3tpeNMTqudR8ckSL2xrVv8R34F9BK2au\n125QZHcbe2qW0A5NgM0KSLpKq97r/tleJyPDpAbYQ3jxtBdQri/VlePJDVOCBUan\nn7Y/g8Xx+WQjXYPs/6Vv0l6iTadSqn8zZ9m+lxLWide0zXKuM0iuDEX4RigZXWxA\nGVdv9035ADwfQVXt5cEfBrXeHO6mlJLS3qE/by7HK8j1RfO7AYN36Lh6ORvCThxL\nweU+HmsdTsDkJjd8Y8YeObghkYW0cox52tRkh2C/9QKBgQDRRL9U0M2yp7/3+UMz\nsTDy0+HhDRcpvDCr7CaV49JceGuaygsssJ8v8DaDWYxmLQF/QWxshdrBloQ4Ppn5\nwDaPDna46VtnoKhf7+6yYvbcvAwz1Dg6Ipcy2GEJDn5raeFkHUhtEuou2ppKdrNR\nk5NwVLsbGz+cslSLOXmzm6O6/QKBgQDMbBT3J0j/kDBz5cZU1RrivMiIxgNUilUl\n60SamjpD7cIyA1TzwkngiXbVV5Cfn6fqiaYfqMgKRZAG2WCmExVFwQQGHkGrlfRk\nQD3wolbnPuQFJiidp3XKnRTTtfUfYDgwwoC1CcwX2oCU624yfhLJABnB5QahJWR8\nnrM7K5FPxQKBgQDLP94k3ngqYMsOaUZf2mUUM75a+n/YxTLwh/gh9JfHwB2ixUF9\nMj4qLUCE6mB2jJe7pStNa+Q/yZS5m/Oooota/k1I4z0ntN5T75ECKSRi1zFy1VeW\n/ymi9I2qYi1e3gNPXTGO3qQcxay9TfRz8sVsgJ8JgLmT05BReI0/aJbpcQKBgBpm\nmw6QdE0NQjS1qDesjhxaZUvExwlUFEshZ2rQIFZFjp8G7yHMJd5p4n8LIBJ9fCI+\nRMYx9iPdeAxqZqEMNeMcWnivz6tpYnbQFS/Ox4p2BNzlYLl7tyrDvrzY8x9qPdeO\nRzEaYtFx1slk3oaG4cYzzR/NhF2rhp7RoDQ0HEBBAoGAWftmt06eCFFdyeok8G3K\n4dYo5WH9lh/0BVUBBSkfPooC8zbog4eYpfDLA4LmgJyEXSk9PgqZNv/ZmHKwswg2\nBeBEXtPFljdAYBXWmF2ZHCtOkrPyR83s5wyBBNAY95eyGxbFOGa4zPbO102XJFth\nmZTRUIiKi1O1BdaVeg/a1BI="

# # Make the API request
# response = requests.get(
#     f"https://www.googleapis.com/forms/v1/forms/{form_id}",
#     params={"key": api_key}
# )

# # Check the response status code
# if response.status_code == 200:
#     # Form data retrieved successfully
#     form_data = response.json()
#     form_body = form_data["responseDestination"]["destinationId"]
#     print("Form Body:", form_body)
# else:
#     # Error occurred
#     print("Error:", response.status_code, response.text)

from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret_882267232515-nci02jnbt3d7h80fi196o16rht6vujii.apps.googleusercontent.com.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

# Prints the title of the sample form:
form_id = '1dW0_Astat5WM_4gVmGkmKaNtKFOKduJl7RO-awXuB2k'
result = service.forms().get(formId=form_id).execute()
print(result)


