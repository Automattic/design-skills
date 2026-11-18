# Major Design System Token Implementations

Reference implementations from IBM Carbon, Salesforce Lightning, Google Material Design 3, and Shopify Polaris.

---

## IBM Carbon Design System

### Architecture

**Modular packages:**
- `@carbon/colors` - IBM Design Language color primitives
- `@carbon/themes` - Semantic theme tokens
- `@carbon/layout` - Spacing scale
- `@carbon/type` - Typography
- `@carbon/motion` - Animation

### Token Hierarchy

**Three tiers:**
1. **Primitives** - Raw IBM color values (`$ibm-color__blue-60`)
2. **Theme tokens** - Semantic role-based (`$interactive`, `$text-primary`)
3. **Component tokens** - Component-specific (internal)

### Color System

**Primitives:**
```scss
$ibm-color__blue-10: #edf5ff;
$ibm-color__blue-60: #0f62fe;
$ibm-color__blue-100: #001141;
```

**Theme tokens (v11 naming):**
```scss
// Background
$background: #ffffff;
$background-hover: #e8e8e8;
$background-selected: #e0e0e0;

// Layer (surfaces)
$layer-01: #f4f4f4;
$layer-02: #ffffff;
$layer-03: #f4f4f4;

// Text
$text-primary: #161616;
$text-secondary: #525252;
$text-placeholder: #a8a8a8;
$text-on-color: #ffffff;

// Interactive
$interactive: #0f62fe;
$link-primary: #0f62fe;
$link-visited: #8a3ffc;

// Support (feedback)
$support-error: #da1e28;
$support-success: #24a148;
$support-warning: #f1c21b;
$support-info: #0043ce;
```

### Built-in Themes

| Theme | Background | Use Case |
|-------|------------|----------|
| White | `#ffffff` | Light mode default |
| g10 | `#f4f4f4` | Light mode subtle |
| g90 | `#262626` | Dark mode subtle |
| g100 | `#161616` | Dark mode default |

### Spacing Scale

**2px base, exponential scale:**
```scss
$spacing-01: 0.125rem;  // 2px
$spacing-02: 0.25rem;   // 4px
$spacing-03: 0.5rem;    // 8px
$spacing-04: 0.75rem;   // 12px
$spacing-05: 1rem;      // 16px
$spacing-06: 1.5rem;    // 24px
$spacing-07: 2rem;      // 32px
$spacing-08: 2.5rem;    // 40px
$spacing-09: 3rem;      // 48px
$spacing-10: 4rem;      // 64px
$spacing-11: 5rem;      // 80px
$spacing-12: 6rem;      // 96px
$spacing-13: 10rem;     // 160px
```

### Motion Tokens

**Durations:**
```scss
$duration-fast-01: 70ms;   // Micro-interactions
$duration-fast-02: 110ms;  // Small transitions
$duration-moderate-01: 150ms;
$duration-moderate-02: 240ms;
$duration-slow-01: 400ms;
$duration-slow-02: 700ms;  // Large transitions
```

**Easing (productive vs expressive):**
```scss
// Productive - efficient, minimal
$ease-productive-standard: cubic-bezier(0.2, 0, 0.38, 0.9);
$ease-productive-entrance: cubic-bezier(0, 0, 0.38, 0.9);
$ease-productive-exit: cubic-bezier(0.2, 0, 1, 0.9);

// Expressive - delightful, engaging
$ease-expressive-standard: cubic-bezier(0.4, 0.14, 0.3, 1);
$ease-expressive-entrance: cubic-bezier(0, 0, 0.3, 1);
$ease-expressive-exit: cubic-bezier(0.4, 0.14, 1, 1);
```

---

## Salesforce Lightning Design System

### Architecture Evolution

**SLDS 1:** Design tokens with Theo transformation
**SLDS 2:** CSS Custom Properties ("Styling Hooks")

### Naming Convention

```
--slds-g-{category}-{variant}-{number}     Global hooks
--slds-c-{component}-{property}            Component hooks
--_slds-*                                   Private/internal
--slds-s-*                                  System/internal
```

### Color System

**Surface colors:**
```css
--slds-g-color-surface-1: #ffffff;
--slds-g-color-surface-2: #f3f3f3;
--slds-g-color-on-surface-1: #181818;
```

**Accent colors:**
```css
--slds-g-color-accent-1: #0176d3;
--slds-g-color-accent-container-1: #e5f2fc;
--slds-g-color-on-accent-1: #ffffff;
```

**Feedback colors:**
```css
--slds-g-color-error-1: #ea001e;
--slds-g-color-error-container-1: #feded8;
--slds-g-color-success-1: #2e844a;
--slds-g-color-success-container-1: #cdefc4;
--slds-g-color-warning-1: #dd7a01;
--slds-g-color-warning-container-1: #fef0cd;
```

**Reference palettes (immutable):**
- Blue: `--slds-g-color-palette-blue-10` through `--slds-g-color-palette-blue-100`
- Neutral: `--slds-g-color-palette-neutral-10` through `--slds-g-color-palette-neutral-100`
- Same pattern for: green, red, orange, yellow, violet, indigo, teal

### Spacing System

```css
--slds-g-spacing-1: 0.25rem;  /* 4px */
--slds-g-spacing-2: 0.5rem;   /* 8px */
--slds-g-spacing-3: 0.75rem;  /* 12px */
--slds-g-spacing-4: 1rem;     /* 16px */
--slds-g-spacing-5: 1.25rem;  /* 20px */
--slds-g-spacing-6: 1.5rem;   /* 24px */
--slds-g-spacing-7: 1.75rem;  /* 28px */
--slds-g-spacing-8: 2rem;     /* 32px */
--slds-g-spacing-9: 2.25rem;  /* 36px */
--slds-g-spacing-10: 2.5rem;  /* 40px */
--slds-g-spacing-11: 2.75rem; /* 44px */
--slds-g-spacing-12: 3rem;    /* 48px */
```

### Component Hooks Example

```css
.slds-button {
  background-color: var(--slds-c-button-color-background, var(--slds-g-color-surface-1));
  color: var(--slds-c-button-text-color, var(--slds-g-color-on-surface-1));
  padding: var(--slds-c-button-spacing-block, var(--slds-g-spacing-2))
           var(--slds-c-button-spacing-inline, var(--slds-g-spacing-4));
}
```

---

## Google Material Design 3

### Three-Tier Architecture

**Reference tokens** (`--md-ref-*`): Concrete values
**System tokens** (`--md-sys-*`): Design decisions
**Component tokens**: Element-specific

### Dynamic Color System

Based on **HCT color space** (Hue, Chroma, Tone).

**Key colors (5):**
1. Primary - Brand color
2. Secondary - Supporting brand
3. Tertiary - Accent/contrast
4. Neutral - Backgrounds, surfaces
5. Neutral-variant - Outlines, text

**Tonal palette (13 tones per color):**
```
0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99, 100
```

### Reference Tokens

```css
/* Palette */
--md-ref-palette-primary0: #000000;
--md-ref-palette-primary10: #001f24;
--md-ref-palette-primary40: #006971;
--md-ref-palette-primary80: #4fd8eb;
--md-ref-palette-primary100: #ffffff;

/* Typeface */
--md-ref-typeface-brand: 'Roboto';
--md-ref-typeface-plain: 'Roboto';
```

### System Tokens

**Color roles:**
```css
/* Primary */
--md-sys-color-primary: var(--md-ref-palette-primary40);
--md-sys-color-on-primary: var(--md-ref-palette-primary100);
--md-sys-color-primary-container: var(--md-ref-palette-primary90);
--md-sys-color-on-primary-container: var(--md-ref-palette-primary10);

/* Surface */
--md-sys-color-surface: var(--md-ref-palette-neutral99);
--md-sys-color-on-surface: var(--md-ref-palette-neutral10);
--md-sys-color-surface-variant: var(--md-ref-palette-neutral-variant90);

/* Background */
--md-sys-color-background: var(--md-ref-palette-neutral99);
--md-sys-color-on-background: var(--md-ref-palette-neutral10);

/* Outline */
--md-sys-color-outline: var(--md-ref-palette-neutral-variant50);
--md-sys-color-outline-variant: var(--md-ref-palette-neutral-variant80);
```

**Typography scale:**
```css
--md-sys-typescale-display-large-font: var(--md-ref-typeface-brand);
--md-sys-typescale-display-large-size: 57px;
--md-sys-typescale-display-large-line-height: 64px;
--md-sys-typescale-display-large-weight: 400;
--md-sys-typescale-display-large-tracking: -0.25px;

--md-sys-typescale-body-medium-font: var(--md-ref-typeface-plain);
--md-sys-typescale-body-medium-size: 14px;
--md-sys-typescale-body-medium-line-height: 20px;
--md-sys-typescale-body-medium-weight: 400;
--md-sys-typescale-body-medium-tracking: 0.25px;
```

**Shape tokens:**
```css
--md-sys-shape-corner-none: 0px;
--md-sys-shape-corner-extra-small: 4px;
--md-sys-shape-corner-small: 8px;
--md-sys-shape-corner-medium: 12px;
--md-sys-shape-corner-large: 16px;
--md-sys-shape-corner-extra-large: 28px;
--md-sys-shape-corner-full: 9999px;
```

**Motion tokens:**
```css
/* Duration */
--md-sys-motion-duration-short1: 50ms;
--md-sys-motion-duration-short2: 100ms;
--md-sys-motion-duration-short3: 150ms;
--md-sys-motion-duration-short4: 200ms;
--md-sys-motion-duration-medium1: 250ms;
--md-sys-motion-duration-medium2: 300ms;
--md-sys-motion-duration-medium3: 350ms;
--md-sys-motion-duration-medium4: 400ms;
--md-sys-motion-duration-long1: 450ms;
--md-sys-motion-duration-long2: 500ms;

/* Easing */
--md-sys-motion-easing-emphasized: cubic-bezier(0.2, 0, 0, 1);
--md-sys-motion-easing-emphasized-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1);
--md-sys-motion-easing-emphasized-accelerate: cubic-bezier(0.3, 0, 0.8, 0.15);
--md-sys-motion-easing-standard: cubic-bezier(0.2, 0, 0, 1);
--md-sys-motion-easing-standard-decelerate: cubic-bezier(0, 0, 0, 1);
--md-sys-motion-easing-standard-accelerate: cubic-bezier(0.3, 0, 1, 1);
```

### Theme Builder

Material Theme Builder generates tokens from:
- Seed color (extracts tonal palette)
- Image (derives colors via quantization)

**Export formats:** Android XML, Jetpack Compose, CSS, Flutter, Design System Package

---

## Shopify Polaris

### Architecture

**Two tiers:**
1. Private primitives (internal color palette)
2. Public semantic tokens (consumer-facing)

**Package:** `@shopify/polaris-tokens`

### Naming Convention

```
--p-{category}-{element}-{role}-{prominence}-{state}
```

### Color Tokens

```css
/* Background */
--p-color-bg: #ffffff;
--p-color-bg-surface: #ffffff;
--p-color-bg-surface-hover: #f6f6f7;
--p-color-bg-surface-active: #f1f2f3;
--p-color-bg-surface-selected: #f2f7fe;
--p-color-bg-surface-disabled: #fafbfb;

/* Text */
--p-color-text: #202223;
--p-color-text-secondary: #6d7175;
--p-color-text-disabled: #8c9196;
--p-color-text-inverse: #ffffff;

/* Border */
--p-color-border: #8c9196;
--p-color-border-hover: #6d7175;
--p-color-border-disabled: #d2d5d8;

/* Interactive */
--p-color-text-interactive: #2c6ecb;
--p-color-text-interactive-hover: #1f5199;
--p-color-text-interactive-active: #164481;
--p-color-text-interactive-disabled: #6d7175;

/* Feedback */
--p-color-text-critical: #d72c0d;
--p-color-bg-critical: #fed3d1;
--p-color-text-success: #008060;
--p-color-bg-success: #aee9d1;
--p-color-text-warning: #916a00;
--p-color-bg-warning: #ffea8a;
```

### Spacing Tokens

**4px base with multiplier naming:**
```css
--p-space-0: 0;
--p-space-025: 1px;
--p-space-050: 2px;
--p-space-100: 4px;    /* 4 × 1 */
--p-space-150: 6px;
--p-space-200: 8px;    /* 4 × 2 */
--p-space-300: 12px;   /* 4 × 3 */
--p-space-400: 16px;   /* 4 × 4 */
--p-space-500: 20px;   /* 4 × 5 */
--p-space-600: 24px;   /* 4 × 6 */
--p-space-800: 32px;   /* 4 × 8 */
--p-space-1000: 40px;
--p-space-1200: 48px;
--p-space-1600: 64px;
--p-space-2000: 80px;
--p-space-2400: 96px;
--p-space-2800: 112px;
--p-space-3200: 128px;
```

### Shadow Tokens

```css
--p-shadow-100: 0px 1px 0px rgba(0, 0, 0, 0.05);
--p-shadow-200: 0px 1px 2px rgba(0, 0, 0, 0.15);
--p-shadow-300: 0px 4px 6px -2px rgba(0, 0, 0, 0.2);
--p-shadow-400: 0px 8px 16px -4px rgba(0, 0, 0, 0.22);
--p-shadow-500: 0px 12px 20px -8px rgba(0, 0, 0, 0.24);
--p-shadow-600: 0px 20px 20px -8px rgba(0, 0, 0, 0.28);

/* Inset shadows */
--p-shadow-inset-100: inset 0px 1px 2px rgba(0, 0, 0, 0.15);
--p-shadow-inset-200: inset 0px 2px 4px rgba(0, 0, 0, 0.2);
```

### Motion Tokens

```css
/* Duration */
--p-motion-duration-0: 0ms;
--p-motion-duration-50: 50ms;
--p-motion-duration-100: 100ms;
--p-motion-duration-150: 150ms;
--p-motion-duration-200: 200ms;
--p-motion-duration-250: 250ms;
--p-motion-duration-300: 300ms;
--p-motion-duration-350: 350ms;
--p-motion-duration-400: 400ms;
--p-motion-duration-450: 450ms;
--p-motion-duration-500: 500ms;

/* Easing */
--p-motion-ease: cubic-bezier(0.25, 0.1, 0.25, 1);
--p-motion-ease-in: cubic-bezier(0.42, 0, 1, 1);
--p-motion-ease-out: cubic-bezier(0, 0, 0.58, 1);
--p-motion-ease-in-out: cubic-bezier(0.42, 0, 0.58, 1);
--p-motion-linear: cubic-bezier(0, 0, 1, 1);

/* Keyframes */
--p-motion-keyframes-bounce: /* bounce animation */
--p-motion-keyframes-fade-in: /* fade-in animation */
--p-motion-keyframes-pulse: /* pulse animation */
--p-motion-keyframes-spin: /* spin animation */
```

### Border Tokens

```css
--p-border-radius-050: 2px;
--p-border-radius-100: 4px;
--p-border-radius-150: 6px;
--p-border-radius-200: 8px;
--p-border-radius-300: 12px;
--p-border-radius-400: 16px;
--p-border-radius-500: 20px;
--p-border-radius-750: 30px;
--p-border-radius-full: 9999px;

--p-border-width-025: 1px;
--p-border-width-050: 2px;
--p-border-width-100: 4px;
```

### Z-Index Tokens

```css
--p-z-index-1: 100;
--p-z-index-2: 400;
--p-z-index-3: 510;
--p-z-index-4: 512;
--p-z-index-5: 513;
--p-z-index-6: 514;
--p-z-index-7: 515;
--p-z-index-8: 516;
--p-z-index-9: 517;
--p-z-index-10: 518;
--p-z-index-11: 519;
--p-z-index-12: 520;
```

### Export Formats

- CSS Custom Properties
- Sass variables
- JavaScript/TypeScript objects
- JSON
- Full TypeScript type definitions

---

## Comparison Summary

| Aspect | Carbon | Lightning | Material 3 | Polaris |
|--------|--------|-----------|------------|---------|
| Tiers | 3 | 2 | 3 | 2 |
| Theming | 4 built-in | Hooks | Dynamic | Light/dark |
| Spacing base | 2px | 4px | 4px | 4px |
| Color naming | Numbered | Semantic | Tonal | Semantic |
| Package | Modular | Monolithic | Per-platform | Single |
| Primary format | Sass | CSS vars | Platform-specific | Multi-format |
