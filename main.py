import typer

from config.database import get_db
from scrapers import scrape_details, scrape_list
from services.item_service import ItemService
from utils.check_type import check_type
from utils.get_urls import get_urls
from utils.init_app import init_app

app = typer.Typer()
init_app()
session = next(get_db())


@app.command()
def list_scraper() -> None:
    """
    Scrape list of items from URLs.
    """
    urls = get_urls()
    for k, v in urls.items():
        _type = check_type(v)
        scrape_list.scrape_list(session, _type, v)


@app.command()
def list_scraper_url(
        url: str
) -> None:
    """
    Scrape list of items from a single URL.

    Args:
        url (str): URL to scrape.
    """
    _type = check_type(url)
    scrape_list.scrape_list(session, _type, url)


@app.command()
def details_scraper() -> None:
    """
    Scrape details for all items.
    """
    items = ItemService(next(get_db())).get_all_details_not_found()
    for item in items:
        scrape_details.scrape_details(session, item.url)


@app.command()
def export_to_json(
        start_page: int = typer.Option(1, min=1),
        page_limit: int = typer.Option(50, min=1)
) -> None:
    """
    Export items to JSON files.

    Args:
        start_page (int): Start page number.
        page_limit (int): Number of items per page.

    Returns:
        None
    """
    ItemService(session).export_to_json(start_page, page_limit)


if __name__ == "__main__":
    app()
