import pandas as pd
from fuzzywuzzy import fuzz
import os

class SpellCheck:
    def __init__(self, dataset_path):
        # Load the dataset dynamically based on file type
        self.dictionary = self._load_dataset(dataset_path)

    def _load_dataset(self, dataset_path):
        """
        Load the dataset and return a set of words for spell checking.
        """
        try:
            if dataset_path.endswith('.csv'):
                df = pd.read_csv(dataset_path, encoding='utf-8')
            elif dataset_path.endswith('.xlsx'):
                df = pd.read_excel(dataset_path, engine='openpyxl')
            else:
                raise ValueError("Unsupported file format. Use .csv or .xlsx")

            # Validate required columns
            if 'word' not in df.columns:
                raise ValueError("Dataset must contain a 'word' column.")
            
            # Return the unique words as a set for fast lookup
            return set(df['word'].str.strip())
        except Exception as e:
            print(f"Error loading dataset: {e}")
            raise

    def check(self, string_to_check):
        """
        Set the string to be checked.
        """
        self.string_to_check = string_to_check

    def suggestions(self):
        """
        Provide spelling suggestions for each word in the input string.
        """
        words = self.string_to_check.split()
        suggestions = {}

        for word in words:
            # Find matches in the dictionary
            matches = [
                dict_word for dict_word in self.dictionary
                if fuzz.ratio(word, dict_word) >= 75
            ]
            suggestions[word] = matches if matches else ['No suggestions']

        return suggestions

    def correct(self):
        """
        Provide a corrected version of the input string based on the dictionary.
        """
        words = self.string_to_check.split()
        corrected_words = []

        for word in words:
            max_score = 0
            best_match = word

            for dict_word in self.dictionary:
                score = fuzz.ratio(word, dict_word)
                if score > max_score:
                    max_score = score
                    best_match = dict_word

            corrected_words.append(best_match if max_score >= 75 else word)

        return " ".join(corrected_words)
