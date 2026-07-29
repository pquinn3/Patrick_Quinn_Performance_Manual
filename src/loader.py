"""
loader.py

Patrick Quinn Performance Engine

Responsible for locating, classifying, and loading ride data.
"""

from pathlib import Path
import pandas as pd

from src.ride import Ride

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
    def inspect_csv(self, file):

        try:

            df = pd.read_csv(file)

            rows = len(df)
            cols = len(df.columns)

            column_names = list(df.columns)

            missing = df.isnull().sum().sum()

            return {
                "rows": rows,
                "cols": cols,
                "columns": column_names,
                "missing": missing,
            }          

        except Exception as e:

            return {
                "error": str(e)
            }

    def load_rides(self):

            rides = []

            for file in self.find_files()["csv"]:

                try:

                    ride = Ride(file)

                    file_type = ride.file_type()

                    print(ride.name, "->", file_type)

                    if file_type == "telemetry":
                        rides.append(ride)
                    
                except Exception as e:

                    print(f"Could not load {file.name}: {e}")

            return rides

    def print_summary(self):

        files = self.find_files()

        print("=" * 60)
        print("Patrick Quinn Performance Engine")
        print("Stage 1A - Data Discovery")
        print("=" * 60)

        print()

        rides = self.load_rides()

        print(f"Ride Files : {len(rides)}")
        print()

        for ride in rides:

            print("-" * 60)

            print(ride.name)

            if ride.distance_miles is not None:
                print(f"Distance.......... {ride.distance_miles:.1f} mi")

            print(f"Duration.......... {ride.formatted_duration()}")

            if ride.avg_speed is not None:
                print(f"Avg Speed......... {ride.avg_speed:.1f} mph")

            if ride.max_speed is not None:
                print(f"Max Speed......... {ride.max_speed:.1f} mph")

            print(f"Rows.............. {ride.rows}")

            print(f"Columns........... {ride.columns}")

            print(f"Power............. {ride.has_column('power_w')}")

            print(f"Heart Rate........ {ride.has_column('heart_rate_bpm')}")

            print(f"Cadence........... {ride.has_column('cadence_rpm')}")

            print(f"GPS............... {ride.has_column('lat') and ride.has_column('lon')}")

            if ride.avg_power is not None:
                print(f"Avg Power......... {ride.avg_power:.1f} W")

            if ride.max_power is not None:
                print(f"Max Power......... {ride.max_power:.1f} W")

            if ride.avg_hr is not None:
                print(f"Avg HR............ {ride.avg_hr:.1f} bpm")

            if ride.max_hr is not None:
                print(f"Max HR............ {ride.max_hr:.1f} bpm")

            if ride.avg_cadence is not None:
                print(f"Avg Cadence....... {ride.avg_cadence:.1f} rpm")

            print()

        for file in files["csv"]:

            print("-" * 60)
            print(file.name)

            info = self.inspect_csv(file)

            if "error" in info:
                print(f"ERROR: {info['error']}")
                continue

            print(f"Rows:            {info['rows']}")
            print(f"Columns:         {info['cols']}")
            print(f"Missing Values:  {info['missing']}")

            print("Available Columns:")

            for col in info["columns"]:
                print(f"   • {col}")

            print()

        print()

        print(f"TCX files : {len(files['tcx'])}")

        for file in files["tcx"]:
            print(f"   • {file.name}")

        print()

        print(f"PDF files : {len(files['pdf'])}")

        for file in files["pdf"]:
            print(f"   • {file.name}")
