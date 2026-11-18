---
name: design-tokens
description: Design token system creation, validation, and transformation following the W3C DTCG 2025.10 specification. Use when working with design tokens, creating token files, validating token structures, transforming tokens for multiple platforms, implementing theming systems, or analyzing/converting tokens from design systems like IBM Carbon, Salesforce Lightning, Google Material, or Shopify Polaris. Covers naming conventions, three-tier architecture, token types, aliasing, and build tool configuration.
---

# Design Tokens

Design token creation and management following the W3C DTCG 2025.10 specification.

## Core Principles

**Three-tier architecture:**
1. **Primitive tokens** - Raw values without context (`color.blue.500`)
2. **Semantic tokens** - Intent-based aliases (`color.background.brand`)
3. **Component tokens** - Specific component styling (`button.primary.background`)

**Why:** Enables theming, maintains consistency, separates concerns.

## Decision Framework

```
Creating a token system?

  ├─ Need raw color/spacing/type values?
  │  └─ Create primitive tokens (see Token Types below)
  │
  ├─ Need to express design intent?
  │  └─ Create semantic tokens referencing primitives
  │
  ├─ Need component-specific styling?
  │  └─ Create component tokens referencing semantics
  │
  ├─ Need theming (light/dark, multi-brand)?
  │  └─ Same semantic names, different primitive values per theme
  │
  └─ Need multi-platform output?
     └─ Use Style Dictionary (see references/build-tools.md)
```

## Quick Reference

**W3C DTCG Spec:** See `references/w3c-dtcg-spec.md` - Complete format specification, token types, aliasing syntax.

**Naming Conventions:** See `references/token-naming.md` - CTI pattern, hierarchy structures, theming patterns.

**Major Systems:** See `references/major-systems.md` - IBM Carbon, Salesforce Lightning, Google Material, Shopify Polaris implementations.

**Token Types:** See `references/token-types.md` - All 13 DTCG token types with examples.

**Build Tools:** See `references/build-tools.md` - Style Dictionary, Tokens Studio configuration.

---

## Workflow 1: Create New Token System

### 1. Define Primitives

Start with raw values. Use DTCG format:

```json
{
  "color": {
    "$type": "color",
    "blue": {
      "500": {
        "$value": { "colorSpace": "srgb", "components": [0, 0.4, 0.8] }
      }
    }
  },
  "space": {
    "$type": "dimension",
    "4": { "$value": { "value": 16, "unit": "px" } }
  }
}
```

### 2. Create Semantic Layer

Reference primitives with curly brace syntax:

```json
{
  "color": {
    "background": {
      "brand": { "$value": "{color.blue.500}" },
      "surface": { "$value": "{color.neutral.50}" }
    },
    "text": {
      "primary": { "$value": "{color.neutral.900}" }
    }
  }
}
```

### 3. Add Component Tokens (Optional)

For complex systems, add component-specific tokens:

```json
{
  "button": {
    "primary": {
      "background": { "$value": "{color.background.brand}" },
      "text": { "$value": "{color.text.inverse}" }
    }
  }
}
```

### 4. Configure Build Tool

See `references/build-tools.md` for Style Dictionary setup.

---

## Workflow 2: Implement Theming

### Light/Dark Mode

Create separate files with identical token names:

```
tokens/
├── primitives/
│   ├── colors.tokens.json      # Shared primitives
├── themes/
│   ├── light.tokens.json       # Light semantic values
│   └── dark.tokens.json        # Dark semantic values
```

Both theme files define the same semantic tokens with different primitive references:

```json
// light.tokens.json
{ "color": { "background": { "surface": { "$value": "{color.neutral.50}" } } } }

// dark.tokens.json
{ "color": { "background": { "surface": { "$value": "{color.neutral.900}" } } } }
```

### Multi-Brand

Override primitives per brand:

```
tokens/
├── brands/
│   ├── brand-a/primitives.json
│   └── brand-b/primitives.json
├── semantic/
│   └── colors.tokens.json      # Shared semantic layer
```

---

## Workflow 3: Validate Tokens

Use `scripts/validate_tokens.py` to check:
- Valid JSON structure
- Required DTCG properties (`$value`, `$type`)
- No circular references
- Valid alias paths

```bash
python scripts/validate_tokens.py tokens/
```

---

## DTCG Format Quick Reference

### File Format

- Extension: `.tokens` or `.tokens.json`
- MIME type: `application/design-tokens+json`
- Properties prefixed with `$`

### Core Properties

| Property | Required | Purpose |
|----------|----------|---------|
| `$value` | Yes | The token's value |
| `$type` | Inherited | Token type (color, dimension, etc.) |
| `$description` | No | Documentation |
| `$deprecated` | No | Mark for removal |
| `$extensions` | No | Vendor-specific data |

### Alias Syntax

```json
{ "semantic-token": { "$value": "{path.to.primitive}" } }
```

### Type Inheritance

Groups inherit `$type` to children:

```json
{
  "spacing": {
    "$type": "dimension",
    "sm": { "$value": { "value": 8, "unit": "px" } },
    "md": { "$value": { "value": 16, "unit": "px" } }
  }
}
```

---

## Token Types at a Glance

| Type | `$type` | Example Value |
|------|---------|---------------|
| Color | `color` | `{ "colorSpace": "srgb", "components": [0, 0.4, 0.8] }` |
| Dimension | `dimension` | `{ "value": 16, "unit": "px" }` |
| Font Family | `fontFamily` | `["Inter", "sans-serif"]` |
| Font Weight | `fontWeight` | `700` or `"bold"` |
| Duration | `duration` | `{ "value": 200, "unit": "ms" }` |
| Cubic Bézier | `cubicBezier` | `[0.4, 0, 0.2, 1]` |
| Number | `number` | `1.5` |
| Typography | `typography` | Composite (see references) |
| Shadow | `shadow` | Composite (see references) |
| Border | `border` | `{ "color": {...}, "width": {...}, "style": "solid" }` |
| Gradient | `gradient` | Array of color stops |
| Transition | `transition` | `{ "duration": {...}, "timingFunction": [...] }` |
| Stroke Style | `strokeStyle` | `"solid"` or `{ "dashArray": [...] }` |

See `references/token-types.md` for complete examples.

---

## Naming Conventions

**CTI Pattern:** Category / Type / Item
```
color.background.primary
spacing.padding.medium
```

**Extended Pattern:** Namespace / Category / Element / Variant / State
```
acme-color-button-primary-hover
```

**Avoid:**
- Abbreviations (`bg` → `background`)
- Platform-specific terms (`ios-blue`)
- Magic numbers in semantic names (`blue-500` is primitive, not semantic)

See `references/token-naming.md` for complete guide.

---

## Common Patterns

### Spacing Scale (4px base)

```json
{
  "space": {
    "$type": "dimension",
    "0": { "$value": { "value": 0, "unit": "px" } },
    "1": { "$value": { "value": 4, "unit": "px" } },
    "2": { "$value": { "value": 8, "unit": "px" } },
    "4": { "$value": { "value": 16, "unit": "px" } },
    "8": { "$value": { "value": 32, "unit": "px" } }
  }
}
```

### Color Tonal Scale

```json
{
  "color": {
    "$type": "color",
    "blue": {
      "50": { "$value": { "colorSpace": "srgb", "components": [0.93, 0.96, 1] } },
      "500": { "$value": { "colorSpace": "srgb", "components": [0.13, 0.59, 0.95] } },
      "900": { "$value": { "colorSpace": "srgb", "components": [0.05, 0.28, 0.63] } }
    }
  }
}
```

---

## Key Reminders

1. **Three tiers** - Primitive → Semantic → Component
2. **DTCG format** - Use `$value`, `$type`, curly brace aliases
3. **Alias depth** - Keep to 2-3 levels max
4. **Theme by swap** - Same names, different values
5. **Platform-agnostic** - Let build tools handle transforms

## Templates

See `assets/templates/` for starter token files:
- `primitives.tokens.json` - Base color, spacing, typography
- `semantic.tokens.json` - Intent-based tokens
- `style-dictionary.config.js` - Build configuration

## When Stuck

1. **Format questions?** → `references/w3c-dtcg-spec.md`
2. **Naming issues?** → `references/token-naming.md`
3. **How do others do it?** → `references/major-systems.md`
4. **Token type syntax?** → `references/token-types.md`
5. **Build setup?** → `references/build-tools.md`
