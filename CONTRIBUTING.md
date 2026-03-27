# Git Conventions

## Commit Message Format

```
<type>(<scope>): <summary>

<body — optional, explains WHY>
```

### Types

| Type | Use for |
|------|---------|
| `feat` | new capability or behaviour |
| `fix` | bug fix |
| `refactor` | restructuring without behaviour change |
| `perf` | performance improvement |
| `docs` | documentation only |
| `chore` | maintenance, deps, config |
| `test` | adding or fixing tests |

### Scopes (optional)

`detector` · `filter` · `logger` · `classifier` · `visualizer`

### Examples

```
feat(detector): select Hough line closest to 90deg for stable angle
fix(filter): clear deque on zero detections to prevent stale output
perf(detector): reduce ROI expansion to cut per-frame processing time
docs: add RPi5 camera setup instructions to README
chore: pin opencv-python version in requirements-rpi.txt
```

### Rules

- Summary under 72 characters, imperative mood — "add" not "added"
- One logical change per commit — one fix, one feature, one file if possible
- Body explains **why**, not what (the diff already shows what)
- Blank line between summary and body

---

## Branching Strategy

```
main          stable, tested code only — never commit broken state here
feature/      new capabilities     e.g. feature/multi-object-tracking
fix/          bug fixes            e.g. fix/false-positive-tuning
experiment/   throwaway work       never merge directly into main
```

### Workflow

1. Branch off `main` → `feature/<name>` or `fix/<name>`
2. Make atomic commits on the branch
3. Merge into `main` only when the branch works end-to-end
4. Delete the branch after merging

---

## Atomic Commits

Each commit should do exactly one thing and leave the repo in a working state.

**Good:**
```
fix(filter): clear deque on zero detections
feat(logger): add object_count column to CSV output
```

**Bad:**
```
various fixes and updates
WIP
```
