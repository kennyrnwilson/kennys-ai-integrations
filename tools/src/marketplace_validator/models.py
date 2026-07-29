from dataclasses import dataclass

ERROR = "error"
WARNING = "warning"


@dataclass(frozen=True)
class Finding:
    """A single validation result. `path` is repo-relative for stable CI output."""

    level: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper():7} {self.path}: {self.message}"
