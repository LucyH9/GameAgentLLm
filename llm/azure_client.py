import os
from openai import OpenAI


class AzureLLMClient:
    def __init__(self, endpoint=None, api_key=None, deployment_name=None):
        #Load Azure OpenAI settings from arguments or environment variables.
        self.endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = deployment_name or os.getenv("AZURE_OPENAI_DEPLOYMENT")

        #Raise an error if any required configuration value is missing.
        if not self.endpoint:
            raise ValueError("Missing Azure OpenAI endpoint.")
        if not self.api_key:
            raise ValueError("Missing Azure OpenAI API key.")
        if not self.deployment_name:
            raise ValueError("Missing Azure OpenAI deployment name.")

        #Create the OpenAI client for Azure requests.
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.api_key
        )

    def get_chat_response(self, prompt, system_message="You are a helpful assistant."):
        #Send a chat completion request to the Azure OpenAI deployment.
        completion = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )

        #Return only the text content of the model's reply.
        return completion.choices[0].message.content