---
name: alfred-design
description: Alfred's design system - typography, color, spacing, and component rules. Use whenever creating or modifying UI in this theme (new pages, sections, components) so the result matches Alfred's visual language.
---

# Alfred design system

Alfred is a SaaS marketing theme with an editorial-playful voice: big confident
type, soft tinted color panels, sharp corners, and generous whitespace. When
you build new UI here, it should be indistinguishable from the existing pages.

## Design personality

- Confident and calm: large headings, short lines (`max-w-xl`), lots of air.
- Playful color, serious structure: soft pastel panels carry personality;
  the grid and type stay disciplined.
- Sharp, print-like edges: this theme almost never rounds corners.

## Typography

Font is **Inter / InterVariable** (configured in `src/styles/global.css` with
OpenType features: square punctuation, slashed zero, tabular numbers). Never
introduce another font.

Always use the `Text` component (`@/components/fundations/elements/Text.astro`)
instead of raw heading tags with ad-hoc sizes:

- Page hero title: `tag="h1" variant="displayLG"` + `font-medium tracking-tight text-balance`, constrained with `max-w-xl` or similar.
- Section heading: `tag="h2" variant="displaySM"` + `font-medium tracking-tight text-balance`.
- Card / feature title: `tag="h3" variant="textXL"` + `font-medium`.
- Lead paragraph: `variant="textLG"`, body: `variant="textBase"`, captions: `variant="textSM"`.

Heading color is `text-base-800` on white, or the section hue's `-800` step
inside a tinted panel (e.g. `text-blue-800` on `bg-blue-50`). Body text is
`text-base-600` (or `text-base-500` in prose).

Do not use font weights above `font-medium` for headings. No `font-bold`
display type anywhere.

## Color system

All colors are custom low-chroma oklch palettes defined in
`src/styles/global.css` under `@theme`: `yellow`, `purple`, `green`, `teal`,
`rose`, `blue`, plus the neutral `base` scale. Use only these token scales -
never Tailwind default palette names that aren't defined there, never hex
values in markup.

Usage rules:

- Page background is white; neutral text uses the `base` scale.
- Sections may sit in a tinted panel: `bg-{hue}-50` (or `-100`) container
  with headings in `text-{hue}-800`. One hue per panel; body text stays
  `text-base-600`.
- **Rotate hues between adjacent sections** (homepage order: blue, rose,
  green). Never two consecutive panels in the same hue.
- Accent for primary actions is `teal-600` (see Button). Black is the
  default button color, not a hue.
- Dark surfaces use `base-800`/`base-900` with white text, sparingly.

## Layout and spacing

- Every section is `<section>` wrapping a `Wrapper` (`@/components/fundations/containers/Wrapper.astro`):
  `variant="standard"` (max-w 1440px, `px-8 md:px-12`) for pages,
  `variant="narrow"` for focused forms, `variant="prose"` for markdown bodies.
- Section vertical padding is `py-8` on the Wrapper; heroes use large top
  padding (`pt-48 ... lg:pt-82`) because the nav floats.
- Tinted panels use `p-8 lg:p-12` inside the Wrapper.
- The spacing rhythm between blocks inside a section is `mt-12`; between a
  title and its supporting paragraph `mt-2` to `mt-4`; between list items in
  grids `gap-8`.
- Feature grids: `grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3`
  (or the 4-col split with an offset lead paragraph, see `Feature1.astro`).
- Images run full-bleed inside their panel: `class="w-full"`, explicit
  `width`/`height`, no rounding, no shadow.

## Components

Reuse these before writing anything new:

- **Button** (`fundations/elements/Button.astro`): variants `default`
  (black, white text), `accent` (teal-600), `muted` (white with `base-200`
  ring); sizes `xs`-`xl`; `isLink` + `href` renders an anchor; `iconOnly`
  with `onlyIconSize` for icon buttons. Buttons are **square-cornered** with
  `ring` borders - do not add `rounded-*` classes to them.
  **Width is a per-use decision** (the component is intentionally
  unopinionated and stretches to its container): standalone CTAs in
  sections get `w-fit`; form submits and pricing-card CTAs get `w-full`;
  buttons in a flex row need no width class. Match the nearest existing
  example when unsure.
  **Width:** the component renders a block-level `flex`, so it stretches to
  fill its container. Standalone CTAs must add `w-fit` (or sit in a
  `flex items-start` parent). Full-width buttons (`w-full`) are only for
  form submits and pricing-card CTAs.
- **Text**: the only sanctioned type scale (see Typography).
- **Kicker** (`assets/Kicker.astro`): the square `size-10` single-letter
  chip that opens a section; color it `bg-{hue}-800 text-white` matching the
  panel hue.
- **Wrapper**: the only page-width container. Don't hand-roll
  `max-w-* mx-auto` wrappers.
- Icons live in `fundations/icons/` as individual Astro components; add new
  ones there in the same stroke style rather than importing icon packs.

## Corners, borders, shadows

- Default is **no border radius**. Small radii (`rounded`, `rounded-md`)
  appear only on tiny UI (badges, inputs); `rounded-full` only for avatars
  and pills. Never round panels, images, or buttons.
- Borders are `ring`/`ring-1` in `base-200`-`base-300`, not heavy borders.
- No drop shadows on cards or panels; the tinted background does the
  separation work.

## Voice and copy

Copy is witty but concise (see existing feature sections). Headlines are
statements, not questions. Sentence case everywhere - no Title Case, no
exclamation marks, no emoji.

## Do / Don't

Do:

- Copy an existing section's structure before inventing a new layout.
- Keep hue-tinted panels to one hue and rotate hues across the page.
- Use `text-balance` on headings and `max-w-*` to keep line lengths short.

Don't:

- Don't round corners on buttons, panels, or images.
- Don't introduce new fonts, colors outside `@theme`, gradients, or shadows.
- Don't exceed `font-medium` on display type.
- Don't use default Tailwind `slate`/`gray`/`zinc` classes - the neutral
  scale here is `base-*`.
- Don't inline a heading with raw classes when `Text` has a variant for it.

## Quality check before finishing

1. Fonts, colors, and spacing all come from existing tokens and match a
   sibling section.
2. New section reads correctly at `sm`, `md`, and `lg` breakpoints.
3. Headings use `Text` variants; buttons use `Button` variants.
4. No new dependencies, no unused imports, minimal diff.
