from openai import OpenAI

endpoint = "https://lucy-cs4371-openai.openai.azure.com/openai/v1"
deployment_name = "GameAgent"
api_key = "FWzQjpk70f4ueNeRcROVLBEJC5g8QOfgkM1mi3wMX3EC8JvBtaqgJQQJ99CDAC1i4TkXJ3w3AAABACOG8FVt"

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)

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
