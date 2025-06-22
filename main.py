import os
import json
import logging
import sys
from groq import Groq
from dotenv import load_dotenv
import argparse

#Load environment variables from .env file
load_dotenv()

# Set logging level based on environment variable
log_level = os.getenv("LOG_LEVEL", "ERROR")

# Configure logging
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jargon.log'),  # Log to file
        logging.StreamHandler(sys.stderr)   # Also log to stderr
    ]
)

logger = logging.getLogger(__name__)

# Initialize OpenAI client for Groq API
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_json_file(filepath: str) -> dict:
    """Load prompts or configs from specified JSON file"""
    logger.debug(f"Loading JSON file: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            logger.debug(f"Successfully loaded {filepath}")
            return data
        
    except FileNotFoundError as e:
        logger.error(f"JSON file not found: {filepath}")
        raise e

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        raise e
    
    except Exception as e:
        logger.error(f"Unexpected error loading {filepath}: {e}")
        raise e 

def get_term() -> str:
    """Get input text from command line and capitalize"""
    
    parser = argparse.ArgumentParser(description='Get definition of a word or phrase')
    parser.add_argument('text', help='The word or phrase to define')
    args = parser.parse_args()
    term = args.text

    logger.debug(f"Input term: '{term}'")

    # Check if input is text (not empty and contains non-whitespace characters)
    if not term or not term.strip():
        logger.error("Empty input provided")
        raise ValueError("Input text cannot be empty")

    # Capitalize first letter if not already capitalized
    if not term[0].isupper():
        term = term.capitalize()
        logger.debug(f"Capitalized term: '{term}'")
            
    return term
    
def main():
    try:
        logger.info("Starting jargon definition lookup")
        
        # Load prompts configuration
        prompts = load_json_file('prompts.json')
        
        # Load generation configuration
        config = load_json_file('config.json')

        # Get input text from command line
        term = get_term()
        
        logger.debug(f"Looking up definition for: {term}")
        
        # Prompt Groq API for definition
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
        logger.info("Successfully retrieved definition")
    
        #Format and print output 
        print(f"{term} - {definition}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)  # exc_info=True adds stack trace
        raise e

if __name__ == "__main__":
    main()
