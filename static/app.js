function askAgent() {
    const userPrompt = document.getElementById('userPrompt').value;
    const responseElement = document.getElementById('response');
    const pipImage = document.getElementById('pip-image');
    const markdownContent = document.getElementById('markdown-content');

    // Show thinking animation
    pipImage.classList.add('thinking');
    if (responseElement) {
        responseElement.style.display = 'none';
    }
    if (markdownContent) {
        markdownContent.style.display = 'none';
        markdownContent.style.opacity = '0';
    }

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
        if (markdownContent) {
            // Highlight specific names
            const highlightedResponse = data.response.replace(
                /(Pip|Phil|Philip|Phil Taylor)/gi,
                '<span class="highlight-name">$1</span>'
            );
            markdownContent.innerHTML = highlightedResponse;
            markdownContent.style.display = 'block';
            setTimeout(() => {
                markdownContent.style.opacity = '1';
            }, 10);
        } else {
            console.error('Markdown content element not found');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        pipImage.classList.remove('thinking');
        if (responseElement) {
            responseElement.textContent = 'An error occurred. Please try again.';
            responseElement.style.display = 'block';
        }
    });
}

// Hide response box initially
document.addEventListener('DOMContentLoaded', function() {
    const humanVerified = localStorage.getItem('humanVerified');
    const humanCheckOverlay = document.getElementById('human-check-overlay');
    const humanCheckYes = document.getElementById('human-check-yes');
    const humanCheckNo = document.getElementById('human-check-no');
    const responseElement = document.getElementById('response');
    const pipImage = document.getElementById('pip-image');

    // Always show the overlay by default
    if (humanCheckOverlay) {
        humanCheckOverlay.style.display = 'flex';
    }

    // Only hide the overlay if the user is verified
    if (humanVerified === 'true' && humanCheckOverlay) {
        humanCheckOverlay.style.display = 'none';
    }

    if (responseElement) {
        responseElement.style.display = 'none';
    }
    
    if (pipImage) {
        pipImage.addEventListener('mouseover', () => pipImage.classList.add('pulse'));
        pipImage.addEventListener('mouseout', () => pipImage.classList.remove('pulse'));
    }

    // Human check logic
    if (humanCheckYes) {
        humanCheckYes.addEventListener('click', () => {
            if (humanCheckOverlay) {
                humanCheckOverlay.style.display = 'none';
            }
            // Set a flag in localStorage to remember the user's choice
            localStorage.setItem('humanVerified', 'true');
        });
    }

    if (humanCheckNo) {
        humanCheckNo.addEventListener('click', () => {
            document.body.innerHTML = '<h1>Humans only</h1>';
        });
    }
});
