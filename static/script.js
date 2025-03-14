// Check query status when page loads
document.addEventListener('DOMContentLoaded', function() {
    checkQueryStatus();
    // Check status every 5 seconds
    setInterval(checkQueryStatus, 5000);
});

async function queryLLM() {
    const queryText = document.getElementById("queryInput").value;
    const submitButton = document.getElementById("submitButton");
    const statusMessage = document.getElementById("statusMessage");
    const responseContainer = document.getElementById("responseContainer");
    
    if (!queryText) {
        statusMessage.textContent = "Please enter a query.";
        return;
    }

    try {
        // Disable button and show processing message
        submitButton.disabled = true;
        statusMessage.textContent = "Processing query...";
        responseContainer.innerHTML = "";  // Clear previous response

        const response = await fetch("/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query_text: queryText })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Error processing request");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let done = false;
        while (!done) {
            const { value, done: doneReading } = await reader.read();
            done = doneReading;
            const text = decoder.decode(value, { stream: true });
            responseContainer.innerHTML += text;  // Append new content to response container
            responseContainer.scrollTop = responseContainer.scrollHeight;  // Auto scroll to the bottom
        }
    } catch (error) {
        statusMessage.textContent = error.message;
        console.error("Error:", error);
    } finally {
        // Wait for a short time before enabling the button again
        // to allow the backend to properly reset the user status
        setTimeout(() => {
            checkQueryStatus();
        }, 1000);
    }
}

async function uploadPDF() {
    const fileInput = document.getElementById("pdfUpload");
    const statusMessage = document.getElementById("statusMessage");
    
    const file = fileInput.files[0];
    if (!file) {
        statusMessage.textContent = "Please select a PDF file.";
        return;
    }

    statusMessage.textContent = "Uploading file...";
    
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/upload_pdf", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        statusMessage.textContent = result.message;
    } catch (error) {
        statusMessage.textContent = "Error uploading file.";
        console.error("Upload error:", error);
    }
}

async function checkQueryStatus() {
    const submitButton = document.getElementById("submitButton");
    const statusMessage = document.getElementById("statusMessage");
    
    try {
        const response = await fetch("/query_status");
        const data = await response.json();
        
        if (data.active) {
            submitButton.disabled = true;
            statusMessage.textContent = "You have an active query processing. Please wait.";
        } else {
            submitButton.disabled = false;
            if (statusMessage.textContent === "You have an active query processing. Please wait.") {
                statusMessage.textContent = "";
            }
        }
    } catch (error) {
        console.error("Status check error:", error);
    }
}