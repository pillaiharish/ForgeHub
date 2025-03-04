document.addEventListener('DOMContentLoaded', function() {
    const pdfForm = document.getElementById('pdf-form');
    const resultDiv = document.getElementById('result');
    const convertedImage = document.getElementById('converted-image');
    const downloadLink = document.getElementById('download-link');

    pdfForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const pdfFile = document.getElementById('pdf-file').files[0];
        const formData = new FormData();
        formData.append('pdf-file', pdfFile);

        fetch('/convert', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            convertedImage.src = data.image_url;
            downloadLink.href = data.download_url;
            downloadLink.download = pdfFile.name.replace('.pdf', '.jpg');
            resultDiv.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
