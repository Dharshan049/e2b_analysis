# pip install e2b-code-interpreter python-dotenv
import os
from pathlib import Path

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

sandbox_id = Path(".sandbox_id").read_text(encoding="utf-8").strip()
sandbox = Sandbox.connect(sandbox_id=sandbox_id, api_key=os.environ["E2B_API_KEY"])

package = "cowsay"  # change this package name
install = sandbox.commands.run(f"pip install {package}")
print(install.stdout)
print(install.stderr)

execution = sandbox.run_code("import cowsay; cowsay.cow('Hello from E2B')")
print(execution.text)
if execution.logs.stdout:
    print("".join(execution.logs.stdout))