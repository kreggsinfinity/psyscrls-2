import os
import requests
import json
import random
from pathlib import Path
from dotenv import load_dotenv

# Load credentials
load_dotenv()
API_KEY = os.getenv("POLLINATIONS_API_KEY")
AI_MODEL = "gemini-fast"
GEN_URL = "https://gen.pollinations.ai/v1/chat/completions"

# Paths
BASE_DIR = Path(__file__).parent
INSPIRATION_FILE = BASE_DIR / "psychologyscrolls.txt"
OUTPUT_FILE = BASE_DIR / "psychologyscrolls.txt"

THEMES = [
    "Attraction and Love Psychology",
    "Body Language Secrets",
    "Dark Psychology and Manipulation Tactics",
    "Facts about Human Behavior",
    "Male and Female Brain Differences",
    "Social Influence and Persuasion",
    "The Psychology of Success and Wealth",
    "Subconscious Mind and Habit Formation",
    "Emotional Intelligence and Resilience",
    "Relationships and Attachment Styles"
]

def get_inspiration_context():
    if not INSPIRATION_FILE.exists(): return ""
    with open(INSPIRATION_FILE, "r", encoding="utf-8") as f:
        # Read the full file to capture all nuances of the relationship advice
        return f.read()

def top_up_library(threshold=100, generate_count=200):
    """Checks the library and only generates if below threshold."""
    if not API_KEY:
        print("❌ Skip top-up: POLLINATIONS_API_KEY not found in environment.")
        return

    if not OUTPUT_FILE.exists():
        open(OUTPUT_FILE, 'w').close()
        
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        existing_quotes = [line.strip() for line in f if line.strip()]
    
    current_count = len(existing_quotes)
    print(f"📊 Current library size: {current_count}")

    if current_count >= threshold:
        print(f"✅ Library is still healthy (>= {threshold}). No new quotes needed today.")
        return

    print(f"⚠️ Library low ({current_count} < {threshold}). Generating {generate_count} new raw masculine insights...")
    
    context = get_inspiration_context()
    existing_lower = set(q.lower() for q in existing_quotes)
    
    batches_needed = (generate_count // 35) + 1
    new_total = 0

    for i in range(batches_needed):
        current_theme = random.choice(THEMES)
        print(f"🌀 Batch {i+1}: Generating psychology insights for '{current_theme}'...")
        
        prompt = f"""
        You are a world-class psychologist and behavior analyst specializing in viral social media content.
        Write 35 MIND-BLOWING, VIRAL, and DEEP psychology facts or insights about '{current_theme}'.
        
        STYLE GUIDELINES (BE EXACT):
        1. Tone: Intriguing, scientific yet accessible, and highly shareable. (Like a 'did you know' fact that reveals a secret about human nature).
        2. Format: 1-2 sentences. Short, punchy, "Twitter-style" but profound. 
        3. Core Logic: Focus on surprising statistics (e.g., '67% of people...'), hidden biological triggers, and actionable social hacks.
        
        EXAMPLES OF TARGET TONE:
        - "Couples who laugh together are 67% more likely to stay together."
        - "The '3-month rule' exists because that’s when infatuation chemicals fade, and real love begins."
        - "Writing about your anger reduces its intensity by 50%—it forces the brain to process emotion logically."
        - "Women's voices become higher-pitched when talking to someone they’re attracted to."
        
        REFERENCE CONTEXT FROM SOURCE FILE:
        {context[:2000]} # Limit context to avoid token bloat
        
        Return ONLY the insights, one per line. No numbers. No hashtags. No emojis.
        """

        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": AI_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 1.0}

        try:
            resp = requests.post(GEN_URL, headers=headers, json=payload, timeout=90)
            if resp.status_code == 200:
                content = resp.json()['choices'][0]['message']['content']
                lines = [q.strip() for q in content.split("\n") if q.strip() and len(q) > 40]
                
                added_this_batch = 0
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    for q in lines:
                        clean_q = q.lstrip('0123456789. ')
                        if clean_q.lower() not in existing_lower:
                            f.write(f"{clean_q}\n")
                            existing_lower.add(clean_q.lower())
                            added_this_batch += 1
                
                new_total += added_this_batch
                print(f"✅ Added {added_this_batch} new quotes.")
            else:
                print(f"❌ API Error: {resp.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")

    print(f"🎉 Top-up complete. Added {new_total} quotes. Total now: {len(existing_lower)}")

if __name__ == "__main__":
    top_up_library(threshold=100, generate_count=200)

