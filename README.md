# Claude Code Spinner Themes

Custom spinner verb collections for [Claude Code](https://claude.ai/claude-code).

## Available Themes

### Passive Aggressive
For when everything is fine. Really. It's fine.

**File:** `passive-aggressive.json`

### Existential Dread
For when the code compiles but the void remains.

**File:** `existential-dread.json`

### AI Hype
AGI was last Tuesday.

**File:** `ai-hype.json`

### Robert Greene
Concealing intentions. Saying less than necessary.

**File:** `robert-greene.json`

### Fran Lebowitz
The book remains unwritten.

**File:** `fran-lebowitz.json`

### Silicon Valley
Disrupting the industry. Pivoting. Pivoting again.

**File:** `silicon-valley.json`

### Product Manager
Corporate jargon for when you want your AI to speak fluent stakeholder.

**File:** `product-manager.json`

### The Shining
All work and no play.

**File:** `the-shining.json`

### Dark Tower
For those who follow the Beam. Thankee-sai.

**File:** `dark-tower.json`

### Marathon Identity
Did I mention I ran a marathon?

**File:** `marathon-identity.json`

### Performative
For when you're doing the work and holding space.

**File:** `performative.json`

### I, Claudius
Roman imperial intrigue inspired by Robert Graves. For when your merge conflicts feel like succession politics.

**File:** `i-claudius.json`

### SQL Server
For DBAs. Technical operations mixed with the questions we actually ask.

**File:** `sql-server.json`

### Layoff Speak
Your role has been eliminated. This is not a reflection of your work.

**File:** `layoff-speak.json`

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
