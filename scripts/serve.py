"""Start the local FastAPI extraction API."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("market.api:app", host="127.0.0.1", port=8000, reload=False)
