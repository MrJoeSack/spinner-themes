# Lessons Learned

## Commit Messages
- Keep them **under 3 words**: "Update", "Add files", "Fix typo"
- Never expose implementation details in public repo history
- Had to rewrite 3 commits because messages were too verbose

## GitHub SVG Limitations
- GitHub **strips CSS animations** from SVGs for security
- Animated demos must use GIF format instead
- SVGs render but won't animate

## Claude Code Spinner Accuracy
When recreating the Claude Code spinner:
- **Characters**: Braille spinner `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏` (not ASCII like ◐◓◑◒)
- **Color**: Orange #ff8700 (ANSI 208), not generic orange
- **Timing**: 100ms per spinner frame rotation
- **Effect**: Shimmer/brightness pulse, not color change to red
- Source: [Reverse Engineering Claude's ASCII Spinner Animation](https://medium.com/@kyletmartinez/reverse-engineering-claudes-ascii-spinner-animation-eec2804626e0)

## Spinner Verbs Must Be Verbs
- All spinner messages should be action verbs (-ing forms)
- Wrong: "I am the one who knocks", "Say my name"
- Right: "Being the one who knocks", "Saying my name"
- Hyphenate phrases when verbing: "Per-my-last-emailing", "Here's-Johnnying"

## Thumbnail Guidelines
- **Avoid faces** - regenerated passive-aggressive, better-call-saul, curb-your-enthusiasm
- Use sketch style with diagonal hatching, not solid fills
- Not too literal - use visual metaphors
- Not too clean/vector-like - should look hand-drawn
