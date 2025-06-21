from fastapi import FastAPI

app = FastAPI()

@app.get("/part/{username}")
def greet_user(username: str):
    return {"message": f"Hi {username.capitalize()}"}
