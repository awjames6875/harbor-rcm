# Harbor RCM

> AI-powered insurance verification for small medical practices and behavioral health agencies.

Built using Jake Van Clief's 3-Layer Folder Architecture for token efficiency and context isolation.

---

## Project Structure

```
harbor-rcm/
├── CLAUDE.md                    ← Layer 1: The Floor Plan / Router
├── PROJECT_KNOWLEDGE.md         ← Master context for Claude.ai Projects
├── README.md                    ← You are here
├── docs/
│   └── PRD.md                   ← Full Product Requirements Document
│
├── 1_intake/                    ← Layer 2: Room 1
│   ├── CONTEXT.md               ← Specific rules for this room
│   ├── skills/                  ← Layer 3: Skills loaded only here
│   ├── code/                    ← Layer 3: Code for this room
│   └── tests/
│
├── 2_verification/              ← Layer 2: Room 2
│   ├── CONTEXT.md
│   ├── skills/
│   ├── code/
│   └── tests/
│
├── 3_normalization/             ← Layer 2: Room 3
│   ├── CONTEXT.md
│   ├── skills/
│   ├── code/
│   └── tests/
│
└── 4_delivery/                  ← Layer 2: Room 4
    ├── CONTEXT.md
    ├── skills/
    ├── code/
    └── tests/
```

---

## How To Use With Claude Code

1. Open this folder in VS Code
2. Run `claude` from the terminal (Claude Code reads CLAUDE.md automatically)
3. Ask Claude to do something like "fix the verification bug"
4. Claude reads the routing table in CLAUDE.md
5. Claude opens ONLY `2_verification/CONTEXT.md`
6. Claude does the work without burning tokens on irrelevant files

**Token comparison:**
- Without this architecture: ~30,000 tokens per command
- With this architecture: ~5,000 tokens per command
- **Result: 6x faster, 6x cheaper**

---

## How To Use With Claude.ai Projects

1. Go to claude.ai → Projects → Create new
2. Name it "Harbor RCM"
3. Upload `PROJECT_KNOWLEDGE.md` to the Project knowledge
4. Now every conversation in that Project starts with full context

Use Claude.ai Projects for **strategy** (pricing, sales, planning).
Use Claude Code for **building** (writing code, fixing bugs).

---

## Current Status

**Phase 1:** Land first customer
- ✅ Architecture set up
- ⏳ Skyvern Cloud signup
- ⏳ Availity Developer signup
- ⏳ Demo at doctor friend's office (Mother's Day weekend)
- ⏳ Close first deal at $2,500 + $500/mo

---

## License

Private. © Adam James / GrowthGenix AI 2026.
