from app.main import create_app
import uvicorn

if __name__ == "__main__":
    app = create_app()
    uvicorn.run("app.main:create_app", factory=True, reload=True, host="0.0.0.0", port=5070)