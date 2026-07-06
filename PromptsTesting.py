"""
Prompt Engineering Experiment
------------------------------
Interactively runs prompts entered by the user through the OpenRouter API
(Gemini 2.5 Flash Lite). Type 'exit' at the prompt to stop.

"""

import textwrap
from openai import OpenAI

API_KEY = "private api key is inserted here"
MODEL = "google/gemini-2.5-flash-lite"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)


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
    results = []  # list of (prompt_text, output) tuples, in order entered

    print("Prompt Engineering Experiment")
    print("Type your prompt and press Enter. Type 'exit' to quit.\n")

    while True:
        prompt_text = input("Enter your prompt: ").strip()

        if prompt_text.lower() == "exit":
            break

        if not prompt_text:
            print("Please enter a prompt, or type 'exit' to quit.\n")
            continue

        try:
            output = run_prompt(prompt_text)
        except Exception as e:
            output = f"[ERROR calling API: {e}]"

        results.append((prompt_text, output))

        print("\nRESPONSE:")
        print(textwrap.fill(output, width=80))
        print()

    # --------------------------------------------------------------
    # Save everything to a markdown file
    # --------------------------------------------------------------
    if results:
        out_file = "prompt_experiment_results.md"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write("# Prompt Engineering Experiment Results\n\n")
            f.write(f"Model used: `{MODEL}`\n\n")
            for i, (prompt_text, output) in enumerate(results, start=1):
                f.write(f"## Prompt {i}\n\n")
                f.write(f"**Prompt:**\n> {prompt_text}\n\n")
                f.write(f"**Response:**\n\n{output}\n\n")
                f.write("---\n\n")

        print(f"All {len(results)} result(s) saved to {out_file}")
    else:
        print("No prompts were run, nothing to save.")


if __name__ == "__main__":
    main()
