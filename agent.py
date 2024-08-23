import openai

def query_openai(prompt):
    openai.api_key = 'your-api-key'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
