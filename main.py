import sys
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompts():
    """Load prompts from prompts.json file"""
    try:
        with open('prompts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: prompts.json file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in prompts.json")
        sys.exit(1)

def load_config():
    """Load configuration from config.json file"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: config.json file not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json")
        sys.exit(1)

def main():

    # Load prompts configuration
    prompts = load_prompts()
    
    # Load generation configuration
    config = load_config()

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
