import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from e2b_code_interpreter import Sandbox

load_dotenv()

api_key = os.environ["GROQ_API_KEY"]
e2b_api_key = os.environ["E2B_API_KEY"]
sandbox_id = Path(".sandbox_id").read_text(encoding="utf-8").strip()

# Create Groq client
client = Groq(api_key=api_key)
system_prompt = "You are a helpful assistant that can execute python code in a Jupyter notebook. Only respond with the code to be executed and nothing else. Strip backticks in code blocks."
prompt = "hey create me a code to for printing the prime number upto 100'"

# Send the prompt to the model
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ],
)

# Extract the code from the response
code = (response.choices[0].message.content or "").strip()
if code.startswith("```"):
    code = code.strip("`\n ")
if code.lower().startswith("python\n"):
    code = code.split("\n", 1)[1]

# Execute code in the same E2B Sandbox (reusing saved sandbox ID)
sandbox = Sandbox.connect(sandbox_id=sandbox_id, api_key=e2b_api_key)
execution = sandbox.run_code(code)

result = execution.text
if result is None and execution.logs.stdout:
    result = "".join(execution.logs.stdout).strip()

print(result)