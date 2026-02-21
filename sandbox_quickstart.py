import os
from e2b import Sandbox
from dotenv import load_dotenv

load_dotenv()

e2b_api_key = os.environ.get("E2B_API_KEY")
if not e2b_api_key:
    raise RuntimeError("E2B_API_KEY is not set. Add it to .env or your shell environment.")

sandbox = Sandbox.create(api_key=e2b_api_key)
result = sandbox.commands.run('echo "Hello from E2B Sandbox!"')
print(result.stdout)