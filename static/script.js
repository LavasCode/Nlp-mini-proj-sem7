const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('file');
const output = document.getElementById('output');
const statusEl = document.getElementById('status');

function setStatus(message, type = 'info') {
  statusEl.textContent = message;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const file = fileInput.files[0];
  if (!file) {
    setStatus('Please select a file first.');
    return;
  }
  output.textContent = '{ /* results appear here */ }';
  setStatus('Uploading and parsing…');
  try {
    const data = new FormData();
    data.append('file', file);
    const res = await fetch('/api/parse', { method: 'POST', body: data });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to parse resume');
    }
    const json = await res.json();
    output.textContent = JSON.stringify(json, null, 2);
    setStatus('Done.');
  } catch (err) {
    console.error(err);
    setStatus('Error: ' + err.message);
  }
});
