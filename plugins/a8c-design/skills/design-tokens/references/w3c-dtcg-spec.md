# W3C Design Tokens Format Specification (DTCG 2025.10)

The Design Tokens Community Group published the first stable specification in October 2025. This reference covers the Format Module, Color Module, and key syntax rules.

## File Format

### Basics

- **Extension:** `.tokens` or `.tokens.json`
- **MIME type:** `application/design-tokens+json`
- **Encoding:** UTF-8
- **Format:** JSON with `$`-prefixed properties

### Specification Properties

All spec-defined properties use `$` prefix to distinguish from custom properties:

| Property | Location | Purpose |
|----------|----------|---------|
| `$value` | Token | The token's value (required for tokens) |
| `$type` | Token or Group | Declares the token type |
| `$description` | Token or Group | Human-readable documentation |
| `$deprecated` | Token | Marks token for removal (boolean or string message) |
| `$extensions` | Token or Group | Vendor-specific data (reverse domain keys) |
| `$root` | Group | Defines a token at group level |
| `$extends` | Group | Inherits from another group |

---

## Token Structure

### Basic Token

```json
{
  "token-name": {
    "$value": "the value",
    "$type": "the-type",
    "$description": "Optional documentation"
  }
}
```

### With Extensions

```json
{
  "brand-primary": {
    "$value": { "colorSpace": "srgb", "components": [0, 0.4, 0.8] },
    "$type": "color",
    "$extensions": {
      "com.figma": { "variableId": "VariableID:123" },
      "com.company.internal": { "approved": true }
    }
  }
}
```

### Deprecated Token

```json
{
  "old-token": {
    "$value": "{new-token}",
    "$deprecated": "Use 'new-token' instead. Will be removed in v3.0."
  }
}
```

---

## Groups

Any JSON object without `$value` is a group. Groups organize tokens hierarchically.

### Basic Group

```json
{
  "color": {
    "primary": { "$value": "#0066cc", "$type": "color" },
    "secondary": { "$value": "#6c757d", "$type": "color" }
  }
}
```

### Type Inheritance

Groups can set `$type` for all children:

```json
{
  "spacing": {
    "$type": "dimension",
    "$description": "Spacing scale based on 4px",
    "xs": { "$value": { "value": 4, "unit": "px" } },
    "sm": { "$value": { "value": 8, "unit": "px" } },
    "md": { "$value": { "value": 16, "unit": "px" } },
    "lg": { "$value": { "value": 24, "unit": "px" } }
  }
}
```

Children inherit `$type` unless they explicitly override it.

### The `$root` Property

Define a token at the same level as a group's children:

```json
{
  "button": {
    "$root": {
      "$value": { "value": 44, "unit": "px" },
      "$type": "dimension",
      "$description": "Default button height"
    },
    "small": { "$value": { "value": 32, "unit": "px" } },
    "large": { "$value": { "value": 56, "unit": "px" } }
  }
}
```

Accessing: `{button}` gets the root, `{button.small}` gets the child.

### The `$extends` Property

Groups can inherit from other groups with deep merge:

```json
{
  "base-button": {
    "padding": { "$value": { "value": 16, "unit": "px" }, "$type": "dimension" },
    "radius": { "$value": { "value": 4, "unit": "px" }, "$type": "dimension" }
  },
  "pill-button": {
    "$extends": "{base-button}",
    "radius": { "$value": { "value": 9999, "unit": "px" } }
  }
}
```

`pill-button` inherits `padding` from `base-button` but overrides `radius`.

---

## Aliasing (References)

### Syntax

Use curly braces with dot-notation paths:

```json
{
  "color": {
    "blue-500": { "$value": { "colorSpace": "srgb", "components": [0, 0.4, 0.8] }, "$type": "color" }
  },
  "semantic": {
    "brand-primary": { "$value": "{color.blue-500}" }
  }
}
```

### Rules

1. **References resolve to `$value`** - The alias gets the target's value
2. **Type inference** - Alias inherits type from target if not specified
3. **Chain depth** - Keep to 2-3 levels for maintainability
4. **No circular references** - Tools must detect and error

### Valid Reference Patterns

```json
{
  "a": { "$value": "{b}" },           
  "b": { "$value": "{c}" },           
  "c": { "$value": "#000" }           
}
```

### Invalid (Circular)

```json
{
  "a": { "$value": "{b}" },
  "b": { "$value": "{a}" }            
}
```

### Property-Level References (JSON Pointer)

For accessing specific properties within composite tokens:

```json
{
  "typography": {
    "heading": {
      "$type": "typography",
      "$value": {
        "fontFamily": ["Inter"],
        "fontSize": { "value": 32, "unit": "px" },
        "fontWeight": 700
      }
    }
  },
  "heading-font-size": {
    "$type": "dimension",
    "$value": { "$ref": "{typography.heading}#/fontSize" }
  }
}
```

---

## Token Types

### Color

```json
{
  "brand-blue": {
    "$type": "color",
    "$value": {
      "colorSpace": "srgb",
      "components": [0, 0.4, 0.8],
      "alpha": 1,
      "hex": "#0066cc"
    }
  }
}
```

**Color spaces supported (14 total):**
- `srgb`, `srgb-linear`
- `display-p3`
- `hsl`, `hwb`
- `lab`, `lch`
- `oklab`, `oklch`
- `xyz`, `xyz-d50`, `xyz-d65`
- `rec2020`
- `a98-rgb`, `prophoto-rgb`

**Components:** Array of channel values (0-1 for most spaces, varies for lab/lch/oklab/oklch)

### Dimension

```json
{
  "spacing-md": {
    "$type": "dimension",
    "$value": {
      "value": 16,
      "unit": "px"
    }
  }
}
```

**Units:** `px` (idealized pixel) or `rem`

The `px` unit represents an idealized reference pixel that transforms appropriately per platform.

### Font Family

```json
{
  "font-sans": {
    "$type": "fontFamily",
    "$value": ["Inter", "Helvetica Neue", "Arial", "sans-serif"]
  }
}
```

String or array of strings (fallback stack).

### Font Weight

```json
{
  "weight-bold": {
    "$type": "fontWeight",
    "$value": 700
  }
}
```

**Numeric:** 1-1000 (CSS font-weight values)

**Keywords:** `thin` (100), `hairline` (100), `extra-light` (200), `ultra-light` (200), `light` (300), `normal` (400), `regular` (400), `book` (400), `medium` (500), `semi-bold` (600), `demi-bold` (600), `bold` (700), `extra-bold` (800), `ultra-bold` (800), `black` (900), `heavy` (900), `extra-black` (950), `ultra-black` (950)

### Duration

```json
{
  "duration-fast": {
    "$type": "duration",
    "$value": {
      "value": 150,
      "unit": "ms"
    }
  }
}
```

**Units:** `ms` (milliseconds) or `s` (seconds)

### Cubic Bézier

```json
{
  "ease-out": {
    "$type": "cubicBezier",
    "$value": [0, 0, 0.2, 1]
  }
}
```

Array of 4 numbers: `[P1x, P1y, P2x, P2y]`

### Number

```json
{
  "line-height-normal": {
    "$type": "number",
    "$value": 1.5
  }
}
```

Plain JSON number for unitless values.

### Typography (Composite)

```json
{
  "heading-1": {
    "$type": "typography",
    "$value": {
      "fontFamily": ["Inter", "sans-serif"],
      "fontSize": { "value": 32, "unit": "px" },
      "fontWeight": 700,
      "lineHeight": 1.25,
      "letterSpacing": { "value": -0.5, "unit": "px" }
    }
  }
}
```

All properties optional. Values can be aliases.

### Shadow

```json
{
  "shadow-md": {
    "$type": "shadow",
    "$value": {
      "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.15 },
      "offsetX": { "value": 0, "unit": "px" },
      "offsetY": { "value": 4, "unit": "px" },
      "blur": { "value": 8, "unit": "px" },
      "spread": { "value": 0, "unit": "px" },
      "inset": false
    }
  }
}
```

**Layered shadows:** Use array of shadow objects:

```json
{
  "shadow-lg": {
    "$type": "shadow",
    "$value": [
      { "color": {...}, "offsetY": { "value": 4, "unit": "px" }, "blur": { "value": 6, "unit": "px" } },
      { "color": {...}, "offsetY": { "value": 2, "unit": "px" }, "blur": { "value": 4, "unit": "px" } }
    ]
  }
}
```

### Border

```json
{
  "border-default": {
    "$type": "border",
    "$value": {
      "color": { "colorSpace": "srgb", "components": [0.85, 0.85, 0.85] },
      "width": { "value": 1, "unit": "px" },
      "style": "solid"
    }
  }
}
```

**Style values:** `solid`, `dashed`, `dotted`, `double`, `groove`, `ridge`, `outset`, `inset`, `none`

### Gradient

```json
{
  "gradient-brand": {
    "$type": "gradient",
    "$value": [
      {
        "color": { "colorSpace": "srgb", "components": [0, 0.4, 0.8] },
        "position": 0
      },
      {
        "color": { "colorSpace": "srgb", "components": [0, 0.6, 1] },
        "position": 1
      }
    ]
  }
}
```

Array of color stops with position (0-1).

### Transition

```json
{
  "transition-default": {
    "$type": "transition",
    "$value": {
      "duration": { "value": 200, "unit": "ms" },
      "delay": { "value": 0, "unit": "ms" },
      "timingFunction": [0.4, 0, 0.2, 1]
    }
  }
}
```

### Stroke Style

```json
{
  "stroke-dashed": {
    "$type": "strokeStyle",
    "$value": {
      "dashArray": [
        { "value": 4, "unit": "px" },
        { "value": 2, "unit": "px" }
      ],
      "lineCap": "round"
    }
  }
}
```

**Simple form:** `"solid"`, `"dashed"`, `"dotted"`, etc.

**Complex form:** Object with `dashArray` and optional `lineCap` (`butt`, `round`, `square`)

---

## File Organization

### Recommended Structure

```
tokens/
├── primitives/
│   ├── colors.tokens.json
│   ├── spacing.tokens.json
│   └── typography.tokens.json
├── semantic/
│   ├── colors.tokens.json
│   ├── spacing.tokens.json
│   └── typography.tokens.json
├── components/
│   ├── button.tokens.json
│   └── card.tokens.json
└── themes/
    ├── light.tokens.json
    └── dark.tokens.json
```

### Multi-File References

References work across files when processed by build tools:

```json
// primitives/colors.tokens.json
{
  "color": {
    "blue": {
      "500": { "$value": {...}, "$type": "color" }
    }
  }
}

// semantic/colors.tokens.json
{
  "color": {
    "brand": {
      "primary": { "$value": "{color.blue.500}" }
    }
  }
}
```

Build tools merge files before resolving references.

---

## Validation Rules

Tools implementing DTCG must:

1. **Require `$value`** on all tokens
2. **Validate `$type`** against known types
3. **Resolve aliases** following dot-notation paths
4. **Detect circular references** and error
5. **Apply type inheritance** from groups to children
6. **Preserve `$extensions`** without validation
7. **Handle unknown properties** gracefully (ignore or pass through)
