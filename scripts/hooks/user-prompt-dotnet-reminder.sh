#!/usr/bin/env bash
# UserPromptSubmit hook: inject concise XML reminder on every prompt.

set -euo pipefail

MSG=$(cat <<'EOF'
<system-reminder>
<dotnet-artisan-routing>
1. Mandatory first action: invoke [skill:dotnet-advisor].
2. Do not plan, reason, design, or implement until [skill:dotnet-advisor] has been invoked.
3. Follow advisor routing and invoke the relevant downstream skills.
4. Apply standards defined by the routed skills.
</dotnet-artisan-routing>
</system-reminder>
EOF
)

echo "$MSG"


exit 0
