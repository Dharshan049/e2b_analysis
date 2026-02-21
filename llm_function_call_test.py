# pip install groq
import argparse
import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def primes_up_to(n: int) -> list[int]:
    print("Using this tool")
    primes = []
    for num in range(2, n + 1):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes


def parse_n_from_failed_generation(err: Exception) -> int | None:
    body = getattr(err, "body", None)
    if not isinstance(body, dict):
        return None

    fg = body.get("error", {}).get("failed_generation")
    if not isinstance(fg, str):
        return None

    match = re.search(r'"n"\s*:\s*(\d+)', fg)
    if match:
        return int(match.group(1))

    match = re.search(r'n\s*=\s*(\d+)', fg)
    if match:
        return int(match.group(1))

    return None


parser = argparse.ArgumentParser(description="Simple function-calling test")
parser.add_argument("prompt", nargs="*", help="Prompt for the assistant")
args = parser.parse_args()

prompt = " ".join(args.prompt) if args.prompt else "I need prime numbers up to 200"

client = Groq(api_key=os.environ["GROQ_API_KEY"])
model = "llama-3.3-70b-versatile"

messages = [{"role": "user", "content": prompt}]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_primes_up_to",
            "description": "Return all prime numbers from 2 up to n (inclusive).",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer", "description": "Upper limit"}
                },
                "required": ["n"],
            },
        },
    }
]

try:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    assistant_msg = response.choices[0].message
    messages.append(
        {
            "role": "assistant",
            "content": assistant_msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in (assistant_msg.tool_calls or [])
            ],
        }
    )

    if assistant_msg.tool_calls:
        for tc in assistant_msg.tool_calls:
            if tc.function.name == "get_primes_up_to":
                params = json.loads(tc.function.arguments or "{}")
                n = int(params.get("n", 0))
                result = {"n": n, "primes": primes_up_to(n)}

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    }
                )

        final_response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        print(final_response.choices[0].message.content)
    else:
        print(assistant_msg.content)

except Exception as err:
    n = parse_n_from_failed_generation(err)
    if n is None:
        raise

    result = {"n": n, "primes": primes_up_to(n)}
    print(json.dumps(result, indent=2))