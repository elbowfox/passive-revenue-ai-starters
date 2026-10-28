// popup.js - Basic freemium AI Prompt Manager skeleton
document.addEventListener('DOMContentLoaded', async () => {
  const titleEl = document.getElementById('title');
  const promptEl = document.getElementById('prompt');
  const saveBtn = document.getElementById('save');
  const enhanceBtn = document.getElementById('enhance');
  const listEl = document.getElementById('list');
  const statusEl = document.getElementById('status');

  // Load saved prompts
  const { prompts = [] } = await chrome.storage.local.get('prompts');
  renderList(prompts);

  saveBtn.addEventListener('click', async () => {
    const title = titleEl.value.trim();
    const text = promptEl.value.trim();
    if (!title || !text) return statusEl.textContent = 'Fill title & prompt';

    const { prompts = [] } = await chrome.storage.local.get('prompts');
    prompts.push({ id: Date.now(), title, text });
    await chrome.storage.local.set({ prompts });
    renderList(prompts);
    titleEl.value = promptEl.value = '';
    statusEl.textContent = 'Saved!';
  });

  enhanceBtn.addEventListener('click', () => {
    // Pro feature: Call your backend / OpenAI-compatible API
    statusEl.textContent = 'Pro feature — connect Stripe + backend for AI enhancement';
    // Example: fetch('https://your-api.com/enhance', { method: 'POST', body: JSON.stringify({ prompt: promptEl.value }) })
  });

  function renderList(prompts) {
    listEl.innerHTML = prompts.map(p => `<li><strong>${p.title}</strong>: ${p.text.slice(0, 60)}...</li>`).join('');
  }
});
