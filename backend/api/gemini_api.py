from fastapi import APIRouter, Cookie, Request, HTTPException
from sqlalchemy import select

from backend.gemini_client import get_answer_from_gemini
from backend.database.database import session_dep
from backend.database.hash import security
from backend.schemas.gemini_schema import GetAIAnswerShema
from backend.models.models import ChatRequest, UserModel

router = APIRouter()


@router.post('/send_prompt', tags=['AI'])
async def send_prompt(data: GetAIAnswerShema, session: session_dep, token: str = Cookie(...)):

    if not token:
        raise HTTPException(status_code=401, detail='No token')

    payload = security._decode_token(token)
    user_id = int(payload.sub)

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    answer = get_answer_from_gemini(data.prompt)

    new_request_data = ChatRequest(
        user_id=user_id,      
        prompt=data.prompt,
        answer=answer
        )

    session.add(new_request_data)
    await session.commit()   

    return {'gemini': answer}


@router.get('/get_current_requests', tags=['AI'])
async def get_my_requests(session: session_dep, token: str = Cookie(...)):

    if not token:
        raise HTTPException(status_code=401, detail='No token')

    payload = security._decode_token(token)
    user_id = int(payload.sub)

    query = await session.execute(select(UserModel).where(UserModel.id == user_id))
    current_user = query.scalar_one_or_none()

    if not current_user:
        raise HTTPException(status_code=404, detail='User not found')

    query_prompt = await session.execute(select(ChatRequest).where(ChatRequest.user_id == user_id))
    info_for_current_user = query_prompt.scalars().all()

    return {'your_prompts': info_for_current_user}