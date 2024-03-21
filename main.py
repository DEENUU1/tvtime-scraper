import typer

from database import engine
from database import get_db
from get_urls import get_urls
from item_service import ItemService
from models import Item
from scraper import scrape_data

app = typer.Typer()

Item.metadata.create_all(bind=engine)


@app.command()
def scrape() -> None:
    urls = get_urls()

    for k, v in urls.items():
        _type = None
        if k.endswith("s"):
            _type = "Show"
        if k.endswith("m"):
            _type = "Movie"

        scrape_data(k, v)


@app.command()
def get_items() -> None:
    db = next(get_db())
    _service = ItemService(db)

    print(_service.get_all())


if __name__ == "__main__":
    app()
