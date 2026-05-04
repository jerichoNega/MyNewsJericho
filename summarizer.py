from google import genai
import os

class Summarizer:
    def __init__(self, api_key, model_name="gemini-flash-latest"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def summarize(self, entry, length="concise", language="English"):
        prompt = f"""
        Summarize the following news article for a WhatsApp newsletter.
        Target Language: {language}
        Style: {length} TL;DR (too long; didn't read)
        
        Source: {entry['source']}
        Title: {entry['title']}
        Content: {entry['summary']}
        
        Provide a concise summary that highlights the key point and its significance. 
        Start with a relevant emoji.
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error summarizing {entry['title']}: {e}")
            return f"Error generating summary for: {entry['title']}"
