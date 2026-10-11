# Jagoron Digital Guide

One source builds **both** the website (GitHub Pages) and the PDF, so they always match.

```
docs/index.html                     <- the website (single file, no external requests)
docs/downloads/Jagoron-Digital-Guide.pdf   <- the PDF (linked from the site's "Download" buttons)
config.json                         <- the only file you must edit (link, contacts)
build.py  style.css  app.js         <- content, design, small script
```

## 1. Publish on GitHub Pages (free, about 5 minutes)

1. Create a **public** repository on GitHub (for example `jagoron`).
2. Upload everything in this folder (drag and drop works on github.com).
3. Repository **Settings > Pages > Build and deployment**: Source = *Deploy from a branch*, Branch = `main`, Folder = `/docs`. Save.
4. After a minute your site is live at `https://YOUR-USERNAME.github.io/jagoron/`.
5. The PDF is at `https://YOUR-USERNAME.github.io/jagoron/downloads/Jagoron-Digital-Guide.pdf` (stable link, safe to print).

## 2. Add your link and the QR code

1. Put the live address in `config.json` as `"site_url"`.
2. Run `pip install -r requirements.txt` then `python build.py`.
3. This adds the link and a **QR code** (`docs/qr.svg`) to the site and the PDF. Use `docs/qr.svg` on the banners, leaflet back cover and table tents.
4. Commit and upload the changed `docs/` files.

## 3. Before you share it publicly

The site shows a yellow **DRAFT** banner until the contacts are ready.

1. In `config.json`, fill each `campus_contacts` entry.
2. Check every number in `national_contacts` yourself (call or check the official page), then set `"verified": true`.
3. Run `python build.py --release`. It refuses to build while anything is unverified or empty, so a wrong number cannot go out by accident.

## Editing

- Text and lists: `build.py`. Colours and layout: `style.css`. Rebuild with `python build.py`.
- No Python? Open `docs/index.html` in Chrome and use *Print > Save as PDF*. The print layout is built in.
- The page works without JavaScript (quiz answers are shown). Nothing the student ticks or taps is stored or sent anywhere. The page loads no fonts, trackers or external files, so it is light on mobile data.

## Alternatives to GitHub Pages

| Option | Good for |
|---|---|
| **GitHub Pages** (recommended) | Free, version history, stable links, easy to hand over |
| Cloudflare Pages / Netlify | Drag-and-drop the `docs` folder; fast worldwide; easy custom domain |
| Custom domain (for example `jagoron.wub.edu.bd`) | A link students can read aloud. Ask the university IT team; works with any option above |
| Google Drive link for the PDF | Backup only; the link is long and can break if sharing changes |
