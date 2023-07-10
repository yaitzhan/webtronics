from sqlalchemy.ext.asyncio import AsyncSession

from webtronics import crud
from webtronics.integrations.emailhunt.service import EmailHuntClient


async def update_user_email_hunt_data(
        db: AsyncSession,
        *,
        user_id: int,
        user_email: str
):
    client = EmailHuntClient()

    email_hunt_data = await client.verify_user_email(email=user_email)

    if email_hunt_data:
        additional_obj = await crud.user_additional.get_by_user_id(db=db, user_id=user_id)
        await crud.user_additional.update(db=db, db_obj=additional_obj, obj_in=email_hunt_data)
        return additional_obj
