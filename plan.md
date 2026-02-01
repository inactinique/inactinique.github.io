# Custom Academic Theme Plan

## Overview
Build a from-scratch Jekyll theme focused on text readability, with dark/light mode toggle, replacing the current Dinky theme.

---

## Design Specifications

### Typography
- **Body text:** Inter (variable font, excellent screen legibility)
- **Headings:** EB Garamond (elegant, oldstyle figures enabled)
- **Numbers:** Oldstyle figures via `font-feature-settings: "onum"`
- **Base size:** 18-20px for comfortable reading
- **Line height:** ~1.6-1.7 for body text
- **Measure:** ~65 characters per line (centered narrow column)

### Color System

**Light Mode:**
- Background: #f8f8f8 (soft off-white)
- Text: #1a1a1a (soft black)
- Muted text: #555555
- Links: #1a1a1a with underline, hover slightly lighter

**Dark Mode:**
- Background: #1a1a1a (soft black)
- Text: #e8e8e8 (soft white)
- Muted text: #999999
- Links: #e8e8e8 with underline, hover slightly brighter

### Layout
- Centered content column, max-width ~38rem (~600px)
- Generous vertical rhythm (whitespace between elements)
- Minimal header: site title + dark/light toggle (minimal switch, no icons)
- No sidebar, no images
- Clean footer with minimal info

### Dark/Light Toggle Behavior
1. On load: detect `prefers-color-scheme` system preference
2. Store user override in `localStorage`
3. Toggle button in header (visible at top)
4. Same toggle floats/sticks when user scrolls past header
5. Smooth transition between modes

---

## Files to Create/Modify

### Remove/Replace
- `assets/css/style.scss` — rewrite entirely (remove Dinky import)

### Modify
- `_config.yml` — remove `theme: jekyll-theme-dinky` line
- `_layouts/default.html` — rewrite layout structure

### Create
- `assets/css/theme.css` — new custom CSS (or keep as .scss if preferred)
- `assets/js/theme-toggle.js` — dark/light toggle logic
- `_includes/header.html` — reusable header with toggle
- `_includes/footer.html` — reusable footer

---

## Implementation Steps

### Step 1: Typography & Base CSS
- Set up CSS custom properties (variables) for colors, fonts, spacing
- Import Google Fonts (Inter + EB Garamond)
- Define base typography: body, headings (h1-h6), paragraphs, lists, blockquotes, code
- Ensure oldstyle figures via `font-feature-settings: "onum"`

### Step 2: Color System & Dark Mode
- Define light mode as default via CSS variables on `:root`
- Define dark mode variables on `[data-theme="dark"]` or `.dark`
- Add `@media (prefers-color-scheme: dark)` for auto-detection
- Ensure smooth color transitions

### Step 3: Layout Structure
- Centered container with max-width
- Header: site title (left), toggle button (right)
- Main content area with proper vertical spacing
- Minimal footer

### Step 4: Toggle JavaScript
- On page load: check localStorage, else check system preference
- Apply theme class/attribute to `<html>` or `<body>`
- Toggle button switches theme and saves to localStorage
- Floating toggle: use `position: sticky` or IntersectionObserver

### Step 5: Update Jekyll Files
- Rewrite `_layouts/default.html` with new structure
- Create `_includes/header.html` and `_includes/footer.html`
- Update `_config.yml` to remove Dinky theme reference
- Ensure all existing Markdown content still renders correctly

### Step 6: Polish & Test
- Test on mobile/tablet/desktop
- Test dark/light in both system modes
- Verify presentations (prez/) are unaffected (they use reveal.js)
- Check GitHub Pages build works

---

## Verification
1. Run `bundle exec jekyll serve` locally to preview
2. Toggle dark/light mode — should transition smoothly
3. Check system preference detection (change OS setting)
4. Verify toggle persists on page reload (localStorage)
5. Check narrow column centering at various widths
6. Confirm prez/ pages still work with reveal.js
7. Push to GitHub, verify Pages build succeeds
