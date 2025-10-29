# Commit Message Guidelines

Well-written commit messages help your future self and teammates understand the "why" behind changes.

## Structure

Each commit message should include:

1. A short summary with issue number (max 72 chars)
2. An optional longer description
3. Structured footers for related metadata

## Examples

```
feat [#42]: add adaptive layout for profile screen

The new layout adjusts to screen size and respects accessibility settings.
```

```
fix [#88]: prevent crash on nil URL in share sheet

Handles a rare edge case when a user tries to share before the URL loads.
```

## Conventions

- Use [Conventional Commits](mdc:https:/www.conventionalcommits.org) (e.g., `feat:`, `fix:`, `chore:`).
- **Include issue number in title**: Extract from branch name and format as `[#123]`
- Use present tense ("add" not "added").
- Capitalize the summary, no period at the end.
- Write descriptive bodies if the "why" isn't obvious.
- Commit small and often.
- **Do not include co-author information** or AI attribution in commit messages.
- **Never add AI attribution** such as "Generated with Claude Code" or "Co-Authored-By: Claude".

## Issue Number Extraction

Extract issue number from branch name using these common patterns:
- `feat/123-description` → `[#123]`
- `fix/456-bug-description` → `[#456]`
- `chore/789-cleanup` → `[#789]`

### Title Format
```
type [#issue]: brief description
```

## Recommended Tags

| Type     | When to use it                             |
| -------- | ------------------------------------------ |
| feat     | New feature                                |
| fix      | Bug fix                                    |
| chore    | Non-functional (e.g. cleanup)              |
| refactor | Code restructuring without behavior change |
| docs     | Documentation-only changes                 |
| test     | Adding or fixing tests                     |
