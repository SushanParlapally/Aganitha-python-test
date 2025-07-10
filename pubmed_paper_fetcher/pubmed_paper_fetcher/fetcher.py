import requests
import xmltodict
from typing import List, Optional
from .models import Paper, Author
import re

PUBMED_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

COMMON_PHARMA_KEYWORDS = ["pharma", "biotech", "therapeutics", "laboratories", "genomics", "biosciences", "lifesciences", "medtech", "inc.", "corp"]
def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(PUBMED_ESEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]
def fetch_pubmed_details(pubmed_ids: List[str]) -> List[dict]:
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }
    response = requests.get(PUBMED_EFETCH_URL, params=params)
    response.raise_for_status()
    parsed = xmltodict.parse(response.content)
    return parsed["PubmedArticleSet"]["PubmedArticle"]
def is_non_academic(affiliation: str) -> bool:
    affiliation_lower = affiliation.lower()
    if "university" in affiliation_lower or "college" in affiliation_lower or "institute" in affiliation_lower:
        return False
    return True
def is_pharma_company(affiliation: str) -> bool:
    return any(keyword in affiliation.lower() for keyword in COMMON_PHARMA_KEYWORDS)
def extract_email(affiliation: str) -> Optional[str]:
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", affiliation)
    return match.group(0) if match else None
def parse_article(article: dict) -> Optional[Paper]:
    try:
        article_meta = article["MedlineCitation"]["Article"]
        pubmed_id = article["MedlineCitation"]["PMID"]["#text"] if isinstance(article["MedlineCitation"]["PMID"], dict) else article["MedlineCitation"]["PMID"]
        title = article_meta["ArticleTitle"]
        pub_date = article_meta.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
        publication_date = "-".join(filter(None, [pub_date.get("Year"), pub_date.get("Month"), pub_date.get("Day")])) or "N/A"

        author_list = article_meta.get("AuthorList", {}).get("Author", [])
        if isinstance(author_list, dict):
            author_list = [author_list]

        non_academic_authors = []
        company_affiliations = []
        email_found = None

        for author in author_list:
            affiliation_info = author.get("AffiliationInfo", [])
            if isinstance(affiliation_info, dict):
                affiliation_info = [affiliation_info]

            for aff in affiliation_info:
                affiliation = aff.get("Affiliation", "")
                if not affiliation:
                    continue

                if is_non_academic(affiliation):
                    name = f"{author.get('LastName', '')} {author.get('ForeName', '')}".strip()
                    non_academic_authors.append(name)

                if is_pharma_company(affiliation):
                    company_affiliations.append(affiliation)

                if not email_found:
                    email_found = extract_email(affiliation)

        if not non_academic_authors or not company_affiliations:
            return None

        return Paper(
            pubmed_id=pubmed_id,
            title=title,
            publication_date=publication_date,
            non_academic_authors=non_academic_authors,
            company_affiliations=company_affiliations,
            corresponding_author_email=email_found
        )
    except Exception as e:
        print(f"[ERROR] Skipping article due to error: {e}")
        return None
def get_filtered_papers(query: str, max_results: int = 20, debug: bool = False) -> List[Paper]:
    ids = search_pubmed(query, max_results=max_results)
    articles = fetch_pubmed_details(ids)

    papers = []
    for article in articles:
        paper = parse_article(article)
        if paper:
            if debug:
                print(f"[DEBUG] Included: {paper.title}")
            papers.append(paper)

    return papers
