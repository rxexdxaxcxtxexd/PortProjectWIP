# Visual Design Specifications for Portfolio
## Context-Aware Memory Management System

**Purpose:** Specifications for creating architecture diagrams, infographics, and visual assets

**Tools:** Excalidraw, draw.io, Figma, Canva

---

## 1. System Architecture Diagram (Hero Visual)

### Purpose
Primary visual for portfolio, GitHub README, and presentations. Shows 4-layer architecture at a glance.

### Specifications

**Dimensions:** 1200x800px (3:2 ratio)
**Format:** PNG with transparent background, SVG for web
**Color Scheme:** Modern, professional, accessible

#### Layout (Left-to-Right Flow)

```
┌─────────────────────────────────────────────────────────────┐
│                   SYSTEM ARCHITECTURE                       │
│         Context-Aware Memory Management System              │
└─────────────────────────────────────────────────────────────┘

[Layer 1: DETECTION]  →  [Layer 2: MEMORY]  →  [Layer 3: RECOVERY]  →  [Layer 4: AUTOMATION]

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Trigger Layer   │    │  Persistence     │    │  Resumption      │    │  Integration     │
│                  │    │                  │    │                  │    │                  │
│ ┌──────────────┐ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │
│ │Project Switch│ │    │ │ MCP Memory   │ │    │ │Load Previous │ │    │ │SessionStart  │ │
│ │  Priority 1  │ │───>│ │   Graph      │ │───>│ │  Context     │ │───>│ │    Hook      │ │
│ └──────────────┘ │    │ │              │ │    │ └──────────────┘ │    │ └──────────────┘ │
│                  │    │ │ Entities &   │ │    │                  │    │                  │
│ ┌──────────────┐ │    │ │  Relations   │ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │
│ │  Keyword     │ │    │ │              │ │    │ │Smart Resume  │ │    │ │SessionEnd    │ │
│ │  Priority 2  │ │───>│ │ SQLite DB    │ │───>│ │   Points     │ │───>│ │    Hook      │ │
│ └──────────────┘ │    │ └──────────────┘ │    │ └──────────────┘ │    │ └──────────────┘ │
│                  │    │                  │    │                  │    │                  │
│ ┌──────────────┐ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │
│ │Entity Mention│ │    │ │Cache Layer   │ │    │ │Update CLAUDE │ │    │ │Git Post-     │ │
│ │  Priority 3  │ │───>│ │ (5min TTL)   │ │───>│ │     .md      │ │───>│ │  Commit      │ │
│ └──────────────┘ │    │ └──────────────┘ │    │ └──────────────┘ │    │ └──────────────┘ │
│                  │    │                  │    │                  │    │                  │
│ ┌──────────────┐ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │    │ ┌──────────────┐ │
│ │Token Threshold│ │    │ │Retry Logic   │ │    │ │Create        │ │    │ │Task          │ │
│ │  Priority 4  │ │───>│ │& Timeouts    │ │───>│ │ Checkpoint   │ │───>│ │ Scheduler    │ │
│ └──────────────┘ │    │ └──────────────┘ │    │ └──────────────┘ │    │ └──────────────┘ │
└──────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘

                    ↓                                                              ↑
              ┌─────────────┐                                               ┌─────────────┐
              │Budget Manager│                                              │   User      │
              │  5K tokens   │                                              │  (Zero      │
              │  per session │                                              │  Friction)  │
              └─────────────┘                                               └─────────────┘
```

#### Color Coding

**Layer 1 (Detection):** Blue (#4A90E2)
- Represents intelligence, analysis, pattern recognition

**Layer 2 (Memory):** Green (#7ED321)
- Represents persistence, storage, reliability

**Layer 3 (Recovery):** Orange (#F5A623)
- Represents restoration, resumption, continuation

**Layer 4 (Automation):** Purple (#BD10E0)
- Represents automation, integration, orchestration

**Connections:** Gray (#9B9B9B)
- Arrows showing data flow between layers

**Text:** Dark Gray (#4A4A4A) on light backgrounds

#### Annotations

- **Top Right:** "214 Tests | 93% Coverage | <1ms Performance"
- **Bottom Left:** "Modular • Extensible • Production-Ready"
- **Each Layer Header:** Icon + Layer name + Brief description

#### Visual Style

- **Boxes:** Rounded corners (8px radius)
- **Shadows:** Subtle drop shadow (2px offset, 10% opacity)
- **Typography:** Sans-serif (Inter, Roboto, or system default)
- **Icons:** Simple, line-style icons for each component

---

## 2. Detector Flow Diagram

### Purpose
Show how priority-based orchestration works. Demonstrates systems thinking.

### Specifications

**Dimensions:** 800x1000px (vertical flow)
**Format:** PNG/SVG

#### Layout (Top-to-Bottom)

```
                         ┌──────────────────┐
                         │  User Prompt     │
                         │  + Context       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ Trigger Engine   │
                         │  Orchestrator    │
                         └────────┬─────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                │                │
                 ▼                ▼                ▼
         Priority Order      Evaluate         Budget Check
         (Lowest First)      Enabled Only    (5K session limit)
                 │                │                │
                 └────────────────┼────────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  Detector Priority Queue │
                    └─────────────┬───────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐         ┌───────────────┐       ┌───────────────┐
│   Priority 1  │         │   Priority 2  │       │   Priority 3  │
│Project Switch │         │   Keyword     │       │Entity Mention │
│               │         │               │       │               │
│ evaluate()    │         │ evaluate()    │       │ evaluate()    │
│               │         │               │       │               │
│ Returns:      │         │ Returns:      │       │ Returns:      │
│ TriggerResult │         │ TriggerResult │       │ TriggerResult │
│ or None       │         │ or None       │       │ or None       │
└───────┬───────┘         └───────┬───────┘       └───────┬───────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ First Triggered  │
                         │    Detector      │
                         └────────┬─────────┘
                                  │
                         ┌────────┴────────┐
                         │   Triggered?    │
                         └────────┬────────┘
                            Yes   │   No
                         ┌────────┴────────┐
                         ▼                 ▼
                 ┌──────────────┐   ┌──────────────┐
                 │Execute Memory│   │Return None   │
                 │    Query     │   │(No action)   │
                 └──────┬───────┘   └──────────────┘
                        │
                        ▼
                 ┌──────────────┐
                 │Update Budget │
                 │Update State  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │Return Context│
                 │  to User     │
                 └──────────────┘
```

#### Visual Elements

- **Decision Diamonds:** Yellow (#FFD700)
- **Process Boxes:** Light Blue (#E3F2FD)
- **Action Boxes:** Light Green (#E8F5E9)
- **Arrows:** Solid black with labels
- **Priority Badges:** Numbered circles (1, 2, 3, 4)

---

## 3. Before/After Workflow Comparison

### Purpose
Show UX improvement. Emotional impact visualization.

### Specifications

**Dimensions:** 1200x600px (2:1 horizontal split)
**Format:** PNG

#### Layout (Side-by-Side)

```
┌────────────────────────────────────┬────────────────────────────────────┐
│          BEFORE (Manual)           │       AFTER (Automated)            │
├────────────────────────────────────┼────────────────────────────────────┤
│                                    │                                    │
│  ⏱️ Session Ends                   │  ✅ Session Ends                   │
│  ❌ Context lost                   │  ✓ Auto-checkpoint (SessionEnd)    │
│  😞 No memory of decisions         │  ✓ Decisions preserved             │
│                                    │                                    │
│  ⏱️ New Session Starts             │  ✅ New Session Starts             │
│  ❌ Manual reconstruction          │  ✓ Auto-resume (SessionStart)      │
│  ⏱️ 15-30 min explaining context   │  ✓ Context loaded instantly        │
│                                    │                                    │
│  ⏱️ Working on Feature             │  ✅ Working on Feature             │
│  ❌ "What was our decision?"       │  ✓ Keyword trigger: instant recall │
│  ⏱️ Search old chats/docs          │  ✓ Memory graph query              │
│  😞 Maybe find it, maybe not       │  ✓ Reliable context                │
│                                    │                                    │
│  ⏱️ Context Window Fills           │  ✅ Context Window Fills           │
│  ❌ Panic! Lose everything?        │  ✓ Token threshold → auto-query    │
│  ⏱️ Manual save, hope for best     │  ✓ Proactive memory preservation   │
│                                    │                                    │
│  TIME WASTED: 2-5 hours/week       │  TIME SAVED: 2-5 hours/week        │
│  RELIABILITY: 40-60%               │  RELIABILITY: 95%+                 │
│  USER EFFORT: High                 │  USER EFFORT: Zero                 │
│                                    │                                    │
└────────────────────────────────────┴────────────────────────────────────┘
```

#### Visual Style

**Before Column:**
- Background: Light red tint (#FFF5F5)
- Icons: Red X marks, sad faces, clock symbols
- Text: "Manual", "Lost", "Wasted"

**After Column:**
- Background: Light green tint (#F5FFF5)
- Icons: Green checkmarks, happy faces, lightning bolts
- Text: "Automated", "Preserved", "Saved"

**Divider:** Vertical line with arrow pointing right
- Label: "Transformation"

---

## 4. Session Lifecycle Visualization

### Purpose
Show how automation hooks integrate. Technical but accessible.

### Specifications

**Dimensions:** 1000x400px (horizontal timeline)
**Format:** PNG/SVG

#### Layout (Timeline)

```
SESSION LIFECYCLE - Fully Automated

Session Start          During Work           Context Warning        Session End
     │                      │                      │                     │
     ▼                      ▼                      ▼                     ▼
┌─────────┐          ┌─────────┐           ┌─────────┐          ┌─────────┐
│SessionStart        │ Work     │           │ 100K    │          │SessionEnd
│  Hook    │         │ Continues│           │ Tokens  │          │  Hook   │
└────┬────┘          └─────────┘           └────┬────┘          └────┬────┘
     │                                           │                     │
     ▼                                           ▼                     ▼
┌─────────────┐                         ┌─────────────┐       ┌─────────────┐
│Load Previous│                         │Token Detector       │Create       │
│   Session   │                         │  Triggers   │       │ Checkpoint  │
└─────────────┘                         └─────────────┘       └─────────────┘
     │                                           │                     │
     ▼                                           ▼                     ▼
┌─────────────┐                         ┌─────────────┐       ┌─────────────┐
│Show Resume  │                         │Query Memory │       │Update       │
│   Points    │                         │   Graph     │       │ CLAUDE.md   │
└─────────────┘                         └─────────────┘       └─────────────┘
     │                                           │                     │
     ▼                                           ▼                     ▼
  User sees                               Context loaded          Session saved
  last session                            proactively             automatically


                    Git Commit Trigger (Any Time)
                            │
                            ▼
                    ┌─────────────┐
                    │post-commit  │
                    │    Hook     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │Auto-checkpoint
                    │   Created   │
                    └─────────────┘
```

#### Visual Elements

- **Timeline:** Horizontal line with milestones
- **Hooks:** Purple boxes (automation triggers)
- **Actions:** Blue boxes (system actions)
- **Outcomes:** Green boxes (user benefits)
- **Arrows:** Show causality

---

## 5. Skills Matrix Infographic

### Purpose
Show competencies demonstrated by project. For portfolio page.

### Specifications

**Dimensions:** 800x1000px (vertical)
**Format:** PNG

#### Layout (Grid)

```
╔════════════════════════════════════════════════════════════╗
║          SKILLS DEMONSTRATED BY THIS PROJECT               ║
╚════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────┐
│                 STRATEGIC PRODUCT                         │
├──────────────────────────────────────────────────────────┤
│ ✓ Problem Identification      [████████░░] 85%           │
│ ✓ Market Analysis              [███████░░░] 75%           │
│ ✓ User Journey Mapping         [████████░░] 80%           │
│ ✓ Prioritization               [████████░░] 85%           │
│ ✓ Metrics Definition           [███████░░░] 70%           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                 SYSTEMS THINKING                          │
├──────────────────────────────────────────────────────────┤
│ ✓ Architecture Design          [█████████░] 90%           │
│ ✓ Modularity                   [█████████░] 90%           │
│ ✓ Scalability Patterns         [████████░░] 80%           │
│ ✓ Resilience Engineering       [████████░░] 85%           │
│ ✓ Observability                [███████░░░] 75%           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                    UX DESIGN                              │
├──────────────────────────────────────────────────────────┤
│ ✓ User-Centered Design         [█████████░] 95%           │
│ ✓ Friction Analysis            [█████████░] 90%           │
│ ✓ Progressive Enhancement      [████████░░] 85%           │
│ ✓ Mental Models                [████████░░] 80%           │
│ ✓ Invisible Design             [████████░░] 85%           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│               TECHNICAL EXECUTION                         │
├──────────────────────────────────────────────────────────┤
│ ✓ Production Standards         [█████████░] 93%           │
│ ✓ Testing Strategy             [█████████░] 93%           │
│ ✓ Performance Optimization     [████████░░] 85%           │
│ ✓ Error Handling               [████████░░] 80%           │
│ ✓ Code Organization            [████████░░] 85%           │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│              AI-FIRST DEVELOPMENT                         │
├──────────────────────────────────────────────────────────┤
│ ✓ AI Augmentation              [█████████░] 90%           │
│ ✓ Hybrid AI Design             [████████░░] 85%           │
│ ✓ Prompt Engineering           [███████░░░] 75%           │
│ ✓ Context Management           [████████░░] 80%           │
│ ✓ AI UX Patterns               [████████░░] 85%           │
└──────────────────────────────────────────────────────────┘
```

#### Color Scheme

- **Bars:** Gradient from blue to green (low to high)
- **Checkmarks:** Green (#7ED321)
- **Section Headers:** Dark blue (#4A90E2)
- **Background:** White with subtle grid pattern

---

## 6. Key Metrics Dashboard

### Purpose
Quick-glance project stats. For portfolio hero section.

### Specifications

**Dimensions:** 1200x300px (horizontal)
**Format:** PNG with transparent background

#### Layout (Four Metrics)

```
┌─────────────────────────────────────────────────────────────────┐
│                   PROJECT METRICS                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│    TESTS    │  COVERAGE   │   MODULES   │ PERFORMANCE │  FRICTION   │
│             │             │             │             │             │
│     214     │     93%     │      4      │    <1ms     │     0%      │
│             │             │             │             │             │
│ Comprehensive│ Exceeds    │ Detector    │ Real-Time   │ Zero User   │
│    Suite    │ Industry   │  Systems    │  Triggers   │   Effort    │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

#### Visual Style

- **Large Numbers:** 48pt bold
- **Labels:** 14pt regular, all caps
- **Descriptions:** 12pt light
- **Dividers:** Thin vertical lines
- **Background:** Subtle gradient (white to light gray)

---

## 7. Technology Stack Visualization

### Purpose
Show technical breadth. For technical interviews.

### Specifications

**Dimensions:** 600x800px (vertical)
**Format:** PNG/SVG

#### Layout (Layered Stack)

```
┌──────────────────────────────────┐
│      TECHNOLOGY STACK            │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│         TESTING                  │
│  pytest • coverage • mocking     │
│  fixtures • integration tests    │
└──────────────────────────────────┘
              ▲
              │
┌──────────────────────────────────┐
│      CORE APPLICATION            │
│  Python 3.14 • Modular Design    │
│  State Management • Caching      │
└──────────────────────────────────┘
              ▲
              │
┌──────────────────────────────────┐
│       INTEGRATION                │
│  MCP Client • Git Hooks          │
│  Task Scheduler • Logging        │
└──────────────────────────────────┘
              ▲
              │
┌──────────────────────────────────┐
│      INFRASTRUCTURE              │
│  SQLite • JSON • File System     │
│  Cross-Platform (Win + Unix)     │
└──────────────────────────────────┘
```

---

## 8. Social Media Graphics

### LinkedIn Post Image

**Dimensions:** 1200x627px (OpenGraph standard)
**Format:** PNG

#### Content

```
┌────────────────────────────────────────────────┐
│                                                │
│    Context-Aware Memory Management             │
│                                                │
│    Production AI Memory System                 │
│                                                │
│    214 Tests  •  93% Coverage  •  18K LOC      │
│                                                │
│    Solving AI's Biggest UX Problem:            │
│           Context Persistence                  │
│                                                │
│    [Simplified architecture icon/diagram]      │
│                                                │
│    First Coding Project                        │
│    Proof of Strategic Thinking at Scale        │
│                                                │
└────────────────────────────────────────────────┘
```

### Twitter Card Image

**Dimensions:** 1200x675px (Twitter summary_large_image)
**Format:** PNG

Similar to LinkedIn but with larger text, simplified content

---

## 9. GitHub Social Preview

**Dimensions:** 1280x640px (GitHub requirement)
**Format:** PNG

#### Content

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│         Context-Aware Memory Management System             │
│                                                            │
│              Production-Ready AI Memory                    │
│                                                            │
│     ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│     │ Detection│─>│  Memory  │─>│ Recovery │             │
│     └──────────┘  └──────────┘  └──────────┘             │
│                                                            │
│   214 Tests  •  93% Coverage  •  Zero-Friction UX          │
│                                                            │
│   Hybrid AI + Traditional Tools  •  Production-Ready       │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Color Palette Reference

### Primary Colors

```
Blue (Intelligence):     #4A90E2
Green (Persistence):     #7ED321
Orange (Recovery):       #F5A623
Purple (Automation):     #BD10E0
```

### Secondary Colors

```
Dark Text:              #4A4A4A
Light Text:             #9B9B9B
Background Light:       #F9F9F9
Background Dark:        #2C3E50
```

### Semantic Colors

```
Success:                #7ED321
Warning:                #F5A623
Error:                  #D0021B
Info:                   #4A90E2
```

### Gradient Backgrounds

```
Light Gradient:         #FFFFFF → #F5F5F5
Dark Gradient:          #2C3E50 → #34495E
Blue Gradient:          #4A90E2 → #357ABD
```

---

## Typography Guidelines

### Fonts

**Primary:** Inter (body text, UI)
**Secondary:** Roboto Mono (code, technical)
**Headings:** Inter Bold or Montserrat

### Sizes

```
Hero Heading:           48pt
Section Heading:        32pt
Subsection:             24pt
Body:                   16pt
Caption:                12pt
Code:                   14pt (monospace)
```

### Weights

```
Light:                  300
Regular:                400
Medium:                 500
Bold:                   700
```

---

## Icon Set Recommendations

### Suggested Sources

1. **Heroicons** (heroicons.com) - Clean, modern, MIT license
2. **Feather Icons** (feathericons.com) - Minimal, consistent
3. **Material Icons** (material.io/icons) - Comprehensive, recognizable
4. **Font Awesome** (fontawesome.com) - Industry standard

### Key Icons Needed

- **Detection:** 🔍 Magnifying glass, 🎯 Target
- **Memory:** 💾 Database, 🧠 Brain, 📦 Archive
- **Recovery:** 🔄 Refresh, ⚡ Lightning, 📤 Upload
- **Automation:** ⚙️ Gear, 🤖 Robot, 🔗 Chain
- **Testing:** ✅ Checkmark, 🧪 Test tube
- **Performance:** ⚡ Lightning bolt, 📊 Chart

---

## Design Tool Templates

### Excalidraw Template (Recommended for Quick Diagrams)

**File:** `architecture-diagram-template.excalidraw`

**Contents:**
- Pre-configured 4 layers with color coding
- Arrow connectors
- Text boxes for annotations
- Icon placeholders
- Export at 2x resolution for clarity

### Figma Template (Recommended for Polished Graphics)

**File:** `portfolio-visuals-template.fig`

**Frames:**
1. System Architecture (1200x800)
2. Before/After Comparison (1200x600)
3. Detector Flow (800x1000)
4. Skills Matrix (800x1000)
5. Metrics Dashboard (1200x300)
6. Social Media (various sizes)

**Shared Components:**
- Color palette
- Typography styles
- Icon library
- Button styles
- Card templates

---

## Accessibility Requirements

### Color Contrast

**WCAG AA Standard:**
- Text contrast ratio: 4.5:1 minimum
- Large text (18pt+): 3:1 minimum
- Interactive elements: 3:1 minimum

**Testing:** Use WebAIM Contrast Checker

### Alternative Text

**For all diagrams, provide:**
- Descriptive alt text (100-150 characters)
- Long description in caption or adjacent text
- Transcript for complex diagrams

**Example Alt Text:**
```
"Four-layer system architecture showing detection, memory, recovery,
and automation layers with arrows indicating data flow between components."
```

### Screen Reader Considerations

- Use semantic HTML when diagrams are embedded in web pages
- Provide text-based alternatives (tables, lists)
- Ensure tab order is logical

---

## Export Settings

### For Web (Portfolio, GitHub)

**PNG:**
- Resolution: 2x (retina)
- Compression: Medium (80-90 quality)
- Max file size: 500KB per image

**SVG:**
- Optimize: Run through SVGO
- Remove metadata
- Minify paths
- Embed fonts if custom typography

### For Print (Case Study PDF)

**PNG:**
- Resolution: 300 DPI
- Color space: RGB (for digital) or CMYK (for physical print)
- Format: PNG or PDF

### For Social Media

**Optimized Sizes:**
- LinkedIn: 1200x627px, <5MB
- Twitter: 1200x675px, <5MB
- GitHub: 1280x640px, PNG
- Open Graph: 1200x630px, <8MB

---

## Quick Creation Checklist

### Phase 1: Essential Diagrams (2 hours)

- [ ] System Architecture (4-layer) - PRIMARY
- [ ] Key Metrics Dashboard
- [ ] GitHub social preview image

### Phase 2: Supporting Visuals (2 hours)

- [ ] Before/After workflow comparison
- [ ] Detector flow diagram
- [ ] Session lifecycle visualization

### Phase 3: Portfolio Graphics (2 hours)

- [ ] Skills matrix infographic
- [ ] Technology stack visualization
- [ ] LinkedIn/Twitter social cards

### Phase 4: Polish (1 hour)

- [ ] Export all formats (PNG, SVG)
- [ ] Optimize file sizes
- [ ] Test accessibility (contrast, alt text)
- [ ] Upload to repository

---

## Tools Quick Start

### Excalidraw (Free, Browser-Based)

1. Go to excalidraw.com
2. Use library: "Architecture Diagrams"
3. Export as PNG (2x) or SVG
4. Embed in README: `![Architecture](./docs/images/architecture.png)`

### draw.io (Free, Desktop or Web)

1. Download from diagrams.net
2. Use template: "Cloud Architecture"
3. Customize colors per spec above
4. Export as PNG/SVG

### Canva (Free Tier Sufficient)

1. Create account at canva.com
2. Use custom dimensions from specs
3. Use templates: "Infographic", "Process Diagram"
4. Export as PNG (Pro tier for SVG)

### Figma (Free Tier Sufficient)

1. Create account at figma.com
2. Import color palette and typography
3. Use components for consistency
4. Export at 2x resolution

---

## Sample Workflow

### Creating System Architecture Diagram (30 minutes)

1. **Setup (5 min)**
   - Open Excalidraw
   - Set canvas to 1200x800
   - Import color palette

2. **Structure (10 min)**
   - Draw 4 main boxes (layers)
   - Add sub-boxes (4 detectors, MCP, hooks)
   - Create arrow connectors

3. **Content (10 min)**
   - Label all boxes
   - Add priority numbers
   - Include key annotations

4. **Polish (5 min)**
   - Adjust spacing and alignment
   - Add subtle shadows
   - Apply color scheme

5. **Export**
   - PNG at 2x (2400x1600)
   - Downscale to 1200x800
   - Optimize with TinyPNG

---

**These specifications provide everything needed to create professional portfolio visuals. Start with Phase 1 essentials, then expand as time allows.**

**Tools are flexible—choose what you're comfortable with. Consistency matters more than tool choice.**
