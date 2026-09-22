const links = [...document.querySelectorAll('[data-skill]')];
const panels = [...document.querySelectorAll('.skill-panel')];
function choose(id) {
  if (!panels.some(panel => panel.id === id)) return;
  for (const panel of panels) panel.hidden = panel.id !== id;
  for (const link of links) {
    if (link.dataset.skill === id) link.setAttribute('aria-current', 'true');
    else link.removeAttribute('aria-current');
  }
}
choose(location.hash.slice(1) || document.body.dataset.initialSkill || panels[0].id);
for (const link of links) link.addEventListener('click', () => choose(link.dataset.skill));
window.addEventListener('hashchange', () => choose(location.hash.slice(1)));
for (const button of document.querySelectorAll('[data-copy]')) {
  button.addEventListener('click', async () => {
    const field = document.getElementById(button.dataset.copy);
    const status = document.getElementById('copy-status');
    try {
      await navigator.clipboard.writeText(field.value);
      status.textContent = `${field.labels[0].textContent} copied. Ready to paste into your assistant.`;
      button.textContent = 'Copied ✓';
      setTimeout(() => { status.textContent = ''; button.textContent = 'Copy ↗'; }, 2200);
    } catch {
      field.focus();
      field.select();
      status.textContent = 'Clipboard unavailable. The complete text is selected; use your device’s Copy command.';
    }
  });
}
