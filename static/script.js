async function sendQuery() {
    const queryInput = document.getElementById('query-input').value;
    const responseContainer = document.getElementById('response-container');
    responseContainer.innerHTML = ''; // Clear previous responses

    const response = await fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query_text: queryInput }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let done = false;

    while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        const chunk = decoder.decode(value, { stream: true });
        responseContainer.innerHTML += chunk;
    }
}
