import sys
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():

    input_text = sys.argv[1]
    
    # Prompt OpenAI API for definition
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides clear, concise definitions of technical or scientific words, phrases, or concepts. Be as concise as possible. There is no need to repeat the word in the definition."},
                {"role": "user", "content": f"Define: {input_text}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        output_text = response.choices[0].message.content.strip()

        print(output_text)
        
    except Exception as e:
        print(f"Error getting definition: {str(e)}")

if __name__ == "__main__":
    main()
