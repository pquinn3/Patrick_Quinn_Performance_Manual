"""
loader.py

Patrick Quinn Performance Manual

Responsible for locating and loading all supported ride files.
"""

from pathlib import Path
import pandas as pd


class DataLoader:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parent.parent

        self.rawdata = self.project_root / "rawdata"

    def find_files(self):

        csv_files = list(self.rawdata.rglob("*.csv"))

        tcx_files = list(self.rawdata.rglob("*.tcx"))

        pdf_files = list(self.rawdata.rglob("*.pdf"))

        return {
            "csv": csv_files,
            "tcx": tcx_files,
            "pdf": pdf_files,
        }

    def print_summary(self):

        files = self.find_files()

        print("=" * 60)
        print("Patrick Quinn Performance Manual")
        print("Stage 1A - Data Discovery")
        print("=" * 60)

        print()

        print(f"CSV files : {len(files['csv'])}")

        for file in files["csv"]:
            print(f"   • {file.name}")

        print()

        print(f"TCX files : {len(files['tcx'])}")

        for file in files["tcx"]:
            print(f"   • {file.name}")

        print()

        print(f"PDF files : {len(files['pdf'])}")

        for file in files["pdf"]:
            print(f"   • {file.name}")
