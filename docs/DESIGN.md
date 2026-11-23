# DESIGN.md: dotandkey.com

> Design reference saved with PocketUI from dotandkey.com.
> Build new UI in this style. Values and colour roles are read from the source's own CSS; adjust any that look wrong.

## Colors

| Role | Value |
| --- | --- |
| Page background | `#ffffff` |
| Text | `#000000` |
| Muted text (secondary copy, captions) | `#1a1a1a` |
| Surface (cards, panels, inputs) | `#fff5fa` |
| Surface 2 | `#e8e8e8` |
| Border | `#e5e5e5` |
| Primary (buttons, links, key actions) | `#ff4081` |
| Accent | `#82b51b` |
| Focus ring | `#111111` |

Also used: `#ff40b1`, `#d7d7d7`, `#222222`, `#ff803a`, `#22bce0`, `#eeeeee`, `#333333`, `#ff2ea6`, `#ff3e80`, `#f4576c`, `#ff5ca0`, `#ff84cd`

## Typography

- **Main typeface:** Poppins-SemiBold
- **Also used:** Poppins-Medium
- **Also used:** Poppins-Regular
- **Also used:** Poppins-Bold
- **Sizes in use:** 10px, 11px, 12px, 13px, 14px, 15px, 16px, 18px, 20px, 24px
- **Weights in use:** 400, 500, 600, 700, 800

## Shape & spacing

- **Corner radius:** 3px, 5px, 6px, 7px, 8px, 10px, 12px, 13px, 16px, 999px
- **Shadows:** `0 0 6px #d7d7d7` · `0 1px 3px #0000001a,0 1px 2px #0000000f` · `0 1px 4px #00000040` · `0 2px 10px #0000001a`
- **Spacing scale:** 2px, 4px, 5px, 6px, 8px, 10px, 12px, 15px, 16px, 20px

## Motion

- **Durations:** 150ms, 200ms, 300ms
- **Easing:** `ease`, `cubic-bezier(.4,0,.2,1)`, `cubic-bezier(.22,1,.36,1)`

## Rules

- Use these values as the design tokens for new UI; don't introduce new colours or fonts without a reason.
- Keep the primary colour for actions and highlights; let neutrals carry the layout.
- Animate colour, opacity and shadow on hover and focus, at these durations; don't animate layout.
- Text on the background is 21:1. Keep new text at 4.5:1 or more (WCAG AA).
- Keyboard focus shows as `#111111`: give every link, button and field that visible focus, plus hover, pressed and disabled states.
- Take the feel, not the content: no text, logos or images from the source.
