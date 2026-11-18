# Token Types Reference

Complete examples for all 13 DTCG token types with common patterns and variations.

---

## Color

### Basic sRGB Color

```json
{
  "brand-blue": {
    "$type": "color",
    "$value": {
      "colorSpace": "srgb",
      "components": [0.129, 0.588, 0.953],
      "alpha": 1
    }
  }
}
```

### With Hex Hint

```json
{
  "brand-blue": {
    "$type": "color",
    "$value": {
      "colorSpace": "srgb",
      "components": [0.129, 0.588, 0.953],
      "hex": "#2196F3"
    },
    "$description": "Primary brand blue"
  }
}
```

### Wide-Gamut (Display P3)

```json
{
  "vibrant-green": {
    "$type": "color",
    "$value": {
      "colorSpace": "display-p3",
      "components": [0, 0.85, 0.3]
    }
  }
}
```

### Perceptually Uniform (OKLCH)

```json
{
  "accessible-blue": {
    "$type": "color",
    "$value": {
      "colorSpace": "oklch",
      "components": [0.62, 0.18, 250]
    },
    "$description": "Lightness: 62%, Chroma: 0.18, Hue: 250°"
  }
}
```

### With Transparency

```json
{
  "overlay-dark": {
    "$type": "color",
    "$value": {
      "colorSpace": "srgb",
      "components": [0, 0, 0],
      "alpha": 0.5
    }
  }
}
```

### Color Scale Pattern

```json
{
  "color": {
    "$type": "color",
    "blue": {
      "50": { "$value": { "colorSpace": "srgb", "components": [0.93, 0.96, 1] } },
      "100": { "$value": { "colorSpace": "srgb", "components": [0.89, 0.95, 0.99] } },
      "200": { "$value": { "colorSpace": "srgb", "components": [0.79, 0.89, 0.98] } },
      "300": { "$value": { "colorSpace": "srgb", "components": [0.63, 0.81, 0.95] } },
      "400": { "$value": { "colorSpace": "srgb", "components": [0.42, 0.71, 0.91] } },
      "500": { "$value": { "colorSpace": "srgb", "components": [0.13, 0.59, 0.95] } },
      "600": { "$value": { "colorSpace": "srgb", "components": [0.12, 0.53, 0.90] } },
      "700": { "$value": { "colorSpace": "srgb", "components": [0.10, 0.46, 0.82] } },
      "800": { "$value": { "colorSpace": "srgb", "components": [0.08, 0.40, 0.75] } },
      "900": { "$value": { "colorSpace": "srgb", "components": [0.05, 0.28, 0.63] } }
    }
  }
}
```

---

## Dimension

### Pixel Values

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

### Rem Values

```json
{
  "font-size-base": {
    "$type": "dimension",
    "$value": {
      "value": 1,
      "unit": "rem"
    }
  }
}
```

### Spacing Scale (4px base)

```json
{
  "space": {
    "$type": "dimension",
    "0": { "$value": { "value": 0, "unit": "px" } },
    "1": { "$value": { "value": 4, "unit": "px" } },
    "2": { "$value": { "value": 8, "unit": "px" } },
    "3": { "$value": { "value": 12, "unit": "px" } },
    "4": { "$value": { "value": 16, "unit": "px" } },
    "5": { "$value": { "value": 20, "unit": "px" } },
    "6": { "$value": { "value": 24, "unit": "px" } },
    "8": { "$value": { "value": 32, "unit": "px" } },
    "10": { "$value": { "value": 40, "unit": "px" } },
    "12": { "$value": { "value": 48, "unit": "px" } },
    "16": { "$value": { "value": 64, "unit": "px" } }
  }
}
```

### Border Radius Scale

```json
{
  "radius": {
    "$type": "dimension",
    "none": { "$value": { "value": 0, "unit": "px" } },
    "sm": { "$value": { "value": 2, "unit": "px" } },
    "md": { "$value": { "value": 4, "unit": "px" } },
    "lg": { "$value": { "value": 8, "unit": "px" } },
    "xl": { "$value": { "value": 12, "unit": "px" } },
    "2xl": { "$value": { "value": 16, "unit": "px" } },
    "full": { "$value": { "value": 9999, "unit": "px" } }
  }
}
```

### Font Size Scale

```json
{
  "font-size": {
    "$type": "dimension",
    "xs": { "$value": { "value": 0.75, "unit": "rem" } },
    "sm": { "$value": { "value": 0.875, "unit": "rem" } },
    "base": { "$value": { "value": 1, "unit": "rem" } },
    "lg": { "$value": { "value": 1.125, "unit": "rem" } },
    "xl": { "$value": { "value": 1.25, "unit": "rem" } },
    "2xl": { "$value": { "value": 1.5, "unit": "rem" } },
    "3xl": { "$value": { "value": 1.875, "unit": "rem" } },
    "4xl": { "$value": { "value": 2.25, "unit": "rem" } },
    "5xl": { "$value": { "value": 3, "unit": "rem" } }
  }
}
```

---

## Font Family

### Single Font

```json
{
  "font-mono": {
    "$type": "fontFamily",
    "$value": "JetBrains Mono"
  }
}
```

### Font Stack

```json
{
  "font-sans": {
    "$type": "fontFamily",
    "$value": ["Inter", "Helvetica Neue", "Arial", "sans-serif"]
  }
}
```

### System Font Stack

```json
{
  "font": {
    "$type": "fontFamily",
    "sans": {
      "$value": [
        "system-ui",
        "-apple-system",
        "BlinkMacSystemFont",
        "Segoe UI",
        "Roboto",
        "Helvetica Neue",
        "Arial",
        "sans-serif"
      ]
    },
    "serif": {
      "$value": ["Georgia", "Cambria", "Times New Roman", "Times", "serif"]
    },
    "mono": {
      "$value": [
        "ui-monospace",
        "SFMono-Regular",
        "Menlo",
        "Monaco",
        "Consolas",
        "Liberation Mono",
        "Courier New",
        "monospace"
      ]
    }
  }
}
```

---

## Font Weight

### Numeric Value

```json
{
  "weight-bold": {
    "$type": "fontWeight",
    "$value": 700
  }
}
```

### Keyword Value

```json
{
  "weight-bold": {
    "$type": "fontWeight",
    "$value": "bold"
  }
}
```

### Complete Weight Scale

```json
{
  "font-weight": {
    "$type": "fontWeight",
    "thin": { "$value": 100 },
    "extralight": { "$value": 200 },
    "light": { "$value": 300 },
    "regular": { "$value": 400 },
    "medium": { "$value": 500 },
    "semibold": { "$value": 600 },
    "bold": { "$value": 700 },
    "extrabold": { "$value": 800 },
    "black": { "$value": 900 }
  }
}
```

---

## Duration

### Milliseconds

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

### Seconds

```json
{
  "duration-slow": {
    "$type": "duration",
    "$value": {
      "value": 0.5,
      "unit": "s"
    }
  }
}
```

### Duration Scale

```json
{
  "duration": {
    "$type": "duration",
    "instant": { "$value": { "value": 0, "unit": "ms" } },
    "75": { "$value": { "value": 75, "unit": "ms" } },
    "100": { "$value": { "value": 100, "unit": "ms" } },
    "150": { "$value": { "value": 150, "unit": "ms" } },
    "200": { "$value": { "value": 200, "unit": "ms" } },
    "300": { "$value": { "value": 300, "unit": "ms" } },
    "500": { "$value": { "value": 500, "unit": "ms" } },
    "700": { "$value": { "value": 700, "unit": "ms" } },
    "1000": { "$value": { "value": 1000, "unit": "ms" } }
  }
}
```

---

## Cubic Bézier

### Standard Easings

```json
{
  "easing": {
    "$type": "cubicBezier",
    "linear": { "$value": [0, 0, 1, 1] },
    "ease": { "$value": [0.25, 0.1, 0.25, 1] },
    "ease-in": { "$value": [0.42, 0, 1, 1] },
    "ease-out": { "$value": [0, 0, 0.58, 1] },
    "ease-in-out": { "$value": [0.42, 0, 0.58, 1] }
  }
}
```

### Material Design Easings

```json
{
  "easing": {
    "$type": "cubicBezier",
    "emphasized": { "$value": [0.2, 0, 0, 1] },
    "emphasized-decelerate": { "$value": [0.05, 0.7, 0.1, 1] },
    "emphasized-accelerate": { "$value": [0.3, 0, 0.8, 0.15] },
    "standard": { "$value": [0.2, 0, 0, 1] },
    "standard-decelerate": { "$value": [0, 0, 0, 1] },
    "standard-accelerate": { "$value": [0.3, 0, 1, 1] }
  }
}
```

---

## Number

### Line Height

```json
{
  "line-height": {
    "$type": "number",
    "none": { "$value": 1 },
    "tight": { "$value": 1.25 },
    "snug": { "$value": 1.375 },
    "normal": { "$value": 1.5 },
    "relaxed": { "$value": 1.625 },
    "loose": { "$value": 2 }
  }
}
```

### Opacity

```json
{
  "opacity": {
    "$type": "number",
    "0": { "$value": 0 },
    "5": { "$value": 0.05 },
    "10": { "$value": 0.1 },
    "25": { "$value": 0.25 },
    "50": { "$value": 0.5 },
    "75": { "$value": 0.75 },
    "100": { "$value": 1 }
  }
}
```

### Scale/Transform

```json
{
  "scale": {
    "$type": "number",
    "75": { "$value": 0.75 },
    "90": { "$value": 0.9 },
    "95": { "$value": 0.95 },
    "100": { "$value": 1 },
    "105": { "$value": 1.05 },
    "110": { "$value": 1.1 },
    "125": { "$value": 1.25 }
  }
}
```

---

## Typography (Composite)

### Basic Typography Token

```json
{
  "body-default": {
    "$type": "typography",
    "$value": {
      "fontFamily": ["Inter", "sans-serif"],
      "fontSize": { "value": 16, "unit": "px" },
      "fontWeight": 400,
      "lineHeight": 1.5,
      "letterSpacing": { "value": 0, "unit": "px" }
    }
  }
}
```

### With Aliases

```json
{
  "heading-1": {
    "$type": "typography",
    "$value": {
      "fontFamily": "{font.sans}",
      "fontSize": "{font-size.4xl}",
      "fontWeight": "{font-weight.bold}",
      "lineHeight": "{line-height.tight}",
      "letterSpacing": { "value": -0.5, "unit": "px" }
    }
  }
}
```

### Typography Scale

```json
{
  "typography": {
    "$type": "typography",
    "display-lg": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 57, "unit": "px" },
        "fontWeight": 400,
        "lineHeight": 1.12,
        "letterSpacing": { "value": -0.25, "unit": "px" }
      }
    },
    "heading-1": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 36, "unit": "px" },
        "fontWeight": 700,
        "lineHeight": 1.22,
        "letterSpacing": { "value": -0.5, "unit": "px" }
      }
    },
    "heading-2": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 28, "unit": "px" },
        "fontWeight": 600,
        "lineHeight": 1.29,
        "letterSpacing": { "value": -0.25, "unit": "px" }
      }
    },
    "body-lg": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 18, "unit": "px" },
        "fontWeight": 400,
        "lineHeight": 1.56,
        "letterSpacing": { "value": 0, "unit": "px" }
      }
    },
    "body-md": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 16, "unit": "px" },
        "fontWeight": 400,
        "lineHeight": 1.5,
        "letterSpacing": { "value": 0, "unit": "px" }
      }
    },
    "body-sm": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 14, "unit": "px" },
        "fontWeight": 400,
        "lineHeight": 1.43,
        "letterSpacing": { "value": 0, "unit": "px" }
      }
    },
    "caption": {
      "$value": {
        "fontFamily": ["Inter", "sans-serif"],
        "fontSize": { "value": 12, "unit": "px" },
        "fontWeight": 400,
        "lineHeight": 1.33,
        "letterSpacing": { "value": 0.25, "unit": "px" }
      }
    }
  }
}
```

---

## Shadow

### Single Shadow

```json
{
  "shadow-sm": {
    "$type": "shadow",
    "$value": {
      "color": {
        "colorSpace": "srgb",
        "components": [0, 0, 0],
        "alpha": 0.1
      },
      "offsetX": { "value": 0, "unit": "px" },
      "offsetY": { "value": 1, "unit": "px" },
      "blur": { "value": 2, "unit": "px" },
      "spread": { "value": 0, "unit": "px" }
    }
  }
}
```

### Layered Shadows

```json
{
  "shadow-lg": {
    "$type": "shadow",
    "$value": [
      {
        "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1 },
        "offsetX": { "value": 0, "unit": "px" },
        "offsetY": { "value": 10, "unit": "px" },
        "blur": { "value": 15, "unit": "px" },
        "spread": { "value": -3, "unit": "px" }
      },
      {
        "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.05 },
        "offsetX": { "value": 0, "unit": "px" },
        "offsetY": { "value": 4, "unit": "px" },
        "blur": { "value": 6, "unit": "px" },
        "spread": { "value": -2, "unit": "px" }
      }
    ]
  }
}
```

### Inset Shadow

```json
{
  "shadow-inset": {
    "$type": "shadow",
    "$value": {
      "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1 },
      "offsetX": { "value": 0, "unit": "px" },
      "offsetY": { "value": 2, "unit": "px" },
      "blur": { "value": 4, "unit": "px" },
      "spread": { "value": 0, "unit": "px" },
      "inset": true
    }
  }
}
```

### Elevation Scale

```json
{
  "shadow": {
    "$type": "shadow",
    "none": { "$value": { "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0 }, "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 0, "unit": "px" }, "blur": { "value": 0, "unit": "px" }, "spread": { "value": 0, "unit": "px" } } },
    "sm": { "$value": { "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.05 }, "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 1, "unit": "px" }, "blur": { "value": 2, "unit": "px" }, "spread": { "value": 0, "unit": "px" } } },
    "md": { "$value": { "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1 }, "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 4, "unit": "px" }, "blur": { "value": 6, "unit": "px" }, "spread": { "value": -1, "unit": "px" } } },
    "lg": { "$value": { "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1 }, "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 10, "unit": "px" }, "blur": { "value": 15, "unit": "px" }, "spread": { "value": -3, "unit": "px" } } },
    "xl": { "$value": { "color": { "colorSpace": "srgb", "components": [0, 0, 0], "alpha": 0.1 }, "offsetX": { "value": 0, "unit": "px" }, "offsetY": { "value": 20, "unit": "px" }, "blur": { "value": 25, "unit": "px" }, "spread": { "value": -5, "unit": "px" } } }
  }
}
```

---

## Border

### Basic Border

```json
{
  "border-default": {
    "$type": "border",
    "$value": {
      "color": {
        "colorSpace": "srgb",
        "components": [0.85, 0.85, 0.85]
      },
      "width": { "value": 1, "unit": "px" },
      "style": "solid"
    }
  }
}
```

### Border Variants

```json
{
  "border": {
    "$type": "border",
    "subtle": {
      "$value": {
        "color": { "colorSpace": "srgb", "components": [0.9, 0.9, 0.9] },
        "width": { "value": 1, "unit": "px" },
        "style": "solid"
      }
    },
    "default": {
      "$value": {
        "color": { "colorSpace": "srgb", "components": [0.8, 0.8, 0.8] },
        "width": { "value": 1, "unit": "px" },
        "style": "solid"
      }
    },
    "strong": {
      "$value": {
        "color": { "colorSpace": "srgb", "components": [0.6, 0.6, 0.6] },
        "width": { "value": 2, "unit": "px" },
        "style": "solid"
      }
    },
    "focus": {
      "$value": {
        "color": { "colorSpace": "srgb", "components": [0.13, 0.59, 0.95] },
        "width": { "value": 2, "unit": "px" },
        "style": "solid"
      }
    }
  }
}
```

---

## Gradient

### Linear Gradient

```json
{
  "gradient-brand": {
    "$type": "gradient",
    "$value": [
      {
        "color": { "colorSpace": "srgb", "components": [0.13, 0.59, 0.95] },
        "position": 0
      },
      {
        "color": { "colorSpace": "srgb", "components": [0.54, 0.17, 0.89] },
        "position": 1
      }
    ]
  }
}
```

### Multi-Stop Gradient

```json
{
  "gradient-rainbow": {
    "$type": "gradient",
    "$value": [
      { "color": { "colorSpace": "srgb", "components": [1, 0, 0] }, "position": 0 },
      { "color": { "colorSpace": "srgb", "components": [1, 0.5, 0] }, "position": 0.17 },
      { "color": { "colorSpace": "srgb", "components": [1, 1, 0] }, "position": 0.33 },
      { "color": { "colorSpace": "srgb", "components": [0, 1, 0] }, "position": 0.5 },
      { "color": { "colorSpace": "srgb", "components": [0, 0, 1] }, "position": 0.67 },
      { "color": { "colorSpace": "srgb", "components": [0.29, 0, 0.51] }, "position": 0.83 },
      { "color": { "colorSpace": "srgb", "components": [0.56, 0, 1] }, "position": 1 }
    ]
  }
}
```

---

## Transition

### Basic Transition

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

### With Aliases

```json
{
  "transition-fast": {
    "$type": "transition",
    "$value": {
      "duration": "{duration.150}",
      "delay": { "value": 0, "unit": "ms" },
      "timingFunction": "{easing.ease-out}"
    }
  }
}
```

---

## Stroke Style

### Simple Style

```json
{
  "stroke-solid": {
    "$type": "strokeStyle",
    "$value": "solid"
  }
}
```

### Dashed Pattern

```json
{
  "stroke-dashed": {
    "$type": "strokeStyle",
    "$value": {
      "dashArray": [
        { "value": 4, "unit": "px" },
        { "value": 4, "unit": "px" }
      ],
      "lineCap": "butt"
    }
  }
}
```

### Dotted Pattern

```json
{
  "stroke-dotted": {
    "$type": "strokeStyle",
    "$value": {
      "dashArray": [
        { "value": 2, "unit": "px" },
        { "value": 2, "unit": "px" }
      ],
      "lineCap": "round"
    }
  }
}
```

### Custom Pattern

```json
{
  "stroke-custom": {
    "$type": "strokeStyle",
    "$value": {
      "dashArray": [
        { "value": 10, "unit": "px" },
        { "value": 5, "unit": "px" },
        { "value": 2, "unit": "px" },
        { "value": 5, "unit": "px" }
      ],
      "lineCap": "square"
    }
  }
}
```
