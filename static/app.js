function askAgent() {
    const userPrompt = document.getElementById('userPrompt').value;
    const responseElement = document.getElementById('response');
    const pipImage = document.getElementById('pip-image');

    // Show thinking animation
    pipImage.classList.add('thinking');
    responseElement.style.display = 'block';
    responseElement.textContent = 'Thinking...';

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: userPrompt }),
    })
    .then(response => response.json())
    .then(data => {
        pipImage.classList.remove('thinking');
        responseElement.style.opacity = '0';
        setTimeout(() => {
            responseElement.textContent = data.response;
            responseElement.style.opacity = '1';
        }, 300);
    });
}

// Hide response box initially
document.addEventListener('DOMContentLoaded', function() {
    const responseElement = document.getElementById('response');
    responseElement.style.display = 'none';
    
    // Add pulse animation to Pip's image
    const pipImage = document.getElementById('pip-image');
    pipImage.addEventListener('mouseover', () => pipImage.classList.add('pulse'));
    pipImage.addEventListener('mouseout', () => pipImage.classList.remove('pulse'));

    // Human check logic
    const humanCheckOverlay = document.getElementById('human-check-overlay');
    const humanCheckYes = document.getElementById('human-check-yes');
    const humanCheckNo = document.getElementById('human-check-no');

    humanCheckYes.addEventListener('click', () => {
        humanCheckOverlay.style.display = 'none';
    });

    humanCheckNo.addEventListener('click', () => {
        document.body.innerHTML = '<h1>Humans only</h1>';
    });
});
