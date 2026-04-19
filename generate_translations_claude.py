import os
import json
import time
from anthropic import Anthropic

# ====================== CONFIG ======================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")   # Set this!

# Languages you want
TARGET_LANGUAGES = ["de", "cs", "sk", "pl", "hu"]

INPUT_FILE = "translations.json"      # Your base English file (the one I gave you)
OUTPUT_FILE = "translations_full.json"

client = Anthropic(api_key=ANTHROPIC_API_KEY)

def translate_with_claude(keys_dict, target_lang):
    """Translate a batch of strings using Claude - best quality for your use case"""
    prompt = f"""You are a professional translator for MedTech and Biotech startup SaaS products.
Translate the following English UI strings, function names, descriptions, buttons, and AI outcomes into natural, professional, founder-friendly {target_lang}.

- Keep technical terms like "Health Score", "Pitch Readiness", "Regulatory Crystal Ball" in English if they are proper module names.
- Make descriptions and outcomes sound natural and motivating.
- Return ONLY a valid JSON object with the exact same keys.

Keys to translate:
{json.dumps(keys_dict, indent=2, ensure_ascii=False)}
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2500,
            temperature=0.1,
            system="You are an expert technical translator for startup tools. Prioritize clarity, professionalism, and natural flow in the target language.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text.strip()
        # Extract JSON safely
        start = text.find('{')
        end = text.rfind('}') + 1
        json_str = text[start:end]
        return json.loads(json_str)
        
    except Exception as e:
        print(f"Claude error for {target_lang}: {e}")
        return {}

def main():
    if not ANTHROPIC_API_KEY:
        print("Error: Please set your ANTHROPIC_API_KEY environment variable.")
        return

    # Load base English
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        base = json.load(f)

    full_translations = {"en": base.get("en", base)}

    print("Starting Claude-powered translation for your full app...\n")

    for lang in TARGET_LANGUAGES:
        print(f"Translating to {lang}...")

        translated = translate_with_claude(base["en"], lang)
        
        full_translations[lang] = translated
        time.sleep(2)  # Be respectful to the API

    # Save the result
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(full_translations, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Translation completed!")
    print(f"   Saved to: {OUTPUT_FILE}")
    print(f"   Languages included: {list(full_translations.keys())}")
    print("\nYou can now use this file in your app.")

if __name__ == "__main__":
    main()