# ScyllaDB Design System tokens (vendored)

Source: the `dist-ds/` bundle of the [scylladb-design-system](https://github.com/scylladb/scylladb-design-system)
repo (`npm run build:ds`). Version in `VERSION`.

What is vendored and why:

| File | Purpose |
|---|---|
| `_colors.scss` | `--color-*` palette (OKLCH) |
| `_semantic.scss` | semantic tokens per theme: `:root` (light), `[data-theme="dark"]`, `[data-theme="scylla"]` |
| `_borders.scss` | `--radius-*`, `--border-w` |
| `_spacing.scss` | `--spacer-*` |
| `_elevation.scss` | `--shadow-*` |
| `_typography.scss` | `@font-face` for Roboto Flex / Roboto Mono + `--type-*` ramp |
| `_iconfont.scss` | `@font-face` for `fonticon` + `$icons` map, `--glyph-*` vars and `.icon-<name>::before` rules |

The icon font is the design system's: the docs-specific glyphs (`icon-docs-*`)
live in the design-system repo under `resources/icons/docs/`, so the theme no
longer builds its own font. The drawings are Remix Icon (4.8.0, Apache-2.0) under
the design system's names, plus a few hand-drawn / kept glyphs; the design system
records the source of every icon in `resources/icons/sources.json`. Codepoints are
stable there (`resources/icons/codepoints.json`), but the theme still references
glyphs by name only (`map.get($icons, "…")`, `var(--glyph-<name>)`). Most icons
ship a line + fill pair; `.icon-duo` renders them two-tone (not used by the theme).
`icon-scylla` was dropped in favour of the design system's `icon-scylla-filled`
(same drawing).

Not vendored on purpose: `_tokens.scss` (app-shell layout/z-index values) and
every component partial.

## How to update

```sh
DS=../scylladb-design-system/dist-ds
for f in _colors _semantic _borders _spacing _elevation _typography _iconfont; do
  cp "$DS/scss/$f.scss" src/css/vendor/scylladb-ds/
done
cp "$DS/VERSION" src/css/vendor/scylladb-ds/VERSION
cp "$DS/fonts/roboto-flex.woff2" "$DS/fonts/roboto-mono.woff2" src/fonts/
cp "$DS/fonts/fonticon.ttf" "$DS/fonts/fonticon.woff" "$DS/fonts/fonticon.eot" src/fonts/
# the bundle references fonts as ../resources/fonts/; the theme keeps them in src/fonts/
sed -i "s#url('../resources/fonts/#url('../fonts/#g" src/css/vendor/scylladb-ds/_typography.scss
# same for the icon font (and drop its cache-buster: webpack inlines the files)
sed -i -E 's#url\("\.\./resources/icons/(fonticon\.[a-z]+)\?v=[0-9]+"\)#url("../fonts/\1")#g' src/css/vendor/scylladb-ds/_iconfont.scss
# the --logo-* tokens point at DS logo assets the theme does not ship (it has its own logos)
sed -i '/--logo-[a-z]*: url(/d' src/css/vendor/scylladb-ds/_semantic.scss
```

Then `npm run build`. The only local changes to the generated files are the
`sed` rewrites above.

## Current state

Two partials are ahead of the 0.6.76 bundle and were copied straight from the
design-system source instead of `dist-ds/`:

- `_colors.scss`: gray ramp update (2026-11-09), not yet built into a bundle.
- `_iconfont.scss` + `src/fonts/fonticon.*`: from the design-system branch
  `remix-icons` (on top of `docs-icons`, 2026-11-10): the Remix Icon redraw, the
  22 `docs-*` glyphs, stable codepoints, 230 icons / 361 glyphs.

Once both land upstream and `npm run build:ds` is re-run there, the sync steps
above bring everything back in line.
