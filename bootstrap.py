from sqlalchemy.orm.mapper import configure_mappers
from pos import create_app
from pos.extensions import db

app = create_app()


@app.cli.command("init_db")
def init_db():
    """
        Initialize/reset the database.
    """
    db.drop_all()
    configure_mappers()
    db.create_all()