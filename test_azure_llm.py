#Import the OpenAI client library.
from openai import OpenAI

#Azure OpenAI endpoint for this deployment.
endpoint = "https://lucy-cs4371-openai.openai.azure.com/openai/v1"

#Name of the deployed model in Azure.
deployment_name = "GameAgent"

#API key for Azure OpenAI.
api_key = "FWzQjpk70f4ueNeRcROVLBEJC5g8QOfgkM1mi3wMX3EC8JvBtaqgJQQJ99CDAC1i4TkXJ3w3AAABACOG8FVt"

#Create the client used to send requests to Azure OpenAI.
client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)


#Send a simple test prompt to verify the model responds correctly.
completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": 'Reply with exactly this JSON and nothing else: {"move": 3}'
        }
    ],
)

print(completion.choices[0].message.content)
