import argparse
import csv
import logging
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter


logger = logging.getLogger(__name__)


def load_passwords(password_file: Path) -> dict:
    """Load mapping of PDF filenames to passwords from a CSV file.

    The CSV must contain two columns: filename and password.
    """
    passwords = {}
    with password_file.open(newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                passwords[row[0]] = row[1]

    logger.info("Loaded %d password entries", len(passwords))
    return passwords


def unlock_pdfs(input_dir: Path, password_file: Path, output_dir: Path) -> None:
    passwords = load_passwords(password_file)
    output_dir.mkdir(parents=True, exist_ok=True)

    for entry in sorted(input_dir.iterdir()):
        if entry.suffix.lower() != ".pdf":
            continue

        password = passwords.get(entry.name)
        if password is None:
            logger.warning("No password found for %s. Skipping.", entry.name)
            continue

        reader = PdfReader(str(entry))
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except Exception as exc:
                logger.error("Failed to decrypt %s: %s", entry.name, exc)
                continue

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        output_path = output_dir / f"{entry.stem}_unlocked.pdf"
        with output_path.open("wb") as f:
            writer.write(f)
        logger.info("Unlocked %s -> %s", entry.name, output_path.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Unlock password-protected PDF files")
    parser.add_argument("input_dir", type=Path, help="Directory containing encrypted PDFs")
    parser.add_argument("password_file", type=Path, help="CSV file mapping PDF filenames to passwords")
    parser.add_argument("output_dir", type=Path, help="Directory to store unlocked PDFs")
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (e.g., INFO, DEBUG)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO), format="%(levelname)s:%(message)s")

    unlock_pdfs(args.input_dir, args.password_file, args.output_dir)


if __name__ == "__main__":
    main()
