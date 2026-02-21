import os
from pathlib import Path

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

STATE_FILE = Path(".sandbox_id")
DEFAULT_TIMEOUT_SECONDS = 60 * 30


def main() -> None:
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        raise RuntimeError("E2B_API_KEY is not set. Add it to .env or your environment.")

    sandbox = Sandbox.create(api_key=api_key, timeout=DEFAULT_TIMEOUT_SECONDS)
    STATE_FILE.write_text(sandbox.sandbox_id, encoding="utf-8")

    print(f"Sandbox created: {sandbox.sandbox_id}")
    print(f"Saved sandbox ID to: {STATE_FILE}")
    print("Use file_ops.py to upload/download/read/list files in this same sandbox.")


if __name__ == "__main__":
    main()