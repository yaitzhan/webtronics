import logging

from webtronics.db.init_db import init_db
from webtronics.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    db = SessionLocal()
    init_db(db)


if __name__ == "__main__":
    main()
