import sys
import os
import json
from groq import Groq
from dotenv import load_dotenv
import argparse

#Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client for Groq API
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

def get_term() -> str:
    """Get input text from command line and capitalize"""

    parser = argparse.ArgumentParser(description='Get definition of a word or phrase')
    parser.add_argument('text', help='The word or phrase to define')
    args = parser.parse_args()
    term = args.text
    

    # Check if input is text (not empty and contains non-whitespace characters)
    if not term or not term.strip():
        print("Error: Input text cannot be empty")
        sys.exit(1)

    # Capitalize first letter if not already capitalized
    if not term[0].isupper():
        term = term.capitalize()
            
    return term
    
def main():

    # Load prompts configuration
    prompts = load_json_file('prompts.json')
    
    # Load generation configuration
    config = load_json_file('config.json')

    # Get input text from command line
    term = get_term()
    
    # Prompt OpenAI API for definition
    try:
        response = client.chat.completions.create(
            model=config['model']['value'],
            messages=[
                {"role": "system", "content": prompts['system']['prompt']},
                {"role": "user", "content": f"Define: {term}"}
            ],
            max_tokens=config['max_tokens']['value'],
            temperature=config['temperature']['value'],
            stream=config['stream']['value']
        )
        
        definition = response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error getting definition: {str(e)}")
    
    #Format and print output 
    print(f"{term} - {definition}")

if __name__ == "__main__":
    main()
