import typer

from check_type import check_type
from database import engine, get_db
from get_urls import get_urls
from models import Item
from scraper import scrape_data
from item_service import ItemService
import os

app = typer.Typer()

Item.metadata.create_all(bind=engine)

if not os.path.exists("data"):
    os.mkdir("data")


@app.command()
def scrape() -> None:
    urls = get_urls()

    for k, v in urls.items():
        _type = check_type(v)
        scrape_data(k, v)


@app.command()
def scrape_by_url(
        url: str
) -> None:
    _type = check_type(url)
    scrape_data(_type, url)


@app.command()
def export_to_json(
        start_page: int = typer.Option(1, min=1),
        page_limit: int = typer.Option(50, min=1)
) -> None:
        session = next(get_db())
        ItemService(session).export_to_json(start_page, page_limit)


if __name__ == "__main__":
    app()
