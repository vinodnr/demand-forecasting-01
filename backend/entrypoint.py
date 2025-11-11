import os, sys, importlib, traceback

sys.path += ["/app", "/app/src"]
for mod in ["main", "src.api.main", "src.app.main"]:
    try:
        m = importlib.import_module(mod)
        if hasattr(m, "app"):
            os.execvp("uvicorn", ["uvicorn", f"{mod}:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except Exception:
        traceback.print_exc()
print("No FastAPI app found.")
