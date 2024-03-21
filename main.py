import typer

from check_type import check_type
from database import get_db
from get_urls import get_urls
import scraper
from item_service import ItemService
from init_app import init_app

app = typer.Typer()
init_app()


@app.command()
def scrape_list() -> None:
    urls = get_urls()

    for k, v in urls.items():
        _type = check_type(v)
        scraper.scrape_data(k, v)


@app.command()
def scrape_list_by_url(
        url: str
) -> None:
    _type = check_type(url)
    scraper.scrape_data(_type, url)


@app.command()
def scrape_details() -> None:
    items = ItemService(next(get_db())).get_all_details_not_found()
    for item in items:
        scraper.scrape_details(item.url)


@app.command()
def export_to_json(
        start_page: int = typer.Option(1, min=1),
        page_limit: int = typer.Option(50, min=1)
) -> None:
        _session = next(get_db())
        ItemService(_session).export_to_json(start_page, page_limit)


if __name__ == "__main__":
    app()
