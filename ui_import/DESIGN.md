---
name: Liquid Precision
colors:
  surface: '#0c1324'
  surface-dim: '#0c1324'
  surface-bright: '#33394c'
  surface-container-lowest: '#070d1f'
  surface-container-low: '#151b2d'
  surface-container: '#191f31'
  surface-container-high: '#23293c'
  surface-container-highest: '#2e3447'
  on-surface: '#dce1fb'
  on-surface-variant: '#ccc3d8'
  inverse-surface: '#dce1fb'
  inverse-on-surface: '#2a3043'
  outline: '#958da1'
  outline-variant: '#4a4455'
  surface-tint: '#d2bbff'
  primary: '#d2bbff'
  on-primary: '#3f008e'
  primary-container: '#7c3aed'
  on-primary-container: '#ede0ff'
  inverse-primary: '#732ee4'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb3ad'
  on-tertiary: '#68000a'
  tertiary-container: '#c6252b'
  on-tertiary-container: '#ffdfdc'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#eaddff'
  primary-fixed-dim: '#d2bbff'
  on-primary-fixed: '#25005a'
  on-primary-fixed-variant: '#5a00c6'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#930013'
  background: '#0c1324'
  on-background: '#dce1fb'
  surface-variant: '#2e3447'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-mono:
    fontFamily: Geist Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.0'
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  base: 4px
  container-gap: 24px
  panel-padding: 32px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The brand personality of the design system is analytical, futuristic, and unshakeable. Designed for high-frequency sentiment analysis, it bridges the gap between a high-end financial terminal and a clean, generative AI interface. The aesthetic is "Dark Mode First," prioritizing eye comfort during deep-focus sessions while maintaining an elite, developer-centric feel.

The design style is a fusion of **Glassmorphism** and **Minimalism**. It utilizes "Liquid Glass" surfaces—highly transparent, blurred modules—to create a sense of depth and data layering. This is paired with a **Bento Grid 2.0** layout philosophy, where information is compartmentalized into asymmetric, modular units that suggest order amidst complex data streams. The emotional response should be one of absolute clarity and technological sophistication.

## Colors

This design system utilizes a deep, nocturnal foundation to make data accents pop. The palette is structured to communicate state and sentiment instantly:

- **Primary Background**: A deep Slate-Black (#020617) provides a canvas that eliminates visual noise.
- **Electric Violet (#7C3AED)**: Used for primary actions, branding highlights, and "neutral but active" states.
- **Emerald Mint (#10B981)**: Specifically reserved for positive sentiment, "True" verifications, and growth indicators.
- **High-Contrast Crimson (#EF4444)**: Reserved for negative sentiment, "False" flags, and critical alerts.

Glass panels use a specialized "Liquid" fill (60% opacity) to allow the deep background to subtly bleed through, ensuring the UI feels cohesive and layered rather than flat.

## Typography

The typography system is built on **Geist**, a typeface that embodies technical precision and modern minimalism. 

- **Headlines**: Use tight letter-spacing and heavy weights to create a "terminal" impact. 
- **Data Points**: For sentiment scores, timestamps, and ticker symbols, the design system employs **Geist Mono** to ensure every character occupies a predictable space, aiding in rapid scanning of numerical data.
- **Readability**: Body text maintains a generous line height (1.6) to ensure that even long-form news snippets remain legible against the dark, translucent backgrounds.

## Layout & Spacing

The layout follows a **Bento Grid 2.0** model—an asymmetric fixed-grid system that adapts fluidly to the viewport.

- **Desktop**: A 12-column grid with a 24px gutter. Components should span varying column widths (e.g., a 4-column "Sentiment Pulse" card next to an 8-column "Trend Analysis" graph) to create visual interest and hierarchy.
- **The Rail**: A minimalist sidebar (72px width) houses primary navigation icons, keeping the focus entirely on the data panels.
- **Modular Padding**: Every panel uses a consistent 32px internal padding to maintain a premium, "breathable" feel, even when data density is high.
- **Mobile**: The grid collapses into a single-column stack, but maintains the 28px corner radius and 16px outer margins to preserve the brand's silhouette.

## Elevation & Depth

Depth in this design system is achieved through **Backdrop Refraction** rather than traditional shadows. 

1.  **Liquid Glass Layer**: The primary container layer uses a 20px background blur (backdrop-filter) and a 1px solid border at 10% white opacity. This creates a "frosted" look that separates the panel from the background.
2.  **Illumination**: Instead of drop shadows, active or hovered elements utilize an **Outer-Glow**. For example, a hovered module emits a soft, 15px radial glow of Electric Violet (#7C3AED) at 20% opacity.
3.  **The Stack**:
    *   *Level 0*: Primary Background (#020617).
    *   *Level 1*: Glass Modules (20px blur).
    *   *Level 2*: Overlays/Modals (40px blur, darker fill).

## Shapes

The shape language is defined by extreme roundedness contrasted against sharp, technical data. 

- **Bento Modules**: All main containers must use a **28px corner radius**. This high degree of rounding provides a "friendly-tech" counter-balance to the dark, aggressive color palette.
- **Interactive Elements**: Buttons and input fields follow a "Pill" philosophy (rounding-xl), ensuring they are easily distinguishable from the structural panels.
- **Nested Elements**: When placing elements inside a module (like a button inside a card), use a smaller 12px radius to maintain visual harmony (concentric rounding).

## Components

### Bento Modules
The core unit of the UI. Must feature the 20px background blur and 28px radius. Titles within modules should be paired with a Geist Mono label to indicate the "Data Source" or "Confidence Score."

### Sentiment Indicators
Visualized as "Pills." Positive sentiment uses a subtle Emerald Mint glow. Negative sentiment uses a Crimson outline. The text inside should always be uppercase Geist Mono.

### Interaction States
- **Hover**: Panels should lift 4px on the Y-axis with a subtle violet outer-glow.
- **Active**: Buttons utilize a "Squishy" interaction—a slight scale-down (0.98) on click to mimic physical feedback.

### Inputs
Search bars and filter chips should be semi-transparent with a 1px border that brightens to Electric Violet on focus. Use "Glassmorphic" dropdowns that inherit the 20px blur of the parent container.

### Modern Rail
The vertical navigation rail should be nearly transparent, using only high-contrast icons that transition from 50% opacity to 100% Emerald Mint when selected.