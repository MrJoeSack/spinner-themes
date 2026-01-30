# Claude Code Spinner Themes

Custom spinner verb collections for [Claude Code](https://claude.ai/claude-code).

## Available Themes

| Theme | Vibe | File |
|-------|------|------|
| **Passive Aggressive** | "Per my last email" / "Noted" | [passive-aggressive.json](passive-aggressive.json) |
| **Existential Dread** | "The abyss staring back" / "One must imagine Sisyphus happy" | [existential-dread.json](existential-dread.json) |
| **AI Hype** | "AGI was last Tuesday" / "Shoggoth with a smiley face" | [ai-hype.json](ai-hype.json) |
| **Robert Greene** | "Saying less than necessary" / "Letting them hang themselves" | [robert-greene.json](robert-greene.json) |
| **Fran Lebowitz** | "Still not writing the book" / "No one listens" | [fran-lebowitz.json](fran-lebowitz.json) |
| **Silicon Valley** | "Pivoting again" / "Default dead" | [silicon-valley.json](silicon-valley.json) |
| **Tech Bro** | "Cold plunge" / "Few understand" | [tech-bro.json](tech-bro.json) |
| **Product Manager** | "Parking lot that" / "Double-clicking on that" | [product-manager.json](product-manager.json) |
| **RTO Excuses** | "Serendipitous encounters" / "Badge swipes don't lie" | [rto-excuses.json](rto-excuses.json) |
| **Back From Vacation** | "Okay I checked email constantly" / "I forgot my password" | [back-from-vacation.json](back-from-vacation.json) |
| **iPhone User** | "Green bubbles are gross" / "My battery health is 84%" | [iphone-user.json](iphone-user.json) |
| **Android User** | "Actually, Android did that first" / "It's not bloatware, it's features" | [android-user.json](android-user.json) |
| **Marathon Identity** | "Did I mention I ran a marathon?" / "Actually, 26.219" | [marathon-identity.json](marathon-identity.json) |
| **The Shining** | "All work and no play" / "Always been the caretaker" | [the-shining.json](the-shining.json) |
| **Dark Tower** | "The world has moved on" / "Blaine is a pain" | [dark-tower.json](dark-tower.json) |
| **Performative** | "Holding space" / "Protecting my energy" | [performative.json](performative.json) |
| **I, Claudius** | "Letting all the poisons hatch" / "Becoming emperor accidentally" | [i-claudius.json](i-claudius.json) |
| **SQL Server** | "Where are my scripts?" / "Estimating 1 row" | [sql-server.json](sql-server.json) |
| **Layoff Speak** | "Right-sizing the organization" / "Laptop return instructions" | [layoff-speak.json](layoff-speak.json) |

## Installation

Copy the `spinnerVerbs` block from any JSON file into your Claude Code settings:

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

**Mode options:** `"append"` adds to defaults, `"replace"` uses only yours.

## License

MIT
