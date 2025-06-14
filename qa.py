import requests

def answer_with_context(question, context):
    prompt = f"Answer the question based on the context below:\n\nContext:\n{context}\n\nQuestion: {question}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    response_json = response.json()
    return response_json.get("response", "No answer generated.")
