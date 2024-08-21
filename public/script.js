document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('input-text');
    const complexity = document.getElementById('complexity');
    const keywords = document.getElementById('keywords');
    const enhanceBtn = document.getElementById('enhance-btn');
    const outputText = document.getElementById('output-text');

    enhanceBtn.addEventListener('click', async () => {
        const text = inputText.value;
        const selectedComplexity = complexity.value;
        const preserveKeywords = keywords.value.split(',').map(k => k.trim());

        if (!text) {
            alert('Please enter some text to enhance!');
            return;
        }

        enhanceBtn.disabled = true;
        enhanceBtn.textContent = 'Enhancing...';

        try {
            const response = await fetch('/api/enhance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text,
                    complexity: selectedComplexity,
                    preserveKeywords,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to enhance text');
            }

            outputText.textContent = data.enhancedText;
        } catch (error) {
            console.error('Error:', error);
            alert(`An error occurred while enhancing the text: ${error.message}`);
        } finally {
            enhanceBtn.disabled = false;
            enhanceBtn.textContent = 'Enhance Text';
        }
    });
});
