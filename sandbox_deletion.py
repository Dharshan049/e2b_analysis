import os
from e2b import Sandbox
from dotenv import load_dotenv

load_dotenv()

e2b_api_key = os.environ.get("E2B_API_KEY")
if not e2b_api_key:
    raise RuntimeError("E2B_API_KEY is not set.")

# List existing sandboxes (paginated)
paginator = Sandbox.list(api_key=e2b_api_key)
sandboxes = []
while paginator.has_next:
    sandboxes.extend(paginator.next_items())

if len(sandboxes) == 0:
    print("No active sandboxes found.")
else:
    print(f"Found {len(sandboxes)} active sandbox(es).")

    for sb in sandboxes:
        sb_id = sb.sandbox_id
        print(f"Closing sandbox: {sb_id}")
        killed = Sandbox.kill(sb_id, api_key=e2b_api_key)
        if killed:
            print(f"Sandbox {sb_id} closed.")
        else:
            print(f"Sandbox {sb_id} was already gone.")
