import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

STATE_FILE = Path(".sandbox_id")


def get_sandbox_id() -> str:
    if not STATE_FILE.exists():
        raise RuntimeError(
            "No saved sandbox ID found. Run create_sandbox.py first to create and store one."
        )

    sandbox_id = STATE_FILE.read_text(encoding="utf-8").strip()
    if not sandbox_id:
        raise RuntimeError(".sandbox_id exists but is empty.")
    return sandbox_id


def connect_sandbox() -> Sandbox:
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        raise RuntimeError("E2B_API_KEY is not set. Add it to .env or your environment.")

    sandbox_id = get_sandbox_id()
    return Sandbox.connect(sandbox_id=sandbox_id, api_key=api_key)


def cmd_upload(sandbox: Sandbox, local_path: str, remote_path: str) -> None:
    source = Path(local_path)
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"Local file not found: {source}")

    data = source.read_bytes()
    sandbox.files.write(remote_path, data)
    print(f"Uploaded {source} -> {remote_path}")


def cmd_download(sandbox: Sandbox, remote_path: str, local_path: str) -> None:
    content = bytes(sandbox.files.read(remote_path, format="bytes"))
    destination = Path(local_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(content)
    print(f"Downloaded {remote_path} -> {destination}")


def cmd_read(sandbox: Sandbox, remote_path: str) -> None:
    content = sandbox.files.read(remote_path, format="text")
    print(content)


def cmd_list(sandbox: Sandbox, remote_dir: str, depth: int) -> None:
    entries = sandbox.files.list(remote_dir, depth=depth)
    if not entries:
        print("No entries found.")
        return

    for entry in entries:
        print(f"{entry.type}\t{entry.path}\t{entry.size}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run file operations on an existing E2B sandbox using saved sandbox ID."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    upload = sub.add_parser("upload", help="Upload local file to sandbox path")
    upload.add_argument("local_path")
    upload.add_argument("remote_path")

    download = sub.add_parser("download", help="Download sandbox file to local path")
    download.add_argument("remote_path")
    download.add_argument("local_path")

    read = sub.add_parser("read", help="Read remote file as text")
    read.add_argument("remote_path")

    ls = sub.add_parser("list", help="List files in remote directory")
    ls.add_argument("remote_dir")
    ls.add_argument("--depth", type=int, default=2)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    sandbox = connect_sandbox()

    if args.command == "upload":
        cmd_upload(sandbox, args.local_path, args.remote_path)
    elif args.command == "download":
        cmd_download(sandbox, args.remote_path, args.local_path)
    elif args.command == "read":
        cmd_read(sandbox, args.remote_path)
    elif args.command == "list":
        cmd_list(sandbox, args.remote_dir, args.depth)
    else:
        parser.error("Unknown command")


if __name__ == "__main__":
    main()