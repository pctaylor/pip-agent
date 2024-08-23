function askAgent() {
    const userPrompt = document.getElementById('userPrompt').value;
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: userPrompt }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').textContent = data.response;
    });
}
