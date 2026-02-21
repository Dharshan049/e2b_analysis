# E2B Learning Playground

This repo is a step-by-step learning setup for working with E2B sandboxes, file operations, LLM-generated code execution, function calling, package installation, and streaming.

## 1) Setup

Install local dependencies:

```powershell
pip install -r requirements.txt
```

This includes E2B SDKs (`e2b`, `e2b-code-interpreter`) plus `python-dotenv` and `groq`.

Create `.env`:

```env
E2B_API_KEY=your_e2b_key
GROQ_API_KEY=your_groq_key
```

## 2) Create and persist one sandbox

Script: `create_sandbox.py`

```powershell
python .\create_sandbox.py
```

What it does:
- Creates one E2B sandbox
- Stores sandbox ID in `.sandbox_id`
- Other scripts reconnect using that same ID

## 3) File operations in the same sandbox

Script: `file_ops.py`

Examples:

```powershell
python .\file_ops.py upload main.py /tmp/main.py
python .\file_ops.py read /tmp/main.py
python .\file_ops.py download /tmp/main.py downloaded_main.py
python .\file_ops.py list /tmp --depth 2
```

## 4) LLM -> generate Python -> run in same sandbox

Script: `llm_sandbox_test.py`

```powershell
python .\llm_sandbox_test.py
```

Flow:
- Send prompt to Groq
- Get Python code
- Execute code in the sandbox from `.sandbox_id`

## 5) Function calling (prime tool)

Script: `llm_function_call_test.py`

```powershell
python .\llm_function_call_test.py
python .\llm_function_call_test.py "I need prime numbers up to 200"
```

Flow:
- Model can call `get_primes_up_to(n)` tool
- Script executes tool locally and returns tool output
- Model returns final response

## 6) Install custom packages in sandbox

Script: `sandbox_install_package.py`

```powershell
python .\sandbox_install_package.py
```

Notes:
- Installs package inside E2B sandbox (not local machine)
- Uses `sandbox.commands.run("pip install ...")`

## 7) Check sandbox Python + installed packages

Script: `sandbox_env_info.py`

```powershell
python .\sandbox_env_info.py
```

Shows:
- `python --version` in sandbox
- `pip list` in sandbox

## 8) Streaming execution output

Script: `sandbox_streaming_demo.py`

```powershell
python .\sandbox_streaming_demo.py
```

Shows callback-based streaming:
- `on_stdout`
- `on_stderr`
- `on_result`
- `on_error`

## Useful helpers

- `sandbox_listing.py` -> list active sandboxes
- `sandbox_deletion.py` -> close active sandboxes
- `sandbox_quickstart.py` -> simple one-shot sandbox example

## Common issues

- Missing API keys: ensure `.env` contains `E2B_API_KEY` and `GROQ_API_KEY`
- Missing `.sandbox_id`: run `python .\create_sandbox.py`
- Expired sandbox: run `python .\create_sandbox.py` again to create a fresh one