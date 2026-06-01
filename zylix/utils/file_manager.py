from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class FileSelection:
    input_files: List[Path]
    output_dir: Path


class FileManager:

    @staticmethod
    def get_files_by_extension(directory: Path, extensions: List[str]) -> List[Path]:
        files = []
        for ext in extensions:
            files.extend(directory.glob(f"*{ext}"))
            files.extend(directory.glob(f"*{ext.upper()}"))
        return sorted(files)

    @staticmethod
    def ensure_directory(path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def get_unique_output_path(output_dir: Path, base_name: str, extension: str) -> Path:
        output_path = output_dir / f"{base_name}{extension}"
        counter = 1

        while output_path.exists():
            output_path = output_dir / f"{base_name}_{counter}{extension}"
            counter += 1

        return output_path

    @staticmethod
    def validate_files(files: List[Path]) -> Optional[str]:
        if not files:
            return "No se seleccionaron archivos"

        for file_path in files:
            if not file_path.exists():
                return f"El archivo no existe: {file_path}"
            if not file_path.is_file():
                return f"No es un archivo válido: {file_path}"

        return None

    @staticmethod
    def get_file_size_str(path: Path) -> str:
        size = path.stat().st_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
