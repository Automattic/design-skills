# Token Naming Conventions

Effective token naming creates discoverable, maintainable systems that scale with organizational complexity.

## The CTI Pattern

**Category / Type / Item** - Industry standard from Amazon Style Dictionary:

```
color.background.primary
color.text.secondary
spacing.padding.medium
typography.heading.large
font.family.sans
```

Read left-to-right from general to specific.

## Extended Hierarchy

For larger systems, Nathan Curtis (EightShapes) proposes:

**Namespace / Category / Element / Variant / State**

```
acme-color-button-primary-default
acme-color-button-primary-hover
acme-color-button-secondary-disabled
```

### Components

| Level | Purpose | Examples |
|-------|---------|----------|
| Namespace | System/brand prefix | `acme`, `carbon`, `polaris` |
| Category | Token type | `color`, `space`, `font`, `motion` |
| Element | What it applies to | `background`, `text`, `border`, `button` |
| Variant | Which version | `primary`, `secondary`, `brand`, `error` |
| State | Interaction state | `default`, `hover`, `active`, `disabled` |

---

## Three-Tier Naming

### Tier 1: Primitives

Raw values with descriptive, non-semantic names:

```json
{
  "color": {
    "blue": {
      "50": { "$value": {...} },
      "100": { "$value": {...} },
      "500": { "$value": {...} },
      "900": { "$value": {...} }
    },
    "neutral": {
      "0": { "$value": {...} },
      "50": { "$value": {...} },
      "900": { "$value": {...} },
      "1000": { "$value": {...} }
    }
  }
}
```

**Naming rules for primitives:**
- Use color names + numeric scale (50-950 or 100-900)
- Use multiplier numbers for spacing (`4`, `8`, `16`)
- Avoid semantic meaning (`primary`, `danger`)

### Tier 2: Semantic Tokens

Express design intent by referencing primitives:

```json
{
  "color": {
    "background": {
      "default": { "$value": "{color.neutral.0}" },
      "subtle": { "$value": "{color.neutral.50}" },
      "brand": { "$value": "{color.blue.500}" },
      "inverse": { "$value": "{color.neutral.900}" }
    },
    "text": {
      "default": { "$value": "{color.neutral.900}" },
      "muted": { "$value": "{color.neutral.600}" },
      "inverse": { "$value": "{color.neutral.0}" },
      "brand": { "$value": "{color.blue.600}" }
    },
    "border": {
      "default": { "$value": "{color.neutral.200}" },
      "strong": { "$value": "{color.neutral.400}" }
    },
    "feedback": {
      "error": { "$value": "{color.red.500}" },
      "success": { "$value": "{color.green.500}" },
      "warning": { "$value": "{color.yellow.500}" },
      "info": { "$value": "{color.blue.500}" }
    }
  }
}
```

**Naming rules for semantics:**
- Describe purpose, not appearance
- Use `default`, `subtle`, `strong` for prominence
- Use `inverse` for opposite context
- Group by application (`background`, `text`, `border`)

### Tier 3: Component Tokens

Map semantic tokens to specific components:

```json
{
  "button": {
    "primary": {
      "background": {
        "default": { "$value": "{color.background.brand}" },
        "hover": { "$value": "{color.blue.600}" },
        "active": { "$value": "{color.blue.700}" },
        "disabled": { "$value": "{color.neutral.200}" }
      },
      "text": {
        "default": { "$value": "{color.text.inverse}" },
        "disabled": { "$value": "{color.text.muted}" }
      }
    }
  }
}
```

**Naming rules for components:**
- Start with component name
- Include variant
- Include property
- Include state last

---

## Common Semantic Categories

### Color Semantics

| Category | Purpose | Examples |
|----------|---------|----------|
| `background` | Surface colors | `default`, `subtle`, `brand`, `inverse` |
| `text` | Text colors | `default`, `muted`, `brand`, `inverse`, `link` |
| `border` | Border colors | `default`, `strong`, `focus` |
| `feedback` | Status indicators | `error`, `success`, `warning`, `info` |
| `interactive` | Clickable elements | `default`, `hover`, `active`, `focus` |

### Spacing Semantics

| Name | Typical Use |
|------|-------------|
| `inset` | Inner padding |
| `stack` | Vertical spacing between items |
| `inline` | Horizontal spacing between items |
| `gap` | Grid/flex gaps |

Example:
```json
{
  "space": {
    "inset": {
      "sm": { "$value": "{space.2}" },
      "md": { "$value": "{space.4}" }
    },
    "stack": {
      "sm": { "$value": "{space.2}" },
      "md": { "$value": "{space.4}" }
    }
  }
}
```

### Typography Semantics

| Name | Purpose |
|------|---------|
| `display` | Large headlines |
| `heading` | Section headings |
| `title` | Card/component titles |
| `body` | Paragraph text |
| `label` | Form labels, UI text |
| `caption` | Small supporting text |
| `code` | Monospace text |

Example:
```json
{
  "typography": {
    "display": {
      "lg": { "$value": {...} },
      "md": { "$value": {...} }
    },
    "heading": {
      "1": { "$value": {...} },
      "2": { "$value": {...} }
    },
    "body": {
      "default": { "$value": {...} },
      "small": { "$value": {...} }
    }
  }
}
```

---

## Theming Patterns

### Light/Dark Mode

Keep token names identical. Change primitive references:

```json
// themes/light.tokens.json
{
  "color": {
    "background": {
      "default": { "$value": "{color.neutral.0}" }
    },
    "text": {
      "default": { "$value": "{color.neutral.900}" }
    }
  }
}

// themes/dark.tokens.json
{
  "color": {
    "background": {
      "default": { "$value": "{color.neutral.900}" }
    },
    "text": {
      "default": { "$value": "{color.neutral.0}" }
    }
  }
}
```

**Key principle:** Consumers use `color.background.default` regardless of theme.

### Multi-Brand

Override primitives per brand, share semantic layer:

```
tokens/
├── brands/
│   ├── brand-a/
│   │   └── primitives.tokens.json  # blue primary
│   └── brand-b/
│       └── primitives.tokens.json  # green primary
└── shared/
    └── semantic.tokens.json        # uses {brand.primary}
```

```json
// brands/brand-a/primitives.tokens.json
{
  "brand": {
    "primary": { "$value": "{color.blue.500}" },
    "secondary": { "$value": "{color.blue.700}" }
  }
}

// shared/semantic.tokens.json
{
  "color": {
    "background": {
      "brand": { "$value": "{brand.primary}" }
    }
  }
}
```

---

## Naming Conventions by System

### IBM Carbon

```
$carbon--{category}-{variant}-{modifier}

$carbon--blue-60
$interactive-01  →  $interactive (v11)
$ui-background   →  $background (v11)
$text-01         →  $text-primary (v11)
```

### Salesforce Lightning

```
--slds-g-{category}-{variant}-{number}    (global)
--slds-c-{component}-{property}           (component)

--slds-g-color-surface-1
--slds-g-spacing-4
--slds-c-button-color-background
```

### Google Material

```
--md-ref-{category}-{name}     (reference)
--md-sys-{category}-{name}     (system)

--md-ref-palette-primary40
--md-sys-color-primary
--md-sys-typescale-body-medium
```

### Shopify Polaris

```
--p-{category}-{element}-{role}-{prominence}-{state}

--p-color-bg-surface
--p-color-text-secondary
--p-space-400
--p-shadow-300
```

---

## Best Practices

### Do

- **Be consistent** - Same pattern across all tokens
- **Be descriptive** - Names should communicate purpose
- **Use lowercase** - `color-primary` not `Color-Primary`
- **Use hyphens** - `font-family` not `fontFamily` in token names
- **Group logically** - By category, then specificity
- **Document intent** - Use `$description` for non-obvious tokens

### Avoid

- **Abbreviations** - `bg` → `background`, `btn` → `button`
- **Platform terms** - `ios-blue`, `android-spacing`
- **Magic numbers** - Don't use `blue-500` as semantic name
- **Overly generic** - `color-1`, `spacing-a`
- **Deep nesting** - Max 4-5 levels
- **Implementation details** - `rgba-black-15` → `shadow-color`

### Naming Length

| Level | Recommended Length | Example |
|-------|-------------------|---------|
| Primitive | 2-3 segments | `color.blue.500` |
| Semantic | 3-4 segments | `color.background.brand` |
| Component | 4-5 segments | `button.primary.background.hover` |

---

## Migration Strategies

### Renaming Tokens

Use `$deprecated` and aliases for backward compatibility:

```json
{
  "old-name": {
    "$value": "{new-name}",
    "$deprecated": "Use 'new-name' instead. Removal in v3.0."
  },
  "new-name": {
    "$value": {...}
  }
}
```

### Gradual Adoption

1. Start with primitives
2. Add semantic layer for new features
3. Migrate existing usage to semantic tokens
4. Add component tokens as needed
5. Deprecate direct primitive usage
