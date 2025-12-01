---
description: Continue troubleshooting from documentation folder
---

You are resuming a troubleshooting session for the **{{arg1}}** subsystem.

**Instructions:**

1. **Read the root tracker first:**
   - Read `/home/neo/agents/sys-admin/TROUBLESHOOTING.md`
   - Find the status of issues in the `{{arg1}}` section
   - Understand what's active, resolved, or pending

2. **Read all files in the specific folder:**
   - Read ALL files in `/home/neo/agents/sys-admin/{{arg1}}/`
   - Understand the full context and troubleshooting history
   - Note what's been tried and what the current state is

3. **Ask for status update:**
   - Ask the user: "What's the current status of the {{arg1}} issue?"
   - Don't assume anything - get fresh information
   - Reference specific files and steps from documentation

4. **Continue troubleshooting:**
   - Based on user's response, continue from where you left off
   - Update TROUBLESHOOTING.md if status changes
   - Create new documentation files as needed with descriptive names
   - When resolved, move issue to "Resolved Issues" section in TROUBLESHOOTING.md

**Important:**
- Always read TROUBLESHOOTING.md first for quick context
- Reference specific file paths (e.g., `audio/tv-audio-troubleshooting.md:23`) when discussing issues
- Update the root tracker when status changes
- Be ready to create new files if new issues discovered

Start by reading the root tracker and the {{arg1}} folder, then ask the user for current status.
