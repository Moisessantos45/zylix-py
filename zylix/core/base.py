from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path


@dataclass
class OperationResult:
    success: bool
    message: str
    output_files: List[Path] = None

    def __post_init__(self):
        if self.output_files is None:
            self.output_files = []


class OperationBase(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        pass

    @property
    @abstractmethod
    def input_extensions(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def output_extension(self) -> str:
        pass

    @abstractmethod
    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:

        pass

    def validate_inputs(self, input_paths: List[Path]) -> Optional[str]:
        if not input_paths:
            return "No input files provided"

        for path in input_paths:
            if not path.exists():
                return f"File not found: {path}"
            ext = path.suffix.lower()
            if ext not in self.input_extensions and f".{ext.lstrip('.')}" not in self.input_extensions:
                return f"Unsupported file type: {ext}"

        return None


class PdfOperationBase(OperationBase):
    @property
    def category(self) -> str:
        return "pdf"

    @property
    def input_extensions(self) -> List[str]:
        return [".pdf"]


class ImageOperationBase(OperationBase):

    @property
    def category(self) -> str:
        return "image"

    @property
    def input_extensions(self) -> List[str]:
        return [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"]
