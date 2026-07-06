"""
Prompt Engineering Experiment
------------------------------
Runs the same task ("write an email requesting a deadline extension")
through 5 prompts of increasing quality, using OpenRouter + Gemini 2.5 Flash Lite.

"""

import textwrap
from openai import OpenAI

API_KEY = "private api key is inserted here"  
MODEL = "google/gemini-2.5-flash-lite"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# ------------------------------------------------------------------
# 2. The prompts (same task but different wording)
# ------------------------------------------------------------------
PROMPTS = {
    "1. Basic": (
        "Write an email asking for a deadline extension in 120 words."
    ),
    "2. Improved": (
        "Write a polite email to my professor asking for a 3-day extension "
        "on my assignment because I am sick. Keep it 120 words."
    ),
    "3. Detailed": (
        "You are a university student writing to your professor. Write a "
        "polite, respectful email requesting a 3-day extension on your Data "
        "Structures assignment due to a documented illness. Mention that you "
        "have already completed 70 percent of the work and will submit as soon as "
        "possible. Keep it in the range of 120 words."
    ),
    "4. Creative": (
        "Write a warm, empathetic email from a student to a professor, asking "
        "for an extension on an assignment due to illness, using a genuine "
        "and heartfelt tone. Feel free to add a metaphor about how illness "
        "slowed down your progress. Keep it in the range of 120 words."
    ),
    "5. Constrained": (
        "You are a university student. Write a formal email to your "
        "professor requesting a 3-day extension on your assignment due to "
        "illness. Keep it in the range of 120 words. use a professional tone, and "
        "include a clear subject line. "
    ),
}

# ------------------------------------------------------------------
# 3. Colors to highlighting each prompt's output 
# ------------------------------------------------------------------
COLORS = {
    "1. Basic": "\033[91m",        # red
    "2. Improved": "\033[93m",     # yellow
    "3. Detailed": "\033[92m",     # green
    "4. Creative": "\033[95m",     # magenta
    "5. Constrained": "\033[96m",  # cyan
}
RESET = "\033[0m"
BOLD = "\033[1m"


def run_prompt(prompt_text: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt_text}],
        temperature=0.7,
        max_tokens=250,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stream=False,
    )
    return response.choices[0].message.content.strip()


def main():
    results = {}

    for label, prompt_text in PROMPTS.items():
        color = COLORS.get(label, "")

        print(f"\n{color}{BOLD}{'=' * 70}")
        print(label)
        print(f"{'=' * 70}{RESET}")
        print(f"{color}PROMPT:{RESET} {prompt_text}\n")

        try:
            output = run_prompt(prompt_text)
        except Exception as e:
            output = f"[ERROR calling API: {e}]"

        results[label] = output
        print(f"{color}RESPONSE:{RESET}")
        print(textwrap.fill(output, width=80))
        print()

    # --------------------------------------------------------------
    # 4. Save everything to a markdown file
    # --------------------------------------------------------------
    out_file = "prompt_experiment_results.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# Prompt Engineering Experiment Results\n\n")
        f.write(f"Model used: `{MODEL}`\n\n")
        for label, prompt_text in PROMPTS.items():
            f.write(f"## {label}\n\n")
            f.write(f"**Prompt:**\n> {prompt_text}\n\n")
            f.write(f"**Response:**\n\n{results[label]}\n\n")
            f.write("---\n\n")

    print(f"{BOLD}All 5 results saved to {out_file}{RESET}")


if __name__ == "__main__":
    main()
