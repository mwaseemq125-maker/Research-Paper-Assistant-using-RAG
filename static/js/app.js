```javascript
async function uploadFiles() {

    const input = document.getElementById("files");
    const status = document.getElementById("uploadStatus");

    if (!input.files.length) {
        status.innerHTML = "⚠️ Please select a PDF.";
        return;
    }

    const formData = new FormData();

    for (const file of input.files) {
        formData.append("files", file);
    }

    status.innerHTML = "⏳ Processing PDFs...";

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    status.innerHTML =
        `✅ ${data.uploaded.length} document(s) uploaded successfully.`;

    loadDocuments();
}


async function loadDocuments() {

    const response = await fetch("/documents");
    const data = await response.json();

    const container = document.getElementById("documents");

    if (!data.documents.length) {
        container.innerHTML = "No documents uploaded.";
        return;
    }

    container.innerHTML = data.documents
        .map(name => `<div class="doc">📄 ${name}</div>`)
        .join("");
}


async function askQuestion() {

    const input = document.getElementById("question");
    const chat = document.getElementById("chat");

    const question = input.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    chat.innerHTML += `
        <div class="message user">
            <b>You:</b><br>${escapeHtml(question)}
        </div>
    `;

    input.value = "";

    chat.innerHTML += `
        <div class="message ai" id="loading">
            ⏳ Searching research papers...
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    const formData = new FormData();
    formData.append("question", question);

    try {

        const response = await fetch("/chat", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("loading").remove();

        let html = `
            <div class="message ai">
                <b>🤖 Assistant:</b><br>
                ${escapeHtml(data.answer).replace(/\n/g, "<br>")}
        `;

        if (data.sources && data.sources.length) {

            html += `<div class="source"><b>Sources:</b>`;

            data.sources.forEach(source => {
                html += `
                    <br>📄 ${escapeHtml(source.source)}
                    — Page ${source.page}
                `;
            });

            html += `</div>`;
        }

        html += `</div>`;

        chat.innerHTML += html;

    } catch (error) {

        document.getElementById("loading").innerHTML =
            "❌ Unable to process your question.";
    }

    chat.scrollTop = chat.scrollHeight;
}


function escapeHtml(text) {

    const div = document.createElement("div");
    div.textContent = text;

    return div.innerHTML;
}


loadDocuments();
```
