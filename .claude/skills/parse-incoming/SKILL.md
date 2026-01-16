---
description: Process incoming files from LocalSend. Use when user runs /parse-incoming or asks to organize received files.
---

# Parse Incoming Files

Process files received via LocalSend and organize them interactively.

**Incoming folder:** `/home/neo/agents/sys-admin/incoming/`
**Archive folder:** `/home/neo/agents/sys-admin/archive/`

## Workflow

1. **List incoming files** - Show all files in the incoming folder with details (name, size, date, type)

2. **For each file, ask the user:**
   - Preview the file if possible (show image, read PDF/text first page, etc.)
   - Ask where it should go (provide suggestions based on file type)
   - Options: move to specific folder, archive, or delete

3. **Execute the action:**
   - Copy file to destination
   - Move original to archive (default) or delete if user confirms

4. **Report summary** - Show what was processed and where files went

## Common Destinations

Based on this repo's structure, suggest:

| File Type | Suggested Destination |
|-----------|----------------------|
| System configs | `config/<subsystem>/` |
| Documentation | `docs/` |
| Package lists | `data/packages/` |
| Screenshots | `docs/screenshots/` or archive |
| PDFs | Ask user - could be docs, reference, etc. |

## Commands

```bash
# List incoming files
ls -la /home/neo/agents/sys-admin/incoming/

# Move to destination
mv /home/neo/agents/sys-admin/incoming/<file> <destination>

# Archive (preserve original name with timestamp)
mv /home/neo/agents/sys-admin/incoming/<file> /home/neo/agents/sys-admin/archive/

# Delete
rm /home/neo/agents/sys-admin/incoming/<file>
```

## Interactive Flow

Use the AskUserQuestion tool to present options for each file. Example:

- Header: "screenshot.png"
- Options: ["Archive (keep for reference)", "docs/screenshots/", "Delete", "Other location"]

Let the user decide per-file, then execute all actions at the end.
