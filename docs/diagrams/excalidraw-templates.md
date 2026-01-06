# Excalidraw Templates for Quick Diagram Creation

These templates can be used to quickly create diagrams by importing into Excalidraw.

## How to Use Templates

1. Go to https://excalidraw.com
2. Click the menu icon (≡) → Open
3. Copy template JSON from below
4. Paste into a text file with `.excalidraw` extension
5. Open that file in Excalidraw
6. Customize colors, text, and layout
7. Export as PNG + SVG

## Template 1: 4-Layer Architecture

**Filename:** `4-layer-architecture-template.excalidraw`

This template provides the basic 4-layer structure for the System Architecture diagram.

**To customize:**
- Replace placeholder text with actual component names
- Adjust colors to exact hex codes: #4A90E2, #7ED321, #F5A623, #BD10E0
- Add arrows between layers
- Add annotations and metrics

**Structure:**
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  LAYER 1    │  │  LAYER 2    │  │  LAYER 3    │  │  LAYER 4    │
│  Detection  │→ │  Memory     │→ │  Recovery   │→ │  Automation │
│  (Blue)     │  │  (Green)    │  │  (Orange)   │  │  (Purple)   │
│             │  │             │  │             │  │             │
│ Component 1 │  │ Component 1 │  │ Component 1 │  │ Component 1 │
│ Component 2 │  │ Component 2 │  │ Component 2 │  │ Component 2 │
│ Component 3 │  │ Component 3 │  │ Component 3 │  │ Component 3 │
│ Component 4 │  │ Component 4 │  │ Component 4 │  │ Component 4 │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## Template 2: Vertical Flow Diagram

**Filename:** `vertical-flow-template.excalidraw`

Use for Detector Priority Flow diagram.

**Structure:**
```
┌───────────────┐
│  Start/Input  │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Process 1   │
└───────┬───────┘
        │
        ▼
    ┌───┴───┐
    │Decision│
    └───┬───┘
   Yes  │  No
    ┌───┴───┐
    ▼       ▼
┌────────┐ ┌────────┐
│Action A│ │Action B│
└────────┘ └────────┘
```

## Template 3: Side-by-Side Comparison

**Filename:** `comparison-template.excalidraw`

Use for Before/After Workflow diagram.

**Structure:**
```
┌──────────────────┬──────────────────┐
│     BEFORE       │      AFTER       │
├──────────────────┼──────────────────┤
│                  │                  │
│  Problem 1       │  Solution 1      │
│  ❌ Description  │  ✅ Description  │
│                  │                  │
│  Problem 2       │  Solution 2      │
│  ❌ Description  │  ✅ Description  │
│                  │                  │
│  Problem 3       │  Solution 3      │
│  ❌ Description  │  ✅ Description  │
│                  │                  │
├──────────────────┼──────────────────┤
│  Metrics (Bad)   │  Metrics (Good)  │
└──────────────────┴──────────────────┘
```

## Template 4: Horizontal Timeline

**Filename:** `timeline-template.excalidraw`

Use for Session Lifecycle diagram.

**Structure:**
```
Milestone 1    Milestone 2    Milestone 3    Milestone 4
    │              │              │              │
    ▼              ▼              ▼              ▼
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ Event  │     │ Event  │     │ Event  │     │ Event  │
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ Action │     │ Action │     │ Action │     │ Action │
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│Outcome │     │Outcome │     │Outcome │     │Outcome │
└────────┘     └────────┘     └────────┘     └────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━→
                        Time
```

## Color Palette Quick Reference

Copy these hex codes for consistent styling:

**Primary Colors:**
```
Detection (Blue):    #4A90E2
Memory (Green):      #7ED321
Recovery (Orange):   #F5A623
Automation (Purple): #BD10E0
```

**Supporting Colors:**
```
Text (Dark):         #4A4A4A
Text (Light):        #9B9B9B
Background (Light):  #F9F9F9
Connections (Gray):  #9B9B9B
```

**Semantic Colors:**
```
Success (Green):     #7ED321
Warning (Yellow):    #FFD700
Error (Red):         #D0021B
Info (Blue):         #4A90E2
```

## Shape Guidelines

**Boxes:**
- Border radius: 8px
- Border width: 2px
- Fill: White or light tint of layer color
- Shadow: 2px offset, 10% opacity

**Arrows:**
- Width: 2px
- Color: #9B9B9B (gray)
- End style: Arrowhead
- Curve: Slight for visual flow

**Text:**
- Font: Inter, Roboto, or default sans-serif
- Headings: 24pt bold
- Labels: 16pt regular
- Annotations: 14pt light

**Icons:**
- Style: Line icons (not filled)
- Size: 24x24px
- Color: Match layer color
- Sources: Heroicons, Feather Icons

## Quick Start Steps

### Create System Architecture (30 min)

1. **Open Excalidraw** (excalidraw.com)

2. **Set Canvas Size:**
   - Click settings
   - Set to 1200x800px

3. **Create Layer Boxes (10 min):**
   - Draw 4 rectangles
   - Apply colors (Blue, Green, Orange, Purple)
   - Add layer names as headers

4. **Add Components (10 min):**
   - Draw 4 smaller boxes inside each layer
   - Add component names:
     - Detection: Project Switch, Keyword, Entity Mention, Token Threshold
     - Memory: MCP Graph, SQLite, Cache, Retry Logic
     - Recovery: Load Context, Resume Points, Update CLAUDE.md, Checkpoint
     - Automation: SessionStart, SessionEnd, Post-commit, Scheduler

5. **Add Arrows (5 min):**
   - Connect layers left to right
   - Connect components to show data flow

6. **Add Annotations (5 min):**
   - Top right: "214 Tests | 93% Coverage | <1ms Performance"
   - Bottom left: "Modular • Extensible • Production-Ready"
   - Bottom components: "Budget Manager: 5K tokens", "User: Zero Friction"

7. **Export:**
   - File → Export Image → PNG (2x scale)
   - File → Export Image → SVG
   - File → Save as → `.excalidraw` source file

### Create Before/After Comparison (30 min)

1. **Create Split Canvas:**
   - Draw large rectangle (1200x600)
   - Add vertical line down middle
   - Label left "BEFORE (Manual)", right "AFTER (Automated)"

2. **Left Side (Before - 15 min):**
   - Background tint: Light red (#FFF5F5)
   - Add rows for each stage:
     - Session Ends: "❌ Context lost"
     - New Session: "⏱️ 15-30 min explaining"
     - Working: "❌ Search old chats"
     - Context Full: "❌ Panic! Lose everything?"
   - Bottom metrics: "TIME WASTED: 2-5 hours/week"

3. **Right Side (After - 15 min):**
   - Background tint: Light green (#F5FFF5)
   - Add rows matching left:
     - Session Ends: "✅ Auto-checkpoint"
     - New Session: "✅ Auto-resume"
     - Working: "✅ Memory graph query"
     - Context Full: "✅ Proactive preservation"
   - Bottom metrics: "TIME SAVED: 2-5 hours/week"

4. **Export:**
   - PNG at 1200x600
   - Optimize with TinyPNG

### Create Skills Matrix (30 min - Use Canva)

1. **Open Canva** (canva.com)
   - Create custom size: 800x1000px

2. **Use Template:**
   - Search "Skills infographic"
   - Select grid or bar chart template

3. **Create 5 Sections:**
   - Strategic Product
   - Systems Thinking
   - UX Design
   - Technical Execution
   - AI-First Development

4. **Add Skills with Bars:**
   - Copy percentages from specs (docs/diagrams/README.md)
   - Create horizontal bars
   - Apply gradient (blue → green)
   - Add checkmarks

5. **Export:**
   - Download as PNG
   - Optimize with TinyPNG

## Alternative: draw.io Templates

For more precise diagrams, use draw.io (diagrams.net):

1. **Open draw.io**
2. **Start with Template:**
   - File → New → From Template
   - Choose "Cloud Architecture" or "Flowchart"

3. **Customize:**
   - Replace shapes with your content
   - Apply color scheme from palette
   - Align precisely with alignment tools

4. **Export:**
   - File → Export as → PNG (300 DPI)
   - File → Export as → SVG
   - File → Save as → `.drawio` source

## Tips for Fast Creation

**Speed Tips:**
- Use copy-paste for repeated elements
- Create one component box, then duplicate
- Use alignment tools for clean layout
- Save color palette in tool for quick access
- Use keyboard shortcuts (Ctrl+C, Ctrl+V, Ctrl+D for duplicate)

**Quality Tips:**
- Zoom to 100% to check readability
- Use grid/snap for alignment
- Keep consistent spacing
- Test colors against white and dark backgrounds
- Preview at actual display size

**Efficiency Tips:**
- Start with simplest diagram (System Architecture)
- Reuse elements across diagrams (arrows, boxes)
- Create color palette once, apply everywhere
- Export all formats at once
- Batch optimize PNGs with TinyPNG

## Validation Before Export

**Quick Check:**
- [ ] All text spelled correctly
- [ ] Colors match hex codes exactly
- [ ] Arrows point the right direction
- [ ] Labels are clear and readable
- [ ] No overlapping elements
- [ ] Proper spacing and alignment

**Export Check:**
- [ ] PNG at 2x resolution
- [ ] SVG optimized
- [ ] File size reasonable (<500KB PNG)
- [ ] Both formats render correctly
- [ ] Source file saved

## Resources

**Icon Libraries:**
- Heroicons: https://heroicons.com (free, MIT)
- Feather Icons: https://feathericons.com (free, MIT)
- Material Icons: https://material.io/icons (free, Apache)

**Color Tools:**
- Color contrast checker: https://webaim.org/resources/contrastchecker/
- Color palette generator: https://coolors.co
- Accessibility validator: https://www.tpgi.com/color-contrast-checker/

**Optimization Tools:**
- PNG compression: https://tinypng.com
- SVG optimization: https://jakearchibald.github.io/svgomg/
- Image analysis: https://www.websiteplanet.com/webtools/imagecompressor/

---

**These templates provide a fast starting point. Customize with actual content from the specification documents, and you'll have professional diagrams in minimal time.**

**Remember: Consistency matters more than perfection. Use the color scheme, follow the layouts, and export at the right sizes.**
