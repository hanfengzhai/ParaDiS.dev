#!/usr/bin/env bash
# Block git commit shell commands that try to add AI agent co-authors.
set -euo pipefail

input=$(cat)
command=$(printf '%s' "$input" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

if printf '%s' "$command" | grep -Eiq \
  'co-authored-by:.*(cursor|cursoragent|cursor\.com|copilot|openai|chatgpt|gpt-|claude|anthropic|gemini|bard|ai.agent|ai-agent)|--trailer.*co-authored-by.*(cursor|cursoragent|copilot|openai|chatgpt|claude|anthropic|gemini)'; then
  cat <<'EOF'
{
  "permission": "deny",
  "user_message": "Git commits must not include AI agent Co-authored-by trailers (Cursor, cursoragent, Copilot, Claude, etc.).",
  "agent_message": "Do not add Co-authored-by lines for any AI agent. Commit with human authorship only."
}
EOF
  exit 0
fi

printf '%s\n' '{ "permission": "allow" }'
exit 0
