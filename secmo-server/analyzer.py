import re
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()


# Preprocessing function for cleaning and structuring logs
def preprocess_logs(raw_logs):
    """
    Cleans raw logs by removing irrelevant information
    and structuring them for better analysis.
    """
    cleaned_logs = re.sub(r'(INFO|DEBUG|TRACE|ERROR|WARNING):', '', raw_logs)
    return cleaned_logs.strip()

# Function to call the OpenAI API to analyze logs
def analyze_logs(logs):
    """
    Sends preprocessed logs to GPT-4 for threat intelligence analysis.
    """
  
    prompt = f"""
    You are a cybersecurity expert. Analyze the following logs and identify any potential security threats.
    For each threat, provide:
    1. A description of the threat.
    2. A risk score from 1 to 10 (where 10 is highest).
    3. Recommended mitigation strategies.
    
    And return it as a string representation of a styled html tabled report that is beautiful for email report in a mono font, scores should be colored depending on risk level.

    Logs:
    {logs}
    """

    client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=1000,
    temperature=0.5,  # Adjust temperature for more deterministic output
    n=1
)
   
    
    
    # Update to access the correct attribute
    return chat_completion.choices[0].message.content;

# Function to generate a threat intelligence report
def generate_threat_report(raw_logs):
        
    #Preprocess logs
    cleaned_logs = preprocess_logs(raw_logs)
    if cleaned_logs:
        report = analyze_logs(cleaned_logs)
        print("Threat Intelligence Report:")
        return report.replace('```html','').replace('```','')
    else:
        print("No critical logs to analyze.")
        return "No critical logs to analyze."
