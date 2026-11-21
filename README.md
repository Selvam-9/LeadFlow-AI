# LeadFlow AI

## Install dependencies on Windows

From PowerShell in this folder, run:

```powershell
.\setup.ps1
```

The script creates a local `.venv` and installs `requirements.txt`. It uses `uv` if available, so a separate `pip` command is not required. Otherwise, it uses an installed Python interpreter.

To start the API after setup, run this from PowerShell in the project folder:

```powershell
.\run.ps1
```

This uses the project's virtual environment directly, so you don't need to activate it or have `uvicorn` on your PATH. Additional Uvicorn options can be passed through, for example `.\run.ps1 --port 8001`.

The API documentation is available at <http://127.0.0.1:8000/docs>.
