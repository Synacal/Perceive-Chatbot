from fastapi import FastAPI
from app.api.api_v1.endpoints import (
    check_user_answer,
    answers,
    prior_art_search,
    attachments,
    ip_validity_analysis,
    requirements_gathering,
    common,
    quickprompt,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(requirements_gathering.router)
app.include_router(check_user_answer.router)
app.include_router(answers.router)
app.include_router(prior_art_search.router)
app.include_router(attachments.router)
app.include_router(ip_validity_analysis.router)
app.include_router(common.router)
app.include_router(quickprompt.router)
