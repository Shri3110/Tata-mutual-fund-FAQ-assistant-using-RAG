---
name: Professional Financial Assistant
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#45464d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#001a42'
  on-tertiary-container: '#3980f4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#d8e2ff'
  tertiary-fixed-dim: '#adc6ff'
  on-tertiary-fixed: '#001a42'
  on-tertiary-fixed-variant: '#004395'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  caption-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 0.5rem
  sm: 1rem
  md: 1.5rem
  lg: 2.5rem
  xl: 4rem
  container-max: 1200px
  gutter: 24px
---

## Brand & Style
The design system is engineered to project stability, growth, and unwavering reliability. As a financial FAQ assistant, the interface must prioritize clarity over decoration, ensuring users feel secure while navigating complex mutual fund data.

The style is **Modern Corporate Minimalism**. It utilizes a "density-first" approach where information is organized into clear modules, supported by generous whitespace to reduce cognitive load. The aesthetic is clean and high-fidelity, avoiding unnecessary ornaments to maintain a focus on expert guidance and data integrity.

## Colors
The palette is rooted in a **Deep Navy** primary, which provides a foundation of authority and institutional trust. This is contrasted by **Emerald Green**, used strategically to signify financial growth, positive performance, and "success" states.

- **Primary (Deep Navy):** Used for headers, primary text, and high-emphasis navigational elements.
- **Secondary (Emerald Green):** Reserved for growth indicators, call-to-action buttons, and completion states.
- **Tertiary (Financial Blue):** A brighter blue used for links and interactive accents to distinguish them from static primary text.
- **Surface & Backgrounds:** Use off-whites and extremely light cool-grays (#F8FAFC) to keep the interface feeling airy and modern.

## Typography
This design system utilizes **Inter** for all roles to leverage its exceptional legibility and systematic feel. 

- **Hierarchy:** Use semi-bold (600) for headlines to establish a clear architectural path for the eye.
- **Readability:** Body text is set with a slightly increased line-height (1.5x) to ensure long FAQ answers remain approachable and easy to scan.
- **Data Display:** For fund numbers and percentages, use Medium (500) weights to ensure they stand out within body copy without the aggression of a full Bold.

## Layout & Spacing
The layout follows a **8px square grid system** to ensure mathematical harmony across all components.

- **Desktop:** A 12-column fixed grid with a 1200px max-width, centered on the viewport.
- **Chat Interface:** The assistant window should utilize a focused "Stage" layout, with a width of 720px for optimal reading line length.
- **Mobile:** A fluid 4-column layout with 16px side margins. 
- **Padding:** Use "Generous" padding (24px+) for container cards to reinforce the clean, high-end feel of the design system.

## Elevation & Depth
Depth is created through **Ambient Shadows** rather than harsh borders. This design system uses three levels of elevation to separate the assistant from the background content:

1.  **Flat (Level 0):** Background surfaces and secondary input fields.
2.  **Raised (Level 1):** Chat bubbles and standard cards. Use a soft shadow: `0 4px 12px rgba(15, 23, 42, 0.05)`.
3.  **Overlay (Level 2):** Modals, dropdown menus, and active search results. Use a more pronounced shadow: `0 12px 32px rgba(15, 23, 42, 0.1)`.

Avoid using pure black for shadows; always tint shadows with the primary Navy color to maintain a cohesive, sophisticated atmosphere.

## Shapes
The shape language is defined by **modern, approachable soft-rectangles**. 

- **Standard Components:** Use a base radius of 12px for buttons and small input fields.
- **Large Components:** Use a radius of 16px for fund cards, chat containers, and modal windows.
- **Chat Bubbles:** The assistant's bubbles should have a 16px radius on all corners except the bottom-left (set to 4px) to indicate the source of the message.

## Components
### Buttons
- **Primary:** Solid Emerald Green with white text. High-contrast and rounded (12px).
- **Secondary:** Transparent background with a 1px Navy border. For less urgent actions.

### Chat Bubbles
- **User:** Light Gray (#F1F5F9) with Primary Navy text, aligned to the right.
- **Assistant:** Primary Navy background with White text, aligned to the left, featuring a small "Expert" badge or icon.

### Input Fields
- **Search:** Large, 16px rounded height with a leading "Magnifying Glass" icon. Use a subtle 1px border (#E2E8F0) that thickens and changes to Blue on focus.
- **Placeholder Text:** Use a light neutral (#94A3B8) with a helpful prompt like "Ask about expense ratios...".

### Informative Fund Cards
- **Structure:** A white card with a 16px radius and Level 1 shadow. 
- **Content:** Header with the fund name in Title-MD, a divider line, and a 2-column grid for "NAV" and "1Y Return" percentages.

### Chips & Tags
- Used for suggested questions. Pill-shaped with a light blue background and Navy text to encourage interaction without looking like primary buttons.