import sys
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

#Load environment variables from .env file
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_json_file(filepath: str) -> dict:
    """Load prompts or configs from specified JSON file"""

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
        
    except FileNotFoundError:
        print(f"Error: {filepath} file not found")
        sys.exit(1)

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        sys.exit(1)

def main():

    # Load prompts configuration
    prompts = load_json_file('prompts.json')
    
    # Load generation configuration
    config = load_json_file('config.json')

    # Get input text from command line
    input_text = sys.argv[1]
    
    # Prompt OpenAI API for definition
    try:
        response = client.chat.completions.create(
            model=config['model']['value'],
            messages=[
                {"role": "system", "content": prompts['system']['prompt']},
                {"role": "user", "content": f"Define: {input_text}"}
            ],
            max_tokens=config['max_tokens']['value'],
            temperature=config['temperature']['value']
        )
        
        output_text = response.choices[0].message.content.strip()

        print(output_text)
        
    except Exception as e:
        print(f"Error getting definition: {str(e)}")

if __name__ == "__main__":
    main()
