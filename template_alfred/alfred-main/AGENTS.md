**# Alfred — AI / agent context

**Alfred** (`@lexington/alfred`) is a Lexington Themes Astro template for a **SaaS / business marketing site**: a feature-led homepage, pricing, customer stories, integrations directory, help center, blog, changelog, team profiles, auth-style form pages, and legal/info pages—plus a **design system** area under `/system/*`.

**Publisher:** [Lexington Themes](https://lexingtonthemes.com/)  
**Design rules:** [.cursor/skills/alfred-design/SKILL.md](./.cursor/skills/alfred-design/SKILL.md) - read before creating or changing any UI.  
**Theme page:** [Alfred template](https://lexingtonthemes.com/templates/alfred)  
**Docs:** [Documentation](https://lexingtonthemes.com/documentation)  
**Support:** [Support](https://lexingtonthemes.com/legal/support/)

## Tech stack

| Area | Details |
|------|---------|
| Framework | **Astro** `^6.0.0` |
| Styling | **Tailwind CSS** `^4.1.18` via `@tailwindcss/vite` in `astro.config.mjs` |
| MDX | `@astrojs/mdx` `^5.0.0` |
| RSS | `@astrojs/rss` `^4.0.17` (`src/pages/rss.xml.js`) |
| Sitemap | `@astrojs/sitemap` `^3.7.1` |
| SEO component | `@lexingtonthemes/seo` `^0.1.0` (used in `src/components/fundations/head/Seo.astro`) |
| Tailwind plugins (npm) | `@tailwindcss/forms`, `@tailwindcss/typography`, `tailwind-scrollbar-hide` |
| Content | `astro:content` + `defineCollection` / `glob` loader in `src/content.config.ts`; schemas use `z` from `astro/zod` |
| Markdown | `markdown.drafts: true`; Shiki theme `github-dark`; root `shikiConfig.wrap: true` |
| Site URL | `site: 'https://yourdomain.com'` in `astro.config.mjs` — replace for production |
| Path alias | `@/*` → `src/*` (`tsconfig.json`) |

## Folder map

| Path | Role |
|------|------|
| `src/pages/` | File-based routes (see [Routing](#routing-conventions)) |
| `src/layouts/` | `BaseLayout.astro`, section layouts (`BlogLayout`, `ChangelogLayout`, …) |
| `src/components/` | UI: `fundations/` (head, elements, containers, icons, scripts), `global/` (nav/footer), `features/`, `blog/`, etc. |
| `src/content/` | MD/MDX per collection (see below) |
| `src/content.config.ts` | Collection definitions and Zod schemas |
| `src/styles/global.css` | Tailwind import, `@theme` color/font tokens, `@plugin` typography + forms |
| `src/images/` | Optimized assets: `assets/`, `blog/`, `team/`, `integrations/`, `customers/`, `brands/` |
| `public/` | **Not present in this repo.** `Favicons.astro` still references standard root paths (e.g. `/favicon.ico`)—add files here when needed |

## Content collections

All collections load `**/*.(md|mdx)` from a folder under `src/content/`. Use **`image()`** fields with paths such as `url: "/src/images/..."` (see existing entries).

### `helpcenter`

- **Folder:** `src/content/helpcenter/`
- **Required frontmatter:** `title` (string), `intro` (string)
- **Images:** none in schema
- **Template:** copy structure from `src/content/helpcenter/1.md`

### `changelog`

- **Folder:** `src/content/changelog/`
- **Required frontmatter:** `page` (string), `description` (string), `pubDate` (date), `image: { url: image(), alt }`
- **Images:** `image.url` via `image()`
- **Template:** `src/content/changelog/1.md`

### `infopages` (legal / info)

- **Folder:** `src/content/infopages/`
- **Required frontmatter:** `page` (string), `pubDate` (date)
- **Images:** none in schema
- **Template:** `src/content/infopages/terms.md`
- **URLs:** `/infopages/[slug]` where `slug` is the file basename (e.g. `terms`, `privacy`, `dpa`)

### `integrations`

- **Folder:** `src/content/integrations/`
- **Required frontmatter:** `email`, `integration`, `description`, `permissions` (string[]), `details` ({ `title`, `value`, optional `url` }[]), `logo: { url: image(), alt }`, `tags` (string[])
- **Images:** `logo.url` via `image()`
- **Template:** `src/content/integrations/1.md`

### `team`

- **Folder:** `src/content/team/`
- **Required frontmatter:** `name`, `image: { url: image(), alt }`
- **Optional:** `role`, `bio`, `socials: { twitter?, website?, linkedin?, email? }`
- **Template:** `src/content/team/david-lee.md`
- **Blog link:** `posts` frontmatter `team` must be the **entry id** (filename without extension) of a team member, e.g. `david-lee` → `/team/david-lee`

### `posts` (blog)

- **Folder:** `src/content/posts/`
- **Export name:** collection key is `posts` (variable `postsCollection` in config)
- **Required frontmatter:** `title`, `pubDate`, `description`, `team` (string — team entry id), `image: { url: image(), alt }`, `tags` (string[])
- **Images:** `image.url` via `image()`
- **Template:** `src/content/posts/1.md`

### `customers`

- **Folder:** `src/content/customers/`
- **Required frontmatter:** `customer`, `avatar: { url: image(), alt }`, `challengesAndSolutions` ({ `title`, `content` }[]), `results` (string[]), `about`, `details` (`Record<string, string>`), `logo: { url: image(), alt }`
- **Optional:** `bgColor`, `ctaTitle`, `testimonial`, `partnership`
- **Images:** `avatar.url`, `logo.url` via `image()`
- **Template:** `src/content/customers/1.md`

## Routing conventions

| Content / area | List / hub URL | Entry URL pattern |
|----------------|----------------|-------------------|
| Blog | `/blog/home` | `/blog/posts/[slug]` — `src/pages/blog/posts/[...slug].astro` |
| Blog tags | `/blog/tags` | `/blog/tags/[tag]` |
| Changelog | `/changelog/home` | `/changelog/[slug]` |
| Customers | `/customers/home` | `/customers/[slug]` |
| Integrations | `/integrations/home` | `/integrations/[slug]` |
| Help center | `/helpcenter/home` | `/helpcenter/[slug]` |
| Team | `/team/home` | `/team/[slug]` |
| Infopages | — | `/infopages/[slug]` |
| RSS | `/rss.xml` | `src/pages/rss.xml.js` — **note:** feed `link` values use `/posts/...`; listing components use `/blog/posts/...`. Align `site`, titles, and paths when shipping. |
| Forms | — | `/forms/sign-in`, `sign-up`, `reset`, `book-demo` |
| System / design kit | — | `/system/overview`, `colors`, `typography`, `buttons`, `links` |
| Other static pages | — | `/`, `/about`, `/pricing`, `/404` |

Dynamic segments use **`[...slug]`** with `getStaticPaths` + `params.slug = entry.id` (content file basename without extension).

## Customization guide

1. **Site URL / domain**  
   - Set `site` in `astro.config.mjs`.  
   - Update placeholder URLs in `src/components/fundations/head/Seo.astro` (currently static `yourwebsite.com` / generic title).  
   - Align `src/pages/rss.xml.js` (`title`, `description`, `site`, item `link`).

2. **Brand colors & typography**  
   - **`src/styles/global.css`**: `@theme` palette (`--color-*`, `--font-sans`), prose-related tokens, marquee keyframes.  
   - **`src/components/fundations/head/Fonts.astro`**: Inter from `https://rsms.me/inter/inter.css`.

3. **Navigation & footer**  
   - `src/components/global/Navigation.astro`  
   - `src/components/global/Footer.astro`

4. **Global shell**  
   - **`src/layouts/BaseLayout.astro`**: imports `global.css`, wraps with `Navigation` + `Footer`, renders `<slot />`.  
   - **`src/components/fundations/head/BaseHead.astro`**: composes `Seo`, `Meta`, `Fonts`, `Favicons`, `FuseJS`, `KeenSlider`.

## Commands

From README (run at repo root):

| Command | Action |
|---------|--------|
| `npm install` | Install dependencies |
| `npm run dev` | Dev server |
| `npm run build` | Production build → `./dist/` |
| `npm run preview` | Preview production build |
| `npm run astro ...` | Astro CLI |

## Guardrails

- **Do not rename** `src/components/fundations/` — the folder is spelled **`fundations`** (not “foundations”); imports depend on it.
- **Do not widen** Zod schemas in `src/content.config.ts` without updating every layout/page that reads `entry.data` and any related components.
- For `image()` fields, keep paths compatible with existing entries (typically under `src/images/...`).
- Prefer **small, pattern-matching edits** over broad refactors.

---

*Generated for this repository only; infer changes from the tree if something drifts.*
**