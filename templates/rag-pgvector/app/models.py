from dataclasses import dataclass
from datetime import datetime


@dataclass
class DocumentChunk:
    id: int
    source: str
    content: str
    created_at: datetime
