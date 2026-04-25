from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="Smart Academic Assistant API",
    description="Backend API for your Streamlit app",
    version="1.0.0"
)

# Enable CORS (important for Streamlit connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "FastAPI is running 🚀",
        "docs": "/docs"
    }

# Health check
@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }

# Example API endpoint
@app.get("/api/test")
def test():
    return {
        "message": "API working correctly"
    }

# Run server (for local + Render)
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)