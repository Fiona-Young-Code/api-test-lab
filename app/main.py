from fastapi import FastAPI


app = FastAPI(title="API Test Lab")


@app.get("/health")
def health_check():
    """Return the current service status."""
    return {
        "status": "ok"
    }