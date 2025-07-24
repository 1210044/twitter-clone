from src.models.media_model import Media
from src.schemas.media_schema import MediaCreate, MediaUpdate
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository
from src.config.database.db_helper import db_helper


class MediaRepository(SqlAlchemyRepository[Media, MediaCreate, MediaUpdate]):
    pass


media_repository = MediaRepository(model=Media, db_session=db_helper.get_db_session)