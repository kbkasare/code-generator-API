document.addEventListener("DOMContentLoaded", function() {
    const editor = CodeMirror(document.getElementById('editor'), {
        mode: "python",
        lineNumbers: true
    });

    window.runCode = function() {
        const code = editor.getValue();
        fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        })
        .then(response => response.json())
        .then(data => {
            const outputDiv = document.getElementById('output');
            if (data.output) {
                outputDiv.textContent = data.output;
            } else if (data.error) {
                outputDiv.textContent = data.error;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});

