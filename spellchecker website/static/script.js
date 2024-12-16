document.getElementById('checkBtn').addEventListener('click', async () => {
    const text = document.getElementById('inputText').value;

    if (!text.trim()) {
        alert('Please enter some text.');
        return;
    }

    const response = await fetch('/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
    });

    const data = await response.json();

    // Display suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    for (const [word, matches] of Object.entries(data.suggestions)) {
        const li = document.createElement('li');
        li.textContent = `${word}: ${matches.join(', ')}`;
        suggestionsList.appendChild(li);
    }

    // Display corrected text
    document.getElementById('correctedText').textContent = data.correctedText;
});
