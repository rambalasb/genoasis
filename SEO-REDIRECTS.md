# Legacy URL Redirects (SEO Audit)

This site is hosted on GitHub Pages, which does not process `.htaccess` or
serve real server-side 301s. The `.htaccess` file that used to live in this
repo listed a redirect map, but none of its rules ever executed on the live
site — GitHub Pages ignores Apache config entirely. It has been removed.

## 2026-09-19: legacy redirect folders removed

The 14 folders below used to exist purely as redirect stubs — a static
`index.html` combining `noindex`, `rel="canonical"`, `meta refresh`, and a
`window.location.replace()` JS redirect to the current page (the standard
client-side redirect pattern for a host with no server-side rewrite support).

They were deleted to keep the site to a minimal set of pages. This was a
deliberate tradeoff: **any visitor who still has one of these old URLs
bookmarked, follows an old external backlink to one, or clicks a stale
cached search result will now get a hard 404** (via `404.html`) instead of
being forwarded to the current page. Traffic to these paths was not checked
against Analytics/Search Console before removal — if search-visible traffic
turns out to still be hitting them, restore the mapping below as redirect
stubs again.

| Old path | Used to redirect to |
|---|---|
| `/membranes/` | `/consumables-spares/` |
| `/frpmedia/` | `/consumables-spares/` |
| `/filters/` | `/consumables-spares/` |
| `/sandmedia/` | `/consumables-spares/` |
| `/valves/` | `/consumables-spares/` |
| `/chemicals/` | `/ro-cooling-water-chemicals/` |
| `/disinfectants/` | `/ro-cooling-water-chemicals/` |
| `/wastewater/` | `/stp-etp-biological-media/` |
| `/pneumatic-products/` | `/pneumatic-automation/` |
| `/instruments/` | `/pneumatic-automation/` |
| `/pumps/` | `/sludge-dewatering-pumping/` |
| `/atmospheric-water-generators/` | `/` (homepage) |
| `/nanobubble-technology/` | `/` (homepage) |
| `/dunnage-air-bags/` | `/` (homepage) |

None of these paths were linked to from anywhere in the current site (nav,
footer, content) or listed in `sitemap.xml`.

## Recreating a redirect

If you need to bring one of these back (e.g. Analytics shows real traffic
still landing on an old path), create `<old-slug>/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Redirecting to <NEW PAGE TITLE> | Genoasis</title>
  <link rel="canonical" href="https://genoasis.com/<new-slug>/">
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="0; url=../<new-slug>/">
  <script>window.location.replace("../<new-slug>/");</script>
</head>
<body>
  <p>This page has moved. Redirecting to <a href="../<new-slug>/">NEW PAGE TITLE</a>. If you are not redirected automatically, please follow the link.</p>
</body>
</html>
```
