import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const personal = process.argv.includes('--personal');
const outputFlag = process.argv.indexOf('--out');
const out = outputFlag < 0 ? path.join(root, 'dist') : path.resolve(process.argv[outputFlag + 1]);
const repo = 'https://github.com/TaylorONeal/ai-yoga';
const revision = execFileSync('git', ['log', '-1', '--format=%H', '--', 'skills', ':!skills/*/index.html'], { cwd: root, encoding: 'utf8' }).trim();
const canonical = personal ? 'https://www.tayloroneal.com/yoga/ai/' : 'https://tayloroneal.github.io/ai-yoga/';
const skills = JSON.parse(await fs.readFile(path.join(root, 'web/skills.json'), 'utf8'));
const escape = text => text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const box = (id, label, value, rows = 5) => `<div class="copy-box"><div class="copy-heading"><label for="${id}">${label}</label><button type="button" data-copy="${id}" aria-label="Copy ${label.toLowerCase()}">Copy <span aria-hidden="true">↗</span></button></div><textarea id="${id}" readonly rows="${rows}" spellcheck="false">${escape(value)}</textarea></div>`;
// Include all prose resources in a single portable prompt, without requiring repository access.
async function markdownFiles(directory, relative = '') {
  const result = [];
  for (const entry of await fs.readdir(path.join(directory, relative), { withFileTypes: true })) {
    if (entry.name.startsWith('.')) continue;
    const name = path.posix.join(relative, entry.name);
    if (entry.isDirectory()) result.push(...await markdownFiles(directory, name));
    else if (entry.name.endsWith('.md') && entry.name !== 'README.md' && entry.name !== 'LICENSE') result.push(name);
  }
  return result.sort();
}
const panels = await Promise.all(skills.map(async (skill, index) => {
  const directory = path.join(root, 'skills', skill.id);
  const prompt = await fs.readFile(path.join(directory, 'SKILL.md'), 'utf8');
  const resources = (await markdownFiles(directory)).filter(file => file !== 'SKILL.md');
  const supporting = await Promise.all(resources.map(async file => `\n\n--- Supporting file: ${file} ---\n${await fs.readFile(path.join(directory, file), 'utf8')}`));
  const session = `Use the complete method below to help me with ${skill.label.toLowerCase()} in this conversation. Do the work with me now; saving or installing a skill is optional. If I ask you to save it, use the features actually available in this assistant, preserve existing skills, and ask before overwriting. If saving is unavailable, say so and continue here. Follow every relevant section of SKILL.md and the included supporting guides, including evidence rules, output structure, quality checks, and continuity. Treat examples as examples, never as facts about me. Use only information I share or sources I authorize. If essential material is missing, ask focused questions before drafting; do not invent personal history, credentials, attendance, quotations, or prior reflections.

MY REQUEST
${skill.example}

MY MATERIAL AND PREFERENCES
[Add your notes, source material, preferred format, and any constraints here. If left blank, help me identify what you need.]

The complete written method is included below. Supporting scripts and sample files are at ${repo}/tree/${revision}/skills/${skill.id}. If code or external files are needed, explain what is missing and ask me to provide or authorize access. Do not claim to run scripts, connect accounts, schedule tasks, publish, or send messages without the necessary tools and my request.

--- SKILL.md ---
${prompt}${supporting.join('')}`;
  return `<article class="skill-panel" id="${skill.id}" aria-labelledby="title-${skill.id}"><div class="panel-top"><span class="eyebrow">Field guide ${String(index + 1).padStart(2, '0')} / ${skill.category}</span><a href="${repo}/tree/${revision}/skills/${skill.id}">Source ↗</a></div><h3 id="title-${skill.id}">${skill.title}</h3><p class="description">${skill.description}</p><div class="skill-example example-${skill.id}"><span class="eyebrow">${skill.sampleTitle}</span><div>${skill.sample.map((line,i) => `<p><span class="sample-marker">${skill.id === 'morning-sutra-mantra' ? '·' : String(i + 1).padStart(2,'0')}</span>${line}</p>`).join('')}</div></div><div class="input-output"><div><span>You bring</span><p>${skill.input}</p></div><div><span>You leave with</span><p>${skill.output}</p></div></div><h4 class="method-label">Inside the method</h4><ul class="depth-list">${skill.depth.map(item => `<li>${item}</li>`).join('')}</ul><p class="setup-note">${skill.note}</p><div class="create-intro"><div><h4>Copy the complete prompt.</h4><p>Paste it into your AI assistant and add your material where indicated. The full method and supporting guides are included.</p></div></div>${box(`full-${skill.id}`, `Complete prompt: ${skill.label}`, session, 14)}<p class="hint">Includes the full skill and ${resources.length} supporting ${resources.length === 1 ? 'guide' : 'guides'}. You can also ask your assistant to save it for next time.</p>${resources.length ? `<div class="resource-list"><h4>Source guides</h4>${resources.map(file => `<a href="${repo}/blob/${revision}/skills/${skill.id}/${file}">${file.replaceAll('-', ' ').replace(/\.md$/, '')} ↗</a>`).join('')}</div>` : ''}</article>`;
}));
const petals = Array.from({length:12}, (_,i) => `<ellipse cx="240" cy="157" rx="55" ry="133" transform="rotate(${i*30} 240 240)"/>`).join('');
const geometry = `<svg viewBox="0 0 480 480" fill="none" aria-hidden="true"><defs><radialGradient id="gold"><stop stop-color="#ffe4a4"/><stop offset=".7" stop-color="#be853d"/><stop offset="1" stop-color="#5e411c"/></radialGradient></defs><g stroke="url(#gold)" stroke-width=".7">${petals}<circle cx="240" cy="240" r="224"/><circle cx="240" cy="240" r="202"/><circle cx="240" cy="240" r="109"/><circle cx="240" cy="240" r="76"/></g><g fill="#d9b16b">${Array.from({length:24},(_,i)=>{const angle=i*Math.PI/12;return `<circle cx="${240+213*Math.cos(angle)}" cy="${240+213*Math.sin(angle)}" r="1.4"/>`}).join('')}</g></svg>`;
const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>AI for yoga teachers · The Practice Toolkit</title><meta name="description" content="Five thoughtful AI skills for yoga teachers: class reconstruction, teacher bios, feedback, a practice-history tracker, and daily sutra contemplation. Copy the full skill into your assistant."><link rel="canonical" href="${canonical}"><meta property="og:title" content="AI for yoga teachers · The Practice Toolkit"><meta property="og:description" content="Keep the craft. Make room for the practice. Five open skills with complete, copyable guidance."><meta property="og:type" content="website"><meta property="og:url" content="${canonical}"><meta name="theme-color" content="#100e0a"><link rel="stylesheet" href="./toolkit.css"><script src="./toolkit.js" defer></script></head>
<body><a class="skip" href="#toolkit">Skip to the skills</a><nav class="site-nav" aria-label="Taylor’s website"><div><a href="https://www.tayloroneal.com/">Taylor O’Neal</a><a href="https://www.tayloroneal.com/yoga">← Yoga</a><a href="https://www.tayloroneal.com/projects">Projects</a></div></nav><div class="ambient" aria-hidden="true"></div><div class="shell"><header><a class="brand" href="https://www.tayloroneal.com/"><span class="brand-mark" aria-hidden="true">✳</span><span>TAYLOR O’NEAL<small>YOGA / OPEN TOOLS</small></span></a><nav aria-label="Main navigation"><a href="#toolkit">The skills</a><a href="#start">How to use</a><a href="${repo}">GitHub ↗</a></nav></header>
<main><section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="gold-line"></span> Technology in service of practice</p><h1>Keep the craft.<br><em>Make room</em><br>for the practice.</h1><p class="hero-description">AI for the work around teaching yoga.<br>Hold onto what you learn. Find the words.<br>Leave a little more space for being there.</p><div class="hero-actions"><a class="primary" href="#toolkit">Explore the five skills <span aria-hidden="true">↘</span></a><a href="#start">Start with a copy & paste</a></div></div><div class="practice-art"><div class="mandala">${geometry}</div><div class="art-center"><span>THE PRACTICE</span><em>Human at<br>the center.</em><small>Five skills. Your judgment.</small></div><span class="orbit-word orbit-top">ATTENTION</span><span class="orbit-word orbit-right">REFLECTION</span><span class="orbit-word orbit-bottom">CONTINUITY</span><span class="orbit-word orbit-left">CRAFT</span><div class="art-caption"><span class="tiny-star">✧</span> Tools to carry the work. Room to keep the wonder.</div></div></section>
<div class="edition-strip"><span>01 / THE OPEN COLLECTION</span><span>5 considered skills</span><span>Full instructions, always</span><span>Made for your AI assistant</span></div>
<section id="start" class="start"><div><p class="eyebrow">A small beginning</p><h2>A skill is a way of working.<br><em>Give it to your AI.</em></h2><p class="intro-note">No code to write. No special vocabulary to learn.<br>Start with the work you want to do.</p></div><ol><li><span>01</span><div><h3>Choose what you need.</h3><p>A class you want to remember. A bio to rewrite. A morning with a little more depth.</p></div></li><li><span>02</span><div><h3>Copy the complete prompt.</h3><p>Paste it into your AI assistant. The instructions and supporting guidance come with it.</p></div></li><li><span>03</span><div><h3>Make it part of your practice.</h3><p>Add your material where indicated and review what comes back. You can ask your assistant to save the method for later.</p></div></li></ol></section>
<section id="toolkit" class="toolkit"><div class="section-heading"><div><p class="eyebrow">The practice toolkit</p><h2>What are you <em>working on?</em></h2></div><span class="collection-count">EXPLORE / 01 TO 05</span></div><div class="workbench"><nav class="skill-picker" aria-label="Choose a yoga skill">${skills.map((skill, i) => `<a href="#${skill.id}" data-skill="${skill.id}"><span class="skill-number">0${i + 1}</span><span><strong>${skill.label}</strong><small>${skill.category}</small></span><span aria-hidden="true">↗</span></a>`).join('')}<div class="picker-note"><span aria-hidden="true">✧</span><p>Keep your experience.<br>Let the tools carry<br>some of the work.</p></div></nav><div class="panels">${panels.join('\n')}</div></div><p id="copy-status" class="copy-status" role="status" aria-live="polite"></p></section>
<section class="care"><div><p class="eyebrow">A few things worth keeping</p><h2>The attention is yours.<br><em>So is the judgment.</em></h2></div><div><p>These are open instructions, not an AI service. Use them with an assistant that accepts long prompts. Saving skills, working with files, and connecting accounts depend on the tools your assistant actually supports.</p><p>Keep student names and sensitive details out of shared prompts. This website does not collect what you copy. Your AI provider’s data policies apply when you paste it there.</p><p class="hint">The skills are free and MIT licensed. Your assistant may have its own fees. Code-assisted tasks need the complete skill folder from the repository; your assistant can explain that when it is relevant.</p></div></section></main>
<footer><a href="https://www.tayloroneal.com/yoga">← Back to the practice</a><p>Built with care. Shared openly.</p><a href="${repo}">Source & supporting files ↗</a></footer></div></body></html>`;
await fs.mkdir(out, { recursive: true });
await fs.writeFile(path.join(out, 'index.html'), html);
for (const name of ['toolkit.css', 'toolkit.js']) await fs.copyFile(path.join(root, 'web', name), path.join(out, name));
await fs.writeFile(path.join(out, '.nojekyll'), '');
await fs.writeFile(path.join(out, 'source.json'), JSON.stringify({ repository: repo, revision, skills: skills.map(s => s.id) }, null, 2) + '\n');
// Folder links from the original README now resolve to real HTML on Pages.
for (const skill of skills) {
  const directory = path.join(out, 'skills', skill.id);
  await fs.mkdir(directory, { recursive: true });
  const page = html.replace('<body>', `<body data-initial-skill="${skill.id}">`)
    .replace('href="./toolkit.css"', 'href="../../toolkit.css"')
    .replace('src="./toolkit.js"', 'src="../../toolkit.js"')
    .replaceAll(canonical, `${canonical}skills/${skill.id}/`)
    .replace('<title>AI for yoga teachers · The Practice Toolkit</title>', `<title>${skill.label} · AI for yoga teachers</title>`);
  await fs.writeFile(path.join(directory, 'index.html'), page);
}
console.log(`Built ${skills.length} complete skills with self-contained prompts for ${canonical}`);
