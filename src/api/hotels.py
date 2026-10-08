from fastapi import Query, APIRouter, Body
from fastapi.openapi.models import Example
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получить данные об отелях",
    description="Тут может быть доп инфа",
)
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)

        hotels = result.scalars().all()
        return hotels

    # if pagination.page and pagination.per_page:
    #     return hotels_[(pagination.page-1) * pagination.per_page:pagination.page * pagination.per_page]


@router.post(
    "",
    summary="Добавить данные об отеле",
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Обновить данные об отеле",
)
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле",
)
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удалить данные об отеле",
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
