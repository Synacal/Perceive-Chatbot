from fastapi import FastAPI
from app.api.api_v1.endpoints import check_user_answer, answers, prior_art_search
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(check_user_answer.router)
app.include_router(answers.router)
app.include_router(prior_art_search.router)