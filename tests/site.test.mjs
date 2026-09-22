import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
const out = await fs.mkdtemp(path.join(os.tmpdir(), 'ai-yoga-site-'));
execFileSync(process.execPath, ['scripts/build-site.mjs', '--out', out]);
const html = await fs.readFile(path.join(out, 'index.html'), 'utf8');
const catalog = JSON.parse(await fs.readFile('web/skills.json', 'utf8'));
const decode = text => text.replaceAll('&quot;', '"').replaceAll('&gt;', '>').replaceAll('&lt;', '<').replaceAll('&amp;', '&');
test('every repository skill has one complete prompt and portable creation guidance', async () => {
  const directories = (await fs.readdir('skills', { withFileTypes: true })).filter(entry => entry.isDirectory()).map(entry => entry.name).sort();
  assert.deepEqual(catalog.map(skill => skill.id).sort(), directories);
  for (const { id } of catalog) {
    const field = html.match(new RegExp(`<textarea id="full-${id}"[^>]*>([\\s\\S]*?)</textarea>`));
    assert.ok(field, `Missing full prompt for ${id}`);
    assert.equal(decode(field[1]), await fs.readFile(`skills/${id}/SKILL.md`, 'utf8'));
    assert.ok(html.includes(`Create a reusable skill called &quot;${id}&quot;`));
  }
  assert.ok(html.includes('ask before overwriting'));
  assert.ok(!html.includes('Claude Code'));
  assert.ok(html.includes('Momence'));
  assert.ok(html.includes('Supporting file: references/continuity.md'));
});
test('all copy buttons point to a unique labelled textarea', () => {
  const ids = [...html.matchAll(/id="([^"]+)"/g)].map(match => match[1]);
  assert.equal(new Set(ids).size, ids.length);
  const copies = [...html.matchAll(/data-copy="([^"]+)"/g)].map(match => match[1]);
  assert.equal(copies.length, 15);
  for (const id of copies) {
    assert.ok(html.includes(`<textarea id="${id}"`));
    assert.ok(html.includes(`<label for="${id}">`));
  }
});
test('both deployment targets contain static content with relative assets and correct canonical', async () => {
  assert.ok(html.includes('https://tayloroneal.github.io/ai-yoga/'));
  assert.ok(html.includes('href="./toolkit.css"'));
  assert.ok(html.includes('src="./toolkit.js"'));
  assert.ok(html.includes('do not invent missing scripts'));
  execFileSync(process.execPath, ['scripts/build-site.mjs', '--personal', '--out', out]);
  const personal = await fs.readFile(path.join(out, 'index.html'), 'utf8');
  assert.ok(personal.includes('<link rel="canonical" href="https://www.tayloroneal.com/yoga/ai/">'));
  assert.ok(personal.includes('id="yoga-bio"'));
});

test('all legacy skill folder links resolve to real HTML', async () => {
  for (const { id } of catalog) {
    const page = await fs.readFile(path.join(out, 'skills', id, 'index.html'), 'utf8');
    assert.ok(page.includes(`data-initial-skill="${id}"`));
    assert.ok(page.includes('href="../../toolkit.css"'));
  }
});
