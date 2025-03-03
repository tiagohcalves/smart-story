from dataclasses import dataclass
import json
import uuid
from datetime import datetime

@dataclass
class Document:
    def __init__(self, id=None, content="", description="", timestamp=None, filetype=""):
        """
        Initialize a Document.

        :param id: Unique document ID (auto-generated if None).
        :param content: Text content of the document.
        :param description: Short description of the document.
        :param timestamp: Timestamp of creation (defaults to now).
        :param filetype: Type of the file (e.g., 'pdf', 'txt', 'jpg').
        """
        self.id = id or str(uuid.uuid4())  # Generate UUID if not provided
        self.content = content
        self.description = description
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.filetype = filetype

    def to_dict(self):
        """Convert document to a dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "description": self.description,
            "timestamp": self.timestamp,
            "filetype": self.filetype,
        }

    def to_json(self):
        """Convert document to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data):
        """Create a Document instance from a dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            description=data["description"],
            timestamp=data["timestamp"],
            filetype=data["filetype"],
        )

    @classmethod
    def from_json(cls, json_str):
        """Create a Document instance from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self):
        return f"Document(id={self.id}, filetype={self.filetype}, timestamp={self.timestamp})"

    def get_content(self):
        if self.filetype == "img":
            return self.description

        return self.content