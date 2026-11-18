# Build Tools Reference

Token transformation and build workflows using Style Dictionary, Tokens Studio, and other tools.

---

## Style Dictionary

Industry-standard tool for transforming tokens to platform-specific outputs.

### Installation

```bash
npm install style-dictionary
```

### Basic Configuration

**`sd.config.js`:**
```javascript
export default {
  source: ['tokens/**/*.tokens.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    }
  }
};
```

### Build Command

```bash
npx style-dictionary build --config sd.config.js
```

### Multi-Platform Configuration

```javascript
export default {
  source: ['tokens/**/*.tokens.json'],
  platforms: {
    // CSS Custom Properties
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables',
        options: {
          outputReferences: true  // Preserve aliases as var()
        }
      }]
    },
    
    // Sass Variables
    scss: {
      transformGroup: 'scss',
      buildPath: 'build/scss/',
      files: [{
        destination: '_variables.scss',
        format: 'scss/variables'
      }]
    },
    
    // JavaScript/TypeScript
    js: {
      transformGroup: 'js',
      buildPath: 'build/js/',
      files: [
        {
          destination: 'tokens.js',
          format: 'javascript/es6'
        },
        {
          destination: 'tokens.d.ts',
          format: 'typescript/es6-declarations'
        }
      ]
    },
    
    // JSON (resolved)
    json: {
      transformGroup: 'web',
      buildPath: 'build/json/',
      files: [{
        destination: 'tokens.json',
        format: 'json/flat'
      }]
    },
    
    // iOS Swift
    ios: {
      transformGroup: 'ios-swift',
      buildPath: 'build/ios/',
      files: [{
        destination: 'StyleDictionary.swift',
        format: 'ios-swift/class.swift',
        className: 'StyleDictionary'
      }]
    },
    
    // Android XML
    android: {
      transformGroup: 'android',
      buildPath: 'build/android/',
      files: [
        {
          destination: 'colors.xml',
          format: 'android/colors',
          filter: { type: 'color' }
        },
        {
          destination: 'dimens.xml',
          format: 'android/dimens',
          filter: { type: 'dimension' }
        },
        {
          destination: 'font_dimens.xml',
          format: 'android/fontDimens',
          filter: { type: 'dimension' }
        }
      ]
    }
  }
};
```

### DTCG Format Support

Style Dictionary v4 supports DTCG format with the `@tokens-studio/sd-transforms` package:

```bash
npm install @tokens-studio/sd-transforms
```

```javascript
import { register } from '@tokens-studio/sd-transforms';
import StyleDictionary from 'style-dictionary';

// Register DTCG transforms
register(StyleDictionary);

export default {
  source: ['tokens/**/*.tokens.json'],
  preprocessors: ['tokens-studio'],
  platforms: {
    css: {
      transformGroup: 'tokens-studio',
      buildPath: 'build/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    }
  }
};
```

### Built-in Transform Groups

| Group | Transforms Applied |
|-------|-------------------|
| `css` | Colors to CSS, sizes to rem, names to kebab-case |
| `scss` | Same as CSS |
| `js` | Colors to hex, sizes to px, names to camelCase |
| `ios` | Colors to UIColor, sizes to CGFloat |
| `ios-swift` | Colors to SwiftUI Color |
| `android` | Colors to hex8, sizes to dp/sp |

### Custom Transforms

```javascript
import StyleDictionary from 'style-dictionary';

StyleDictionary.registerTransform({
  name: 'size/pxToRem',
  type: 'value',
  transitive: true,
  filter: (token) => token.$type === 'dimension',
  transform: (token) => {
    const value = token.$value.value;
    const unit = token.$value.unit;
    if (unit === 'px') {
      return `${value / 16}rem`;
    }
    return `${value}${unit}`;
  }
});

StyleDictionary.registerTransform({
  name: 'color/cssVariable',
  type: 'value',
  transitive: true,
  filter: (token) => token.$type === 'color',
  transform: (token) => {
    const { colorSpace, components, alpha = 1 } = token.$value;
    if (colorSpace === 'srgb') {
      const [r, g, b] = components.map(c => Math.round(c * 255));
      return alpha < 1 
        ? `rgba(${r}, ${g}, ${b}, ${alpha})`
        : `rgb(${r}, ${g}, ${b})`;
    }
    // Handle other color spaces
    return token.$value;
  }
});
```

### Custom Formats

```javascript
StyleDictionary.registerFormat({
  name: 'css/customProperties',
  format: ({ dictionary, options }) => {
    const { selector = ':root' } = options;
    const tokens = dictionary.allTokens
      .map(token => `  --${token.name}: ${token.value};`)
      .join('\n');
    return `${selector} {\n${tokens}\n}`;
  }
});
```

### Filtering Tokens

```javascript
{
  platforms: {
    css: {
      files: [
        {
          destination: 'colors.css',
          format: 'css/variables',
          filter: { type: 'color' }
        },
        {
          destination: 'spacing.css',
          format: 'css/variables',
          filter: { type: 'dimension' }
        },
        {
          destination: 'typography.css',
          format: 'css/variables',
          filter: { type: 'typography' }
        }
      ]
    }
  }
}
```

### Theme Configuration

Build multiple themes from the same source:

```javascript
const themes = ['light', 'dark'];

export default {
  source: ['tokens/primitives/**/*.tokens.json'],
  platforms: Object.fromEntries(
    themes.map(theme => [
      `css-${theme}`,
      {
        transformGroup: 'css',
        buildPath: `build/css/${theme}/`,
        files: [{
          destination: 'variables.css',
          format: 'css/variables',
          options: {
            selector: `[data-theme="${theme}"]`
          }
        }],
        source: [`tokens/themes/${theme}/**/*.tokens.json`]
      }
    ])
  )
};
```

---

## Tokens Studio (Figma Tokens)

Visual token management in Figma with sync capabilities.

### Token Format

Tokens Studio uses a format similar to DTCG but with some differences:

```json
{
  "global": {
    "colors": {
      "primary": {
        "value": "#0066cc",
        "type": "color"
      }
    },
    "spacing": {
      "md": {
        "value": "16",
        "type": "spacing"
      }
    }
  }
}
```

**Key differences from DTCG:**
- `value` instead of `$value`
- `type` instead of `$type`
- No `$` prefix on properties
- Dimension values are strings without unit objects

### Sync Configuration

**`.tokens.json` or `tokens.json`:**
```json
{
  "$themes": [
    {
      "id": "light",
      "name": "Light",
      "selectedTokenSets": {
        "global": "enabled",
        "themes/light": "enabled"
      }
    },
    {
      "id": "dark",
      "name": "Dark",
      "selectedTokenSets": {
        "global": "enabled",
        "themes/dark": "enabled"
      }
    }
  ],
  "$metadata": {
    "tokenSetOrder": ["global", "themes/light", "themes/dark"]
  }
}
```

### Converting to DTCG

Use `@tokens-studio/sd-transforms` to convert Tokens Studio format to DTCG-compatible format for Style Dictionary:

```javascript
import { register } from '@tokens-studio/sd-transforms';
import StyleDictionary from 'style-dictionary';

register(StyleDictionary);

export default {
  source: ['tokens/**/*.json'],
  preprocessors: ['tokens-studio'],
  platforms: {
    css: {
      transformGroup: 'tokens-studio',
      buildPath: 'build/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables'
      }]
    }
  }
};
```

### Git Sync Setup

1. Create a repository for tokens
2. In Tokens Studio settings, add GitHub/GitLab provider
3. Configure branch and file path
4. Pull/push tokens from Figma

---

## Other Tools

### Terrazzo

New tool with full DTCG support:

```bash
npm install @terrazzo/cli @terrazzo/token-tools
```

**`terrazzo.config.mjs`:**
```javascript
import { defineConfig } from '@terrazzo/cli';
import css from '@terrazzo/plugin-css';

export default defineConfig({
  tokens: './tokens/**/*.tokens.json',
  outDir: './build/',
  plugins: [
    css({
      filename: 'tokens.css',
      p3: true,  // Enable P3 color support
    }),
  ],
});
```

### Specify

API-first token management:

```bash
npm install @specifyapp/sdk
```

```javascript
import Specify from '@specifyapp/sdk';

const client = new Specify({ token: process.env.SPECIFY_TOKEN });

// Fetch tokens
const tokens = await client.getTokens({ repository: 'my-repo' });

// Transform to CSS
const css = await client.toCSS(tokens);
```

---

## Build Workflow Patterns

### Simple Project

```
tokens/
├── primitives.tokens.json
├── semantic.tokens.json
└── sd.config.js
```

```javascript
// sd.config.js
export default {
  source: ['tokens/*.tokens.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'dist/',
      files: [{
        destination: 'tokens.css',
        format: 'css/variables'
      }]
    }
  }
};
```

### Multi-Theme Project

```
tokens/
├── primitives/
│   └── colors.tokens.json
├── themes/
│   ├── light.tokens.json
│   └── dark.tokens.json
├── semantic/
│   └── colors.tokens.json
└── sd.config.js
```

```javascript
// sd.config.js
const themes = ['light', 'dark'];

export default {
  source: [
    'tokens/primitives/**/*.tokens.json',
    'tokens/semantic/**/*.tokens.json'
  ],
  platforms: {
    ...Object.fromEntries(
      themes.map(theme => [
        theme,
        {
          transformGroup: 'css',
          buildPath: `dist/${theme}/`,
          source: [`tokens/themes/${theme}.tokens.json`],
          files: [{
            destination: 'tokens.css',
            format: 'css/variables',
            options: { selector: `[data-theme="${theme}"]` }
          }]
        }
      ])
    )
  }
};
```

### Multi-Brand Project

```
tokens/
├── brands/
│   ├── brand-a/
│   │   └── primitives.tokens.json
│   └── brand-b/
│       └── primitives.tokens.json
├── shared/
│   ├── semantic.tokens.json
│   └── components.tokens.json
└── sd.config.js
```

```javascript
// sd.config.js
const brands = ['brand-a', 'brand-b'];

export default {
  source: ['tokens/shared/**/*.tokens.json'],
  platforms: {
    ...Object.fromEntries(
      brands.map(brand => [
        brand,
        {
          transformGroup: 'css',
          buildPath: `dist/${brand}/`,
          source: [`tokens/brands/${brand}/**/*.tokens.json`],
          files: [{
            destination: 'tokens.css',
            format: 'css/variables'
          }]
        }
      ])
    )
  }
};
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/build-tokens.yml
name: Build Tokens

on:
  push:
    paths:
      - 'tokens/**'
  pull_request:
    paths:
      - 'tokens/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - run: npm ci
      
      - run: npx style-dictionary build
      
      - uses: actions/upload-artifact@v4
        with:
          name: tokens
          path: build/
```

### NPM Scripts

```json
{
  "scripts": {
    "tokens:build": "style-dictionary build",
    "tokens:clean": "rm -rf build/",
    "tokens:watch": "style-dictionary build --watch",
    "tokens:validate": "node scripts/validate-tokens.js"
  }
}
```

---

## Output Examples

### CSS Custom Properties

```css
:root {
  --color-blue-500: rgb(33, 150, 243);
  --color-background-brand: var(--color-blue-500);
  --space-4: 1rem;
  --font-family-sans: 'Inter', sans-serif;
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
```

### Sass Variables

```scss
$color-blue-500: rgb(33, 150, 243);
$color-background-brand: $color-blue-500;
$space-4: 1rem;
$font-family-sans: 'Inter', sans-serif;
```

### JavaScript ES6

```javascript
export const colorBlue500 = 'rgb(33, 150, 243)';
export const colorBackgroundBrand = 'rgb(33, 150, 243)';
export const space4 = '1rem';
export const fontFamilySans = "'Inter', sans-serif";
```

### TypeScript Declarations

```typescript
export declare const colorBlue500: string;
export declare const colorBackgroundBrand: string;
export declare const space4: string;
export declare const fontFamilySans: string;
```

### iOS Swift

```swift
import UIKit

public class StyleDictionary {
    public static let colorBlue500 = UIColor(red: 0.129, green: 0.588, blue: 0.953, alpha: 1.0)
    public static let space4: CGFloat = 16.0
}
```

### Android XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<resources>
    <color name="color_blue_500">#2196F3</color>
    <dimen name="space_4">16dp</dimen>
</resources>
```
