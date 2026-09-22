from fastapi import Query, Body, APIRouter


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@router.get(
    "",
    summary="Получить данные об отелях",
    description="Тут может быть доп инфа"
)
def get_hotels(
    id: int | None = Query(None, description="Айдишник"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


#body, request body
@router.post(
    "",
    summary="Добавить данные об отеле"
)
def create_hotel(
        title : str = Body(embed=True)                                                              #embed делает json
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
    })
    return {"status" : "OK"}


@router.put(
    "/{hotel_id}",
    summary="Обновить данные об отеле"
)
def put_hotel(
        hotel_id: int,
        title : str = Body(embed=True),
        name : str = Body(embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status" : "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично обновить данные об отеле"
)
def patch_hotel(
        hotel_id: int,
        title : str | None = Body(None, embed=True),
        name : str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name:
                hotel["name"] = name
    return {"status" : "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удалить данные об отеле"
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
