import typer
from typing import Optional
from pubmed_paper_fetcher.fetcher import get_filtered_papers
import csv
from rich.console import Console
from rich.table import Table

from pubmed_paper_fetcher.models import Paper

app = typer.Typer()
console = Console()


def save_to_csv(papers: list[Paper], filename: str) -> None:
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID",
            "Title",
            "Publication Date",
            "Non-academic Author(s)",
            "Company Affiliation(s)",
            "Corresponding Author Email"
        ])
        writer.writeheader()
        for paper in papers:
            writer.writerow({
                "PubmedID": paper.pubmed_id,
                "Title": paper.title,
                "Publication Date": paper.publication_date,
                "Non-academic Author(s)": "; ".join(paper.non_academic_authors),
                "Company Affiliation(s)": "; ".join(paper.company_affiliations),
                "Corresponding Author Email": paper.corresponding_author_email or "N/A"
            })


def print_to_console(papers: list[Paper]) -> None:
    table = Table(title="PubMed Papers with Pharma Affiliations")

    table.add_column("PubmedID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Publication Date", style="green")
    table.add_column("Non-academic Authors", style="yellow")
    table.add_column("Companies", style="blue")
    table.add_column("Email", style="white")

    for paper in papers:
        table.add_row(
            paper.pubmed_id,
            paper.title,
            paper.publication_date,
            "; ".join(paper.non_academic_authors),
            "; ".join(paper.company_affiliations),
            paper.corresponding_author_email or "N/A"
        )

    console.print(table)


@app.command()
def main(
    query: str = typer.Argument(..., help="PubMed search query (quoted if multi-word)"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Filename to save CSV output")
):
    """Fetch PubMed papers with pharma/biotech affiliations."""
    console.print(f"🔍 Searching PubMed for: [bold]{query}[/bold]...", style="cyan")

    try:
        papers = get_filtered_papers(query, debug=debug)

        if not papers:
            console.print("⚠️  No papers found with non-academic pharma/biotech affiliations.", style="red")
            raise typer.Exit(code=1)

        if file:
            save_to_csv(papers, file)
            console.print(f"✅ Results saved to [green]{file}[/green]")
        else:
            print_to_console(papers)

    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
