from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from preprocessing import selecionar_comentario, extrair_features_manuais

class ValidateCommentRequestDto(BaseModel):
    comment: str    

class ValidateCommentResponseDto(BaseModel):
    isOffensive: bool    

model = joblib.load("ai.joblib")

app = FastAPI()

origins = [
] # TODO: configure cors properly using env variables

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/validate-comment")
async def validate_comment(request: ValidateCommentRequestDto):
    if not request.comment:
        return Response(content={"erro": "Campo 'comentario' é obrigatório"}, media_type="application/json", status_code=400)

    df = pd.DataFrame({"comentario": [request.comment]})
    pred = model.predict(df)[0]
    return ValidateCommentResponseDto(isOffensive=bool(pred))
