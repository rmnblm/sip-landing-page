# sip-landing-page

Static content for the Sip iOS app, served from this repo's `main` branch via
`raw.githubusercontent.com`. (A marketing site can be deployed on top of this later — GitHub Pages,
Cloudflare, etc.)

## What the app fetches

| Purpose | Path | Consumed by |
| --- | --- | --- |
| Exchange rates | `assets/currencies.json` | `CurrencyCache` (`C.baseURL`) |
| What's New | `whatsnew/ios/<version>/<lang>.md` | `WhatsNewService` (`C.whatsNewURL`) |

Base URLs in the app (`Sip/Core/Constants.swift`):

- `C.baseURL` → `https://raw.githubusercontent.com/rmnblm/sip-landing-page/main/assets/`
- `C.whatsNewURL` → `https://raw.githubusercontent.com/rmnblm/sip-landing-page/main/whatsnew/ios/`

> The **previously shipped** app fetches currencies from the old
> `rmnblm/sip-app-landing-page` repo (`master/assets/currencies.json`). That repo must stay alive as
> the fallback for already-installed builds — do not delete it.

## What's New

`WhatsNewService` presents release notes on launch:

- **First-ever launch** shows `whatsnew/ios/1.0/<lang>.md` (the welcome) — this is also what an
  existing user sees on their first launch of a build that introduced the feature, because the
  "last seen" marker starts empty.
- **After an upgrade**, the new version's notes are shown once, if published. Versions without a
  file show nothing.

### Publishing a version's notes

Create `whatsnew/ios/<version>/en.md` (plus other languages). `<version>` must match the app's
`CFBundleShortVersionString` exactly (e.g. `2.1`).

Supported markdown: `# Heading`, `## Subheading`, `![alt](https://…)` images (absolute URLs,
committed alongside the `.md`), paragraphs with inline `**bold**` / `*italic*`, and one optional
`[button: Title]` line that sets the dismiss-button label (defaults to "Continue").

The app prefers the user's language and falls back to `en.md`.
