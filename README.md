# Prime Drivers Logistics — Website

Static HTML/CSS/JS site. No build step needed: open `index.html` in a browser,
or upload the whole folder to any host (Netlify, Vercel, cPanel, GitHub Pages).

## Files
- `index.html`: home page
- `services.html`, `equipment.html`, `about.html`, `contact.html`
- `dispatch-*.html`: one page per truck type (box truck, dry van, reefer, power only, hotshot, flatbed)
- `css/style.css`: all styles (colors are CSS variables at the top)
- `js/main.js`: loader, sticky header, mobile menu, dropdown, scroll animations, counters, FAQ, video popup
- `images/`: photos (placeholders cropped from the screen recording, so replace them with full-quality originals using the same file names)

## Common edits
- **Phone / WhatsApp number:** change `PHONE` and `WA` at the top of `build.py`, then run `python3 build.py` to regenerate every page.
  (Or search-and-replace `12792714680` and `+1 (279) 271-4680` in the HTML files.)
- **Header, footer, page text:** edit `build.py` and re-run it. That way every page stays in sync.
- **Video popup:** set the `data-video` URL on the play button in `index.html` (any YouTube embed link).
