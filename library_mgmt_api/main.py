# main.py
from fastapi import FastAPI, Depends
from routes import router
from dependencies import get_supabase
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Include the router and pass the Supabase client
app.include_router(router, dependencies=[Depends(get_supabase)])

# Implement CORS to control allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://library-40ni.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
