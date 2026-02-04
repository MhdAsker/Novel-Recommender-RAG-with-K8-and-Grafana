import pandas as pd
from typing import List


class BookDataLoader:
    def __init__(self, input_csv: str, output_csv: str):
        self.input_csv = input_csv
        self.output_csv = output_csv

        self.required_columns: List[str] = [
            "title",
            "author",
            "genres",
            "description"
        ]

    def load_and_process(self) -> pd.DataFrame:
        # Load dataset
        df = pd.read_csv(
            self.input_csv,
            encoding="utf-8",
            on_bad_lines="skip"
        )

        # Validate required columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Drop rows missing core semantic fields
        df = df.dropna(subset=self.required_columns)

        # Build clean semantic text for embeddings
        df["combined_info"] = (
            "Title: " + df["title"].astype(str) + ". "
            "Author: " + df["author"].astype(str) + ". "
            "Genres: " + df["genres"].astype(str) + ". "
            "Description: " + df["description"].astype(str)
        )

        # Persist processed dataset
        df.to_csv(self.output_csv, index=False, encoding="utf-8")

        return df
