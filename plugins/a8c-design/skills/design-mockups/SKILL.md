---
name: design-mockups
description: Build and present HTML/CSS design mockups with a local preview server. Use when prototyping website designs, iterating on visual concepts, or presenting design options.
compatibility: Requires filesystem access, a terminal, Node.js 20+, npm, and a browser preview.
---

# Design Mockups

Rapidly prototype and present HTML/CSS design mockups with a local server. Use the project brief in the user's request. Ask for it if missing.

Use the current project folder or a location chosen by the user. Check for existing files before scaffolding. Run the setup below in a new project directory. For an existing Node.js project, preserve its package settings and adapt the server filename or start command to its module system.

## Design Phases

Design work moves through distinct phases. **Know which phase you're in.**

### Phase 1: Style Exploration
**Goal:** Find the right visual direction for the entire site.

Create multiple concepts with different aesthetics (terminal, minimal, brutalist, etc.). Each mockup is a complete style — colors, typography, effects, vibe.

**Location:** `mockups/*.html` (root level)

```
mockups/
├── retro-terminal.html      # Concept A
├── minimal-stark.html       # Concept B
├── warm-organic.html        # Concept C
└── brutalist-chaos.html     # Concept D
```

**Outcome:** Pick a winner (e.g., `terminal-minimal-v2`).

---

### Phase 2: Site Templates
**Goal:** Build out all page types in the chosen style.

Create a subfolder named after the chosen direction. Build every major page template with shared styles.

**Location:** `mockups/{chosen-direction}/`

```
mockups/
├── terminal-v2-site/        # ← Chosen direction
│   ├── styles.css           # Shared design system
│   ├── home.html
│   ├── post.html
│   ├── about.html
│   ├── project.html
│   ├── archive.html
│   ├── search.html
│   └── 404.html
```

**Outcome:** Complete set of page templates.

---

### Phase 3: Section Explorations
**Goal:** Iterate on specific components or sections within the chosen style.

When a section needs multiple approaches (e.g., "how should projects be listed?"), create explorations inside the chosen direction folder.

**Location:** `mockups/{chosen-direction}/` with descriptive names

**Naming convention:** `{section}-{variant}.html`

```
mockups/
├── terminal-v2-site/
│   ├── styles.css
│   ├── home.html
│   ├── projects-grid.html         # Section exploration
│   ├── projects-file-tree.html    # Section exploration
│   ├── projects-file-tree-v2.html # Iteration on exploration
│   └── projects-hybrid.html       # Section exploration
```

**Outcome:** Pick the best approach for each section, integrate into templates.

---

## Project Structure

```
{project-name}/
├── mockups/
│   ├── concept-a.html           # Phase 1: Style exploration
│   ├── concept-b.html
│   ├── concept-c.html
│   └── {chosen-direction}/      # Phase 2+3: Templates & explorations
│       ├── styles.css           # Shared design system
│       ├── home.html            # Page template
│       ├── post.html            # Page template
│       ├── {section}-v1.html    # Section exploration
│       └── {section}-v2.html    # Section iteration
├── docs/
│   └── logs/                    # Session notes
├── server.js
├── package.json
└── README.md
```

## Quick Start

```bash
# Create project
mkdir -p {project-name}
cd {project-name}
mkdir -p mockups docs/logs

# Initialize
npm init -y
npm install express
npm pkg set type=commonjs 'scripts.start=node server.js'
```

Save the server template below as `server.js`, then start it.

```bash
npm start
```

## Server Template

Save as `server.js` to serve mockups with a gallery UI. If port 3000 is busy, choose another port with `PORT=3001 npm start`. Open the printed URL and check that the gallery and a mockup load before sharing it. For a remote environment, use its preview or forwarded port URL. To preview from another device on your network, run `HOST=0.0.0.0 npm start`.

```javascript
const express = require('express');
const fs = require('fs');
const path = require('path');
const os = require('os');

const app = express();
const PORT = Number(process.env.PORT || 3000);
const HOST = process.env.HOST || '127.0.0.1';
const MOCKUPS_DIR = path.join(__dirname, 'mockups');
fs.mkdirSync(MOCKUPS_DIR, { recursive: true });

app.use('/mockups', express.static(MOCKUPS_DIR));

function getLocalIP() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

const mockupMeta = {
  // 'direction/home': { colors: ['#112233', '#445566'], desc: 'Homepage' }
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);
}

app.get('/', (req, res) => {
  const mockups = fs.readdirSync(MOCKUPS_DIR, { recursive: true })
    .filter(f => f.endsWith('.html') && fs.statSync(path.join(MOCKUPS_DIR, f)).isFile())
    .sort()
    .map(f => {
      const relativePath = f.split(path.sep).join('/');
      const slug = relativePath.replace(/\.html$/, '');
      const meta = mockupMeta[slug] || { colors: ['#ccc', '#999', '#666', '#333'], desc: '' };
      return {
        name: escapeHtml(slug.replace(/-/g, ' ')),
        path: `/mockups/${relativePath.split('/').map(encodeURIComponent).join('/')}`,
        colors: meta.colors,
        desc: escapeHtml(meta.desc)
      };
    });

  res.send(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mockups</title>
  <style>
    :root { --bg: #f5f5f5; --card: #fff; --text: #111; --muted: #666; --border: rgba(0,0,0,0.08); }
    @media (prefers-color-scheme: dark) { :root { --bg: #161616; --card: #222; --text: #eee; --muted: #888; --border: rgba(255,255,255,0.08); } }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }
    .container { max-width: 900px; margin: 0 auto; }
    h1 { font-size: 1.25rem; margin-bottom: 2rem; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.25rem; }
    .card { background: var(--card); border-radius: 12px; overflow: hidden; text-decoration: none; color: inherit; box-shadow: 0 1px 3px var(--border); transition: transform 0.2s; }
    .card:hover { transform: translateY(-2px); }
    .preview { height: 100px; display: flex; padding: 1rem; gap: 0.5rem; }
    .swatch { flex: 1; border-radius: 6px; }
    .info { padding: 1rem; }
    .name { font-weight: 600; text-transform: capitalize; }
    .desc { font-size: 0.8rem; color: var(--muted); margin-top: 0.25rem; }
    .meta { margin-top: 2rem; font-size: 0.8rem; color: var(--muted); }
    code { background: var(--card); padding: 0.125rem 0.5rem; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Design Mockups</h1>
    <div class="grid">
      ${mockups.map(m => `<a href="${m.path}" class="card"><div class="preview">${m.colors.map(c => `<div class="swatch" style="background:${c}"></div>`).join('')}</div><div class="info"><div class="name">${m.name}</div><div class="desc">${m.desc}</div></div></a>`).join('')}
    </div>
    <div class="meta">Local: <code>http://localhost:${PORT}</code> · ${HOST === '0.0.0.0' ? `Network: <code>http://${getLocalIP()}:${PORT}</code>` : 'Local preview'}</div>
  </div>
</body>
</html>`);
});

const server = app.listen(PORT, HOST, () => {
  console.log(`Mockup server: http://localhost:${server.address().port}`);
  if (HOST === '0.0.0.0') {
    console.log(`Network: http://${getLocalIP()}:${server.address().port}`);
  }
});
server.on('error', error => {
  console.error(`Could not start the mockup server: ${error.message}`);
  process.exitCode = 1;
});
```

## Naming Conventions

| Phase | Pattern | Example |
|-------|---------|---------|
| Style exploration | `{style-name}.html` | `retro-terminal.html` |
| Style iteration | `{style-name}-v2.html` | `terminal-minimal-v2.html` |
| Page template | `{page-type}.html` | `post.html`, `about.html` |
| Section exploration | `{section}-{variant}.html` | `projects-file-tree.html` |
| Section iteration | `{section}-{variant}-v2.html` | `projects-file-tree-v2.html` |

## Workflow Rules

1. **Know your phase** — Don't put section explorations in the root mockups folder
2. **Never overwrite** — Create new files for iterations (`-v2`, `-v3`)
3. **Shared styles in Phase 2+** — Use a `styles.css` for the chosen direction
4. **Document decisions** — Log sessions in `docs/logs/`
5. **Check the preview before answering** — Open the gallery and at least one mockup in the browser
6. **Refresh the gallery** — New and moved HTML files are discovered automatically
7. **Restart after changes** — Kill and restart the server after updating `server.js`

## Updating the Gallery Index

The server discovers HTML files in `mockups/` and its subfolders on each gallery request. Refresh the page after adding, moving, or removing a mockup.

Optionally add a `mockupMeta` entry in `server.js` for colors and a description. Use the path relative to `mockups/`, without `.html`, as its key. For example, use `terminal-v2-site/home` for `mockups/terminal-v2-site/home.html`. Restart the server after editing `server.js`.

## Mockup Best Practices

### Phase 1 Mockups (Style Exploration)
- Self-contained HTML with embedded CSS
- Show the full vibe: colors, typography, effects
- Include enough content to judge the aesthetic
- No external dependencies (except fonts)

### Phase 2+ Mockups (Templates & Sections)
- Link to shared `styles.css`
- Focus on layout and content structure
- Real-ish content (not lorem ipsum if possible)
- Mobile-responsive

### Color Palette
Define 4-5 key colors:
```css
:root {
  --bg: #0d120d;
  --text: #6b8c5a;
  --accent: #9DFF20;
  --muted: #3d5a30;
}
```

### Common Effects

**CRT Scanlines:**
```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background: repeating-linear-gradient(0deg, rgba(0,0,0,0.15), rgba(0,0,0,0.15) 1px, transparent 1px, transparent 2px);
  pointer-events: none;
  z-index: 1000;
}
```

**Blinking Cursor:**
```css
.cursor {
  display: inline-block;
  width: 0.6em;
  height: 1em;
  background: var(--accent);
  animation: blink 1s step-end infinite;
}
@keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
```

## Tips

- **Iterate fast** — Don't perfect, explore
- **Test on phone** — Start with `HOST=0.0.0.0 npm start` and use the network URL
- **Commit often** — Git tracks your exploration
- **Choose a free port** — If port 3000 is busy, use `PORT=3001 npm start`
- **Update README** — Keep project docs current with the chosen direction
