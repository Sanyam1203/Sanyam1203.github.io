# Design System Specification: High-Tech Precision

## 1. Overview & Creative North Star

**Creative North Star: "The Kinetic Monolith"**
This design system is built on the philosophy of "Precision Engineering through Light." It moves away from the static, boxed nature of standard UI, favoring a cinematic, editorial experience that feels like a high-end EV dashboard or an aerospace interface. 

The aesthetic is driven by the tension between "The Monolith" (the deep `background` and `surface` blacks) and "The Kinetic" (the vibrant, glowing `primary` cyan). We break the traditional grid through **intentional asymmetry**: large-scale display typography may bleed off the container, and interactive elements utilize glassmorphism to feel as though they are floating in a three-dimensional dark space. This system is not a template; it is a signature atmosphere of speed, luxury, and technological dominance.

---

## 2. Colors & Surface Philosophy

The palette is a high-contrast study in depth. It utilizes the "Dark Mode" spectrum to create a sense of infinite space, punctuated by electric cyan highlights.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning or layout containment. Boundaries must be defined solely through background color shifts.
*   *Example:* A section using `surface-container-low` (#1B1B1D) sitting on a `background` (#131315) creates a sophisticated, soft-edge transition that feels "carved" rather than "outlined."

### Surface Hierarchy & Nesting
Treat the UI as physical layers of stacked obsidian and frosted glass.
*   **Depth Level 0 (Base):** `background` (#131315).
*   **Depth Level 1 (Sectioning):** `surface-container-low` (#1B1B1D).
*   **Depth Level 2 (Cards/Interaction):** `surface-container-highest` (#353437).
*   **The Nesting Rule:** Use `surface-container-lowest` (#0E0E10) inside higher surfaces to create "inset" areas for data or media, mimicking the recessed bays of a high-tech console.

### Signature Textures & Glass
*   **The Glass Rule:** For floating modals or navigation bars, use `surface-variant` (#353437) at 60% opacity with a `backdrop-filter: blur(20px)`.
*   **Kinetic Gradients:** Hero actions and primary states should never be flat. Use a linear gradient (45-degree angle) from `primary` (#97FDFF) to `primary-container` (#3FE6E8) to provide "visual soul" and a metallic, automotive sheen.

---

## 3. Typography

The type system is a dialogue between the "Sharp" and the "Human."

*   **Display & Headlines (Space Grotesk):** This is the "Sharp" element. It conveys precision engineering. Use `display-lg` (3.5rem) with tighter letter-spacing (-0.02em) for high-impact editorial moments. Headlines should be unapologetically bold to command the dark canvas.
*   **Body & Titles (Manrope):** This is the "Human" element. Manrope provides a warmer, more legible counterpoint to the technicality of Space Grotesk. It ensures that complex data remains accessible and premium.
*   **Labels (Space Grotesk):** For micro-copy and technical readouts (e.g., `label-sm`), use Space Grotesk in All-Caps with +0.05em tracking to mimic the look of etched serial numbers on carbon fiber.

---

## 4. Elevation & Depth

We eschew traditional drop shadows for **Tonal Layering** and **Luminous Depth.**

*   **The Layering Principle:** Place a `surface-container-lowest` card on a `surface-container-low` section. The human eye will perceive the lift based on the tonal contrast alone, maintaining a sleek, modern profile.
*   **Ambient Shadows:** When an element must float (e.g., a critical notification), use a "Shadow-Glow." The shadow should have a blur radius of 40px and a very low opacity (6%) of the `primary` color (#97FDFF) rather than black. This simulates the light from the UI glowing against the background.
*   **The "Ghost Border" Fallback:** If accessibility requires a stroke, use `outline-variant` (#3B494C) at 15% opacity. This "Ghost Border" provides a hint of structure without breaking the seamless black aesthetic.

---

## 5. Components

### Buttons
*   **Primary:** A gradient from `primary` to `primary-container`. Text color must be `on-primary` (#003738) for maximum contrast. Radius: `sm` (0.125rem) for a sharp, machined look.
*   **Secondary:** No fill. `Ghost Border` (outline-variant at 20%) with a glassmorphic background blur.
*   **Interaction:** On hover, the primary button should emit an `ambient-glow` shadow using the `primary-fixed` token.

### Cards & Lists
*   **Constraint:** **Never use horizontal divider lines.** 
*   **Solution:** Separate list items by alternating between `surface-container` and `surface-container-low`, or use vertical whitespace (1.5rem+) from the spacing scale.
*   **Card Styling:** Use `lg` (0.5rem) roundedness. Cards should feature a 1px top-edge highlight using `primary` at 10% opacity to simulate overhead lighting on a metallic surface.

### Input Fields
*   **Base State:** `surface-container-lowest` background with a subtle `outline-variant` bottom-border only. 
*   **Focus State:** The bottom border transforms into a `primary` (#97FDFF) glow, and the label (`label-md`) shifts to `primary`.

### Data Visualization (EV-Tech specific)
*   **Progress Gauges:** Use circular glass containers. The "fill" should be a gradient of `primary`, while the "empty" track should be `surface-container-highest`.

---

## 6. Do's and Don'ts

### Do
*   **DO** use extreme typographic scale. Pair `display-lg` headers with `body-sm` text for an editorial, high-fashion tech feel.
*   **DO** embrace "True Black" (`#0E0E10`) for deep inset areas to create high-end visual weight.
*   **DO** use `tertiary` (#FFEAC0) sparingly as a "Warning" or "Alert" highlight to contrast against the dominant cyan.

### Don't
*   **DON'T** use `md` or `xl` roundedness on primary action buttons. Keep them `sm` (0.125rem) to maintain the "Precision Engineering" vibe.
*   **DON'T** use 100% opaque borders. They clutter the UI and break the Monolith aesthetic.
*   **DON'T** use pure white (#FFFFFF) for body text. Always use `on-surface` (#E5E1E4) to prevent eye strain against the dark background.