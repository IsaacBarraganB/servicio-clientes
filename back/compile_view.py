import os

import typer
from sqlalchemy import text

from project.infrastructure.repository import session as repository
from project.utils.general_utils import GeneralUtils

app = typer.Typer()


def register_view(view: str, name: str):
    try:
        with next(repository()) as session:
            session.execute(text(view))
            session.commit()
        print(f"Se creó la vista correctamente {name}")
    except Exception as error:
        session.rollback()
        print(f"Ocurrio un error al crear la vista {error} ")


@app.command()
def createview():
    PATH = "project/static/database"
    database = os.listdir(PATH)
    for name_view in database:
        view_database = GeneralUtils.load_file(
            os.path.abspath(PATH + "/" + name_view)
        )
        register_view(view_database, name_view)


if __name__ == "__main__":
    app()
