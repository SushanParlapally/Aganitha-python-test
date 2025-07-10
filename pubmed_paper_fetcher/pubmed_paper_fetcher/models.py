from typing import List, Optional
from pydantic import BaseModel, Field

class Author(BaseModel):
    name: str
    affiliation: Optional[str] = None
    is_non_academic: bool = False
    is_pharma_or_biotech: bool = False

class Paper(BaseModel):
    pubmed_id: str = Field(..., alias="PubmedID")
    title: str = Field(..., alias="Title")
    publication_date: str = Field(..., alias="Publication Date")
    non_academic_authors: List[str] = Field(default_factory=list, alias="Non-academic Author(s)")
    company_affiliations: List[str] = Field(default_factory=list, alias="Company Affiliation(s)")
    corresponding_author_email: Optional[str] = Field(None, alias="Corresponding Author Email")

    model_config = {
        "populate_by_name": True
    }