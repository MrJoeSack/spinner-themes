# Claude Code Spinner Themes

Custom spinner verb collections for [Claude Code](https://claude.ai/claude-code).

## Available Themes

### Passive Aggressive
For when everything is fine. Really. It's fine.

**File:** `passive-aggressive.json`

### Product Manager
Corporate jargon for when you want your AI to speak fluent stakeholder.

**File:** `product-manager.json`

### SQL Server
For DBAs. Technical operations mixed with the questions we actually ask.

**File:** `sql-server.json`

### I, Claudius
Roman imperial intrigue inspired by Robert Graves. For when your merge conflicts feel like succession politics.

**File:** `i-claudius.json`

## Installation

Copy the `spinnerVerbs` configuration into your Claude Code settings:

**Windows:** `%USERPROFILE%\.claude\settings.json`
**macOS/Linux:** `~/.claude/settings.json`

```json
{
  "spinnerVerbs": {
    "mode": "append",
    "verbs": [
      "Your spinner messages here..."
    ]
  }
}
```

Restart Claude Code after editing.

### Mode Options

- `"append"` - Adds your custom verbs to the default set
- `"replace"` - Uses only your custom verbs

## License

MIT
