from google import generativeai as genai


class Gemini(object):
    def __init__(self, api_key :str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="You are a blonde kindly and sweet hero, your name is Alice",
        )

    def send(self, text :str) -> str:
        resp = self.model.generate_content(text)
        return resp.text if resp else ''
