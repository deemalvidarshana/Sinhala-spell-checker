# app.py
from flask import Flask, render_template, request
from spellcheck import SpellCheck

app = Flask(__name__)

# Initialize the spell checker with the dataset
spell_check = SpellCheck('data-spell-checker.xlsx')  # Path to your dataset

@app.route('/')
def index():
    return render_template('index.html', input_text='', corrected_text='', suggestions={}, word_status={}, all_correct=True)

@app.route('/check', methods=['POST'])
def check_spelling():
    user_input = request.form.get('user_input')

    if user_input:
        spell_check.check(user_input)
        corrected_text = spell_check.correct()

        words = user_input.split()
        suggestions = spell_check.suggestions()

        word_status = {}
        incorrect_words = {}

        all_correct = True

        for word in words:
            if word in spell_check.dictionary:
                word_status[word] = 'Correct'
            else:
                all_correct = False
                word_status[word] = 'Incorrect'
                incorrect_words[word] = suggestions.get(word, [])

        return render_template('index.html', input_text=user_input, corrected_text=corrected_text, suggestions=incorrect_words, word_status=word_status, all_correct=all_correct)

    return render_template('index.html', input_text='', corrected_text='', suggestions={}, word_status={}, all_correct=True)

if __name__ == '__main__':
    app.run(debug=True)
