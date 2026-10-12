from sqlalchemy import select, func

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
            query = select(HotelsOrm)
            if location:
                query = query.where(func.lower(HotelsOrm.location).contains(location.strip().lower()))
            if title:
                query = query.where(func.lower(HotelsOrm.title).contains(title.strip().lower()))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )
            result = await self.session.execute(query)

            return result.scalars().all()
