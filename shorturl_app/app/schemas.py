from pydantic import BaseModel, HttpUrl

class UrlCreate(BaseModel):
    url: HttpUrl

class UrlResponse(BaseModel):
    short_id: int
    full_url: HttpUrl
    short_url: str
