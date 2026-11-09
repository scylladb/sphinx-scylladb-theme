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

Not vendored on purpose: `_iconfont.scss` (the theme keeps its own `fonticon`
build — it has 23 docs-specific glyphs the design system does not ship, and the
codepoints differ), `_tokens.scss` (app-shell layout/z-index values) and every
component partial.

## How to update

```sh
DS=../scylladb-design-system/dist-ds
for f in _colors _semantic _borders _spacing _elevation _typography; do
  cp "$DS/scss/$f.scss" src/css/vendor/scylladb-ds/
done
cp "$DS/VERSION" src/css/vendor/scylladb-ds/VERSION
cp "$DS/fonts/roboto-flex.woff2" "$DS/fonts/roboto-mono.woff2" src/fonts/
# the bundle references fonts as ../resources/fonts/; the theme keeps them in src/fonts/
sed -i "s#url('../resources/fonts/#url('../fonts/#g" src/css/vendor/scylladb-ds/_typography.scss
# the --logo-* tokens point at DS logo assets the theme does not ship (it has its own logos)
sed -i '/--logo-[a-z]*: url(/d' src/css/vendor/scylladb-ds/_semantic.scss
```

Then `npm run build`. The only local changes to the generated files are the two
`sed` rewrites above.

## Current state

`_colors.scss` is ahead of the 0.6.76 bundle: it was copied straight from the
design-system source (`scss/_colors.scss`, gray ramp update, 2026-11-09) before
`npm run build:ds` was re-run there. Once the bundle is rebuilt, the sync steps
above bring the two back in line.
