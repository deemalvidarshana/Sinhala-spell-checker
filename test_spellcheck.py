from spellcheck import SpellCheck

# Initialize the spell checker with the dataset
spell_check = SpellCheck('data-spell-checker.xlsx')  # Path to your dataset

# Set the string to be checked
string_to_be_checked = "අංක අමකය අංකනට"  
spell_check.check(string_to_be_checked)

# Print suggestions and corrected text
print("Suggestions:", spell_check.suggestions())
print("Corrected Text:", spell_check.correct())
