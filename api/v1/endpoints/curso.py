from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select  # Nessa versão fica dando warnings

from models.curso_model import CursoModel
from core.deps import get_session

# Bypass warnings SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
SelectOfScalar.inherit_cache = True  # type: ignore
# Fim Bypass

router = APIRouter()

# POST CURSO
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CursoModel
)
async def post_curso(
    curso: CursoModel, db: AsyncSession = Depends(get_session)
):
    novo_curso = CursoModel(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas,
    )

    db.add(novo_curso)
    await db.commit()

    return novo_curso


# GET CURSO
@router.get("/", response_model=List[CursoModel])
async def get_curso(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos
