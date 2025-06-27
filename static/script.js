
document.getElementById('analyze-button').addEventListener('click', async () => {
    const imageInput = document.getElementById('image-input');
    const file = imageInput.files[0];
    if (!file) {
        alert('Please select an image first.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    const resultDiv = document.getElementById('result');
    resultDiv.textContent = 'Analyzing...';

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
        } else {
            resultDiv.innerText = data.analysis;
        }
    } catch (error) {
        resultDiv.textContent = 'An error occurred.';
        console.error(error);
    }
});
