from sqlalchemy.orm.mapper import configure_mappers
from pos import create_app
from pos.extensions import db
from pos.user import User

app = create_app()


@app.cli.command("init_db")
def init_db():
    """
        Initialize/reset the database.
    """
    db.drop_all()
    configure_mappers()
    db.create_all()
    
    for i in range(10):
        user = User(
                username=f"User{i}",
                email=f"user-{i}@demo.fr",
                password="password"
            )
        db.session.add(user)

    db.session.commit()
