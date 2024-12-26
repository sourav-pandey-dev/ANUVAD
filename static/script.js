// script.js

// Function to update user count dynamically on the homepage
function updateUserCount() {
    fetch('/get-user-count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('user-count').innerText = data.user_count;
        })
        .catch(error => {
            console.error('Error fetching user count:', error);
        });
}

// Add event listeners for translation actions
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('translate-text-btn')) {
        document.getElementById('translate-text-btn').addEventListener('click', translateText);
    }

    if (document.getElementById('upload-image-btn')) {
        document.getElementById('upload-image-btn').addEventListener('click', uploadImage);
    }
});

// Text translation function
function translateText() {
    const textArea = document.getElementById('text-input');
    const sourceLang = document.getElementById('source-lang').value;
    const targetLang = document.getElementById('target-lang').value;

    fetch('/translate-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            text: textArea.value,
            source_lang: sourceLang,
            target_lang: targetLang,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('translated-text').innerText = data.translated_text;
            }
        })
        .catch(error => console.error('Error translating text:', error));
}

// Image upload and translation function
function uploadImage() {
    const fileInput = document.getElementById('image-input');
    const targetLang = document.getElementById('image-target-lang').value;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('target_lang', targetLang);

    fetch('/translate-image', {
        method: 'POST',
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById('extracted-text').innerText = data.extracted_text;
                document.getElementById('image-translated-text').innerText = data.translated_text;
            }
        })
        .catch(error => console.error('Error translating image:', error));
}

// Call updateUserCount if the user count element exists
if (document.getElementById('user-count')) {
    updateUserCount();
}

document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('user-count')) {
        updateUserCount();
    }
    if (document.getElementById('translate-text-btn')) {
        document.getElementById('translate-text-btn').addEventListener('click', translateText);
    }
    if (document.getElementById('upload-image-btn')) {
        document.getElementById('upload-image-btn').addEventListener('click', uploadImage);
    }
});

// Fetch user count dynamically
function updateUserCount() {
    fetch('/get-user-count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('user-count').innerText = data.user_count;
        })
        .catch(error => console.error('Error fetching user count:', error));
}

// Translate text
function translateText() {
    const textInput = document.getElementById('text-input').value;
    const sourceLang = document.getElementById('source-lang').value;
    const targetLang = document.getElementById('target-lang').value;

    fetch('/translate-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textInput, source_lang: sourceLang, target_lang: targetLang }),
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('translated-text').innerText = data.translated_text || 'Translation error';
        })
        .catch(error => console.error('Error translating text:', error));
}

// Upload and translate image
function uploadImage() {
    const fileInput = document.getElementById('image-input');
    const targetLang = document.getElementById('image-target-lang').value;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('target_lang', targetLang);

    fetch('/translate-image', { method: 'POST', body: formData })
        .then(response => response.json())
        .then(data => {
            document.getElementById('extracted-text').innerText = data.extracted_text || 'No text extracted';
            document.getElementById('image-translated-text').innerText = data.translated_text || 'Translation error';
        })
        .catch(error => console.error('Error translating image:', error));
}
