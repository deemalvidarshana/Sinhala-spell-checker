import pandas as pd
from fuzzywuzzy import fuzz


class SpellCheck:
    def __init__(self, dataset_path):
        # Check if the file is Excel or CSV and load it accordingly
        if dataset_path.endswith('.xlsx') or dataset_path.endswith('.xls'):
            try:
                df = pd.read_excel(dataset_path, engine='openpyxl')
            except Exception as e:
                raise Exception(f"Error reading Excel file: {e}")
        else:
            try:
                df = pd.read_csv(dataset_path, encoding='utf-8', sep=',', header=0)
            except UnicodeDecodeError:
                raise Exception("Error decoding CSV file. Ensure it's UTF-8 encoded.")

        # Ensure the file contains a 'word' column
        if 'word' not in df.columns:
            raise ValueError("Dataset must have a 'word' column.")

        # Extract words into a list
        self.dictionary = df['word'].drop_duplicates().str.strip().tolist()

    def check(self, string_to_check):
        """Set the string to check."""
        self.string_to_check = string_to_check

    def suggestions(self):
        """Provide word suggestions based on fuzzy matching."""
        string_words = self.string_to_check.split()
        suggestions = []
        for i in range(len(string_words)):
            for word in self.dictionary:
                if fuzz.ratio(string_words[i], word) >= 75:  # Threshold for similarity
                    suggestions.append(word)
        return suggestions

    def correct(self):
        """Return corrected text based on the highest similarity match."""
        string_words = self.string_to_check.split()
        for i in range(len(string_words)):
            max_percent = 0
            for word in self.dictionary:
                percent = fuzz.ratio(string_words[i], word)
                if percent >= 75 and percent > max_percent:
                    string_words[i] = word
                    max_percent = percent
        return " ".join(string_words)
