# PubMed Paper Fetcher

Fetch and filter PubMed research papers based on a user-defined query, specifically identifying papers with at least one **non-academic** author affiliated with **pharmaceutical or biotech companies**.

> 🧠 This tool was developed with the help of **OpenAI ChatGPT** to streamline the development and ensure correctness across asynchronous programming, API integration, and CLI design.

---

## 🧩 Project Structure

pubmed_paper_fetcher/
│
├── init.py
├── models.py # Pydantic models for Paper and Author
├── fetcher.py # Core logic to search PubMed, fetch articles, and parse results
├── cli.py # Typer-based CLI application
│
├── README.md
├── pyproject.toml # Poetry project configuration
├── result.csv # Sample output file


## ⚙️ Installation & Usage

### 📦 Prerequisites

- Python 3.10+
- Poetry (recommended): https://python-poetry.org/docs/#installation

### 🚀 Setup

1. **Clone the repository**

git clone https://github.com/SushanParlapally/Aganitha-python-test.git
cd pubmed-paper-fetcher

Install dependencies

poetry install

usage CLI COMMANDS : poetry run get-papers-list "your pubmed query" -f output.csv

Example command :  poetry run get-papers-list "biotech cancer therapy" -f result.csv --debug



📚 Libraries & Tools Used

Tool/Library	                               Purpose                     	                                         Link

requests	                             To perform HTTP requests	                                 https://pypi.org/project/requests/
xmltodict	                             For parsing PubMed XML responses	                         https://pypi.org/project/xmltodict/
pydantic	                             For structured data models and validation	                 https://docs.pydantic.dev/
typer	                                 For building the command-line interface	                 https://typer.tiangolo.com/
rich	                                 For formatting CLI output	                                 https://pypi.org/project/rich/
twine	                                 For publishing the module to PyPI	                         https://pypi.org/project/twine/
pytest	                                 For testing (development only)	                             https://docs.pytest.org/
OpenAI ChatGPT	                         LLM used to develop, refactor, and validate the tool        https://chat.openai.com/


Repository & Package
GitHub Repository: https://github.com/SushanParlapally/Aganitha-python-test.git
testtPyPI  Package:https://test.pypi.org/project/pubmed-paper-fetcher-xuyhan07-test01/0.1.0/