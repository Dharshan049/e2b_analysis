# pip install e2b-code-interpreter python-dotenv
import os
from pathlib import Path

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

sandbox_id = Path(".sandbox_id").read_text(encoding="utf-8").strip()
sandbox = Sandbox.connect(sandbox_id=sandbox_id, api_key=os.environ["E2B_API_KEY"])

code = """
import time
import sys

print('step 1: stdout')
time.sleep(1)
print('step 2: stderr', file=sys.stderr)
time.sleep(1)
print('step 3: stdout')

x = 2 + 3
x
"""


def on_stdout(msg):
    print(f"[stdout] {msg.line}", end="")


def on_stderr(msg):
    print(f"[stderr] {msg.line}", end="")


def on_result(result):
    if result.text is not None:
        print(f"[result] {result.text}")


def on_error(err):
    print(f"[error] {err.name}: {err.value}")


execution = sandbox.run_code(
    code,
    on_stdout=on_stdout,
    on_stderr=on_stderr,
    on_result=on_result,
    on_error=on_error,
)

if execution.error:
    print("Execution finished with error.")
else:
    print("Execution finished.")