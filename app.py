"""
StockMind AI Server Entrypoint Alias
"""

from main import app

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    reload = os.environ.get("ENV", "production") == "development"
    uvicorn.run("main:app", host=host, port=port, reload=reload)
