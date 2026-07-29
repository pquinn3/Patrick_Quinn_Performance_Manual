"""
ride.py

Patrick Quinn Performance Engine

Defines a Ride object used throughout the analytics engine.
"""

from pathlib import Path
import pandas as pd


class Ride:

    def file_type(self):

        if self.has_column("timestamp") and self.has_column("distance_m"):
            return "telemetry"

        if "rank" in self.df.columns and "firstname" in self.df.columns:
            return "race_results"

        if "Lap" in self.df.columns and "NP" in self.df.columns:
            return "lap_summary"

        return "unknown"

    def __init__(self, file):

        self.file = Path(file)

        self.name = self.file.stem

        self.df = pd.read_csv(self.file)

        self.rows = len(self.df)

        self.columns = len(self.df.columns)

        self.column_names = list(self.df.columns)

        # Basic ride metrics
        self.avg_power = self.average("power_w")
        self.max_power = self.maximum("power_w")

        self.avg_hr = self.average("heart_rate_bpm")
        self.max_hr = self.maximum("heart_rate_bpm")

        self.avg_cadence = self.average("cadence_rpm")
        self.max_cadence = self.maximum("cadence_rpm")

        self.max_speed = self.maximum("speed_ms")

        # Distance (meters → miles)
        if self.has_column("distance_m"):
            self.distance_miles = self.last("distance_m") * 0.000621371
        else:
            self.distance_miles = None

        # Duration
        self.duration_seconds = self.total_seconds()

        # Average speed (mph)
        if self.duration_seconds > 0 and self.distance_miles is not None:
            self.avg_speed = self.distance_miles / (self.duration_seconds / 3600)
        else:
            self.avg_speed = None

        # Maximum speed (mph)
        if self.max_speed is not None:
            self.max_speed *= 2.23694

    def has_column(self, column):

        return column in self.df.columns

    def average(self, column):
        """Return the average of a column, or None if it doesn't exist."""
        if self.has_column(column):
            return self.df[column].mean()
        return None

    def maximum(self, column):
        """Return the maximum of a column, or None if it doesn't exist."""
        if self.has_column(column):
            return self.df[column].max()
        return None   

    def first(self, column):
        if self.has_column(column):
            return self.df[column].iloc[0]
        return None

    def last(self, column):
        if self.has_column(column):
            return self.df[column].iloc[-1]
        return None

    def total_seconds(self):

        start = pd.to_datetime(self.first("timestamp"))
        end = pd.to_datetime(self.last("timestamp"))

        return (end - start).total_seconds()

    def formatted_duration(self):

        if self.duration_seconds is None or pd.isna(self.duration_seconds):
            return "Unknown"

        hours = int(self.duration_seconds // 3600)
        minutes = int((self.duration_seconds % 3600) // 60)
        seconds = int(self.duration_seconds % 60)

        return f"{hours}:{minutes:02}:{seconds:02}"