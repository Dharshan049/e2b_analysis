import os
from e2b import Sandbox
from dotenv import load_dotenv

load_dotenv()

e2b_api_key = os.environ.get("E2B_API_KEY")
if not e2b_api_key:
    raise RuntimeError("E2B_API_KEY is not set.")

paginator = Sandbox.list(api_key=e2b_api_key)
sandboxes = []
while paginator.has_next:
    sandboxes.extend(paginator.next_items())

if len(sandboxes) == 0:
    print("No active sandboxes found.")
else:
    print(f"Found {len(sandboxes)} active sandbox(es):")
    for sb in sandboxes:
        print(f"- {sb.sandbox_id} | state={sb.state} | template={sb.template_id}")
