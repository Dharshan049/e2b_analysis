# pip install e2b-code-interpreter python-dotenv
import os
from pathlib import Path

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

sandbox_id = Path(".sandbox_id").read_text(encoding="utf-8").strip()
sandbox = Sandbox.connect(sandbox_id=sandbox_id, api_key=os.environ["E2B_API_KEY"])

py = sandbox.commands.run("python --version")
print("Python version in sandbox:")
print(py.stdout or py.stderr)

pkgs = sandbox.commands.run("pip list")
print("Installed packages in sandbox:")
print(pkgs.stdout)
if pkgs.stderr:
    print(pkgs.stderr)