import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    sys.path.insert(0, str(Path(sys.executable).parent))

from pathlib import Path
from typing import List, Optional
import io

from PIL import Image
from pypdf import PdfReader, PdfWriter, PageRange

from .base import OperationBase, OperationResult, PdfOperationBase


class PdfToImage(PdfOperationBase):

    @property
    def name(self) -> str:
        return "PDF a Imagen"

    @property
    def output_extension(self) -> str:
        return ".png"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        from pdf2image import convert_from_path

        dpi = kwargs.get("dpi", 300)
        output_format = kwargs.get("format", "png").upper()
        output_files = []

        try:
            for pdf_path in input_paths:
                images = convert_from_path(str(pdf_path), dpi=dpi)
                base_name = pdf_path.stem
                pdf_output_dir = output_dir / base_name
                pdf_output_dir.mkdir(parents=True, exist_ok=True)

                for i, img in enumerate(images, 1):
                    output_path = pdf_output_dir / f"page_{i}.{output_format.lower()}"
                    save_format = "JPEG" if output_format == "JPG" else output_format
                    img.save(output_path, format=save_format)
                    output_files.append(output_path)

            return OperationResult(True, f"Convertido {len(output_files)} páginas", output_files)
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")


class MergePdfs(PdfOperationBase):

    @property
    def name(self) -> str:
        return "Unir PDFs"

    @property
    def output_extension(self) -> str:
        return ".pdf"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        output_name = kwargs.get("output_name", "").strip()
        try:
            writer = PdfWriter()
            for pdf_path in sorted(input_paths):
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    writer.add_page(page)

            if output_name:
                output_path = output_dir / f"{output_name}.pdf"
            else:
                output_path = output_dir / "merged.pdf"
            writer.write(output_path)

            return OperationResult(True, "PDFs unidos exitosamente", [output_path])
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")


class SplitPdf(PdfOperationBase):

    @property
    def name(self) -> str:
        return "Dividir PDF"

    @property
    def output_extension(self) -> str:
        return ".pdf"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        ranges = kwargs.get("ranges", None)
        output_files = []

        try:
            for pdf_path in input_paths:
                reader = PdfReader(pdf_path)
                base_name = pdf_path.stem
                pdf_output_dir = output_dir / base_name
                pdf_output_dir.mkdir(parents=True, exist_ok=True)

                if ranges:
                    for i, page_range in enumerate(ranges, 1):
                        writer = PdfWriter()
                        for idx in page_range:
                            if 0 <= idx < len(reader.pages):
                                writer.add_page(reader.pages[idx])
                        output_path = pdf_output_dir / f"part_{i}.pdf"
                        writer.write(output_path)
                        output_files.append(output_path)
                else:
                    for i, page in enumerate(reader.pages, 1):
                        writer = PdfWriter()
                        writer.add_page(page)
                        output_path = pdf_output_dir / f"page_{i}.pdf"
                        writer.write(output_path)
                        output_files.append(output_path)

            return OperationResult(True, f"Dividido en {len(output_files)} archivos", output_files)
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")


class CompressPdf(PdfOperationBase):

    @property
    def name(self) -> str:
        return "Comprimir PDF"

    @property
    def output_extension(self) -> str:
        return ".pdf"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        from datetime import datetime
        quality = kwargs.get("quality", "medium")
        output_name = kwargs.get("output_name", "").strip()
        output_files = []

        try:
            for pdf_path in input_paths:
                reader = PdfReader(pdf_path)
                writer = PdfWriter()
                base_name = pdf_path.stem

                if output_name and len(input_paths) == 1:
                    pdf_output_dir = output_dir
                    final_name = f"{output_name}.pdf"
                else:
                    timestamp = datetime.now().strftime("%H%M%S")
                    pdf_output_dir = output_dir / f"{base_name}_{timestamp}"
                    pdf_output_dir.mkdir(parents=True, exist_ok=True)
                    final_name = "compressed.pdf"

                for page in reader.pages:
                    writer.add_page(page)

                output_path = pdf_output_dir / final_name
                writer.write(output_path)
                output_files.append(output_path)

            return OperationResult(True, f"Comprimido {len(output_files)} PDF(s)", output_files)
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")


class ExtractTextFromPdf(PdfOperationBase):

    @property
    def name(self) -> str:
        return "Extraer Texto de PDF"

    @property
    def output_extension(self) -> str:
        return ".txt"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        output_files = []

        try:
            for pdf_path in input_paths:
                reader = PdfReader(pdf_path)
                base_name = pdf_path.stem
                pdf_output_dir = output_dir / base_name
                pdf_output_dir.mkdir(parents=True, exist_ok=True)
                text_parts = []

                for i, page in enumerate(reader.pages, 1):
                    text = page.extract_text()
                    text_parts.append(f"--- Página {i} ---\n{text}\n")

                output_path = pdf_output_dir / "texto.txt"
                output_path.write_text("\n".join(text_parts), encoding="utf-8")
                output_files.append(output_path)

            return OperationResult(True, f"Extraído texto de {len(output_files)} PDF(s)", output_files)
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")


class AddWatermark(PdfOperationBase):

    @property
    def name(self) -> str:
        return "Agregar Marca de Agua"

    @property
    def output_extension(self) -> str:
        return ".pdf"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        from datetime import datetime
        watermark_text = kwargs.get("text", "WATERMARK")
        position = kwargs.get("position", "center")
        opacity = kwargs.get("opacity", 0.3)
        output_name = kwargs.get("output_name", "").strip()
        output_files = []

        try:
            for pdf_path in input_paths:
                reader = PdfReader(pdf_path)
                writer = PdfWriter()
                base_name = pdf_path.stem

                if output_name and len(input_paths) == 1:
                    pdf_output_dir = output_dir
                    final_name = f"{output_name}.pdf"
                else:
                    timestamp = datetime.now().strftime("%H%M%S")
                    pdf_output_dir = output_dir / f"{base_name}_{timestamp}"
                    pdf_output_dir.mkdir(parents=True, exist_ok=True)
                    final_name = "watermarked.pdf"

                for page in reader.pages:
                    page.merge_page(page)
                    writer.add_page(page)

                output_path = pdf_output_dir / final_name
                writer.write(output_path)
                output_files.append(output_path)

            return OperationResult(True, f"Marca de agua agregada a {len(output_files)} PDF(s)", output_files)
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")


class RotatePdf(PdfOperationBase):

    @property
    def name(self) -> str:
        return "Rotar PDF"

    @property
    def output_extension(self) -> str:
        return ".pdf"

    def execute(self, input_paths: List[Path], output_dir: Path, **kwargs) -> OperationResult:
        from datetime import datetime
        angle = kwargs.get("angle", 90)
        pages = kwargs.get("pages", "all")
        output_name = kwargs.get("output_name", "").strip()
        output_files = []

        try:
            for pdf_path in input_paths:
                reader = PdfReader(pdf_path)
                writer = PdfWriter()
                base_name = pdf_path.stem

                if output_name and len(input_paths) == 1:
                    pdf_output_dir = output_dir
                    final_name = f"{output_name}.pdf"
                else:
                    timestamp = datetime.now().strftime("%H%M%S")
                    pdf_output_dir = output_dir / f"{base_name}_{timestamp}"
                    pdf_output_dir.mkdir(parents=True, exist_ok=True)
                    final_name = "rotated.pdf"

                for i, page in enumerate(reader.pages):
                    if pages == "all" or i in pages:
                        page.rotate(angle)
                    writer.add_page(page)

                output_path = pdf_output_dir / final_name
                writer.write(output_path)
                output_files.append(output_path)

            return OperationResult(True, f"Rotado {len(output_files)} PDF(s)", output_files)
        except Exception as e:
            return OperationResult(False, f"Error: {str(e)}")
