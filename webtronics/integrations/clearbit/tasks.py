from sqlalchemy.ext.asyncio import AsyncSession

import crud
from webtronics.integrations.clearbit.service import ClearbitClient


async def update_user_clearbit_data(
        db: AsyncSession,
        *,
        user_id: int,
        user_email: str
):
    client = ClearbitClient()

    clearbit_data = await client.get_person_user_data(email=user_email)

    if clearbit_data:
        additional_obj = await crud.user_additional.get_by_user_id(db=db, user_id=user_id)
        await crud.user_additional.update(db=db, db_obj=additional_obj, obj_in=clearbit_data)
        return additional_obj
