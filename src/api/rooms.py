from fastapi import APIRouter, Query
from datetime import date

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch


router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получить данные о комнатах определенного отеля",
)
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2026-08-01"),
        date_to: date = Query(example="2026-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получить данные о комнате определенного отеля",
)
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавить данные о новой комнате",
)
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Обновить данные о комнате",
)
async def put_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частично обновить данные о комнате",
)
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удалить данные о комнате",
)
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()

    return {"status": "OK"}
