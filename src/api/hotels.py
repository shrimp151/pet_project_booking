from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example

from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.schemas.hotels import HotelPatch, HotelAdd


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получить данные об отелях",
    description="Тут может быть дополнительная информация",
)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5

    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get(
    "/{hotel_id}",
    summary="Получить данные об отеле по id"
)
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary="Добавить данные о новом отеле",
)
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": Example(
        summary="Сочи",
        value={
            "title": "Отель Сочи 5 звезд у моря",
            "location": "Сочи, ул. Моря 1",
        },
    ),
    "2": Example(
            summary="Дубай",
            value={
                "title": "Отель Дубай у фонтана",
                "location": "Дубай, ул. Шейха 2",
            },
        )
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновить данные об отеле",
)
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удалить данные об отеле",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}
