# Himalaya CLI Command Reference

## Global Options

All commands support these options:

| Option | Description |
|--------|-------------|
| `-a, --account <NAME>` | Override default account |
| `-c, --config <PATH>` | Override config file path |
| `-o, --output <FORMAT>` | Output format: `plain` (default) or `json` |
| `--debug` | Enable debug logs |
| `--trace` | Enable verbose logs with backtrace |

## Commands

### envelope list

Search and list emails.

```bash
himalaya envelope list [OPTIONS] [QUERY]...
```

**Options:**
- `-f, --folder <NAME>` - Folder to search (default: `INBOX`)
- `-p, --page <NUMBER>` - Page number (default: 1)
- `-s, --page-size <NUMBER>` - Results per page
- `-w, --max-width <PIXELS>` - Max table width

**Query Syntax:**

Filter operators:
- `not <condition>` - Negate condition
- `<condition> and <condition>` - Both must match
- `<condition> or <condition>` - Either must match

Filter conditions:
- `date <yyyy-mm-dd>` - Exact date match
- `before <yyyy-mm-dd>` - Before date (NOTE: unreliable with Gmail IMAP)
- `after <yyyy-mm-dd>` - After date (NOTE: unreliable with Gmail IMAP)
- `from <pattern>` - Sender matches pattern
- `to <pattern>` - Recipient matches pattern
- `subject <pattern>` - Subject matches pattern
- `body <pattern>` - Body matches pattern
- `flag <flag>` - Has flag (seen, answered, flagged, deleted, draft)

Sort syntax:
- `order by date [asc|desc]`
- `order by from [asc|desc]`
- `order by to [asc|desc]`
- `order by subject [asc|desc]`

**Examples:**
```bash
# List inbox
himalaya envelope list

# Search All Mail for sender
himalaya envelope list -f "[Gmail]/All Mail" from "@amazon.com"

# Combine conditions
himalaya envelope list -f "[Gmail]/All Mail" from "@amazon.com" and subject "order"

# JSON output with 500 results
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "@spam.com"

# Sort by date descending
himalaya envelope list order by date desc
```

---

### message read

Read email content.

```bash
himalaya message read [OPTIONS] <ID>...
```

**Options:**
- `-f, --folder <NAME>` - Folder containing message (default: `INBOX`)
- `-p, --preview` - Don't mark as "seen"
- `--no-headers` - Show only body
- `-H, --header <NAME>` - Specific headers to show

**Examples:**
```bash
# Read single message
himalaya message read 12345

# Read from All Mail
himalaya message read -f "[Gmail]/All Mail" 12345

# Read as JSON
himalaya -o json message read -f "[Gmail]/All Mail" 12345

# Preview without marking seen
himalaya message read -p 12345
```

---

### message move

Move emails to another folder. **Accepts multiple IDs for batch operations.**

```bash
himalaya message move [OPTIONS] <TARGET> <ID>...
```

**Arguments:**
- `<TARGET>` - Destination folder name
- `<ID>...` - One or more envelope IDs

**Options:**
- `-f, --folder <SOURCE>` - Source folder (default: `INBOX`)

**Examples:**
```bash
# Move single message to trash
himalaya message move -f "[Gmail]/All Mail" "[Gmail]/Trash" 12345

# Batch move multiple messages (FAST)
himalaya message move -f "[Gmail]/All Mail" "[Gmail]/Trash" 12345 12346 12347

# Move to custom label
himalaya message move -f "INBOX" "Work/Projects" 12345
```

---

### message delete

Move to trash (or add deleted flag if already in trash).

```bash
himalaya message delete [OPTIONS] <ID>...
```

**Options:**
- `-f, --folder <NAME>` - Source folder (default: `INBOX`)

**Note:** This moves to trash, doesn't permanently delete. Use `folder expunge` to permanently delete.

**Examples:**
```bash
# Delete from inbox
himalaya message delete 12345

# Delete from All Mail (moves to trash)
himalaya message delete -f "[Gmail]/All Mail" 12345 12346
```

---

### message copy

Copy emails to another folder.

```bash
himalaya message copy [OPTIONS] <TARGET> <ID>...
```

**Arguments:**
- `<TARGET>` - Destination folder
- `<ID>...` - One or more envelope IDs

**Options:**
- `-f, --folder <SOURCE>` - Source folder (default: `INBOX`)

---

### folder list

List all folders/labels.

```bash
himalaya folder list
```

**Example output for Gmail:**
```
| NAME                    | DESC                 |
|-------------------------|----------------------|
| INBOX                   | \HasNoChildren       |
| [Gmail]/All Mail        | \All, \HasNoChildren |
| [Gmail]/Drafts          | \Drafts              |
| [Gmail]/Sent Mail       | \Sent                |
| [Gmail]/Spam            | \Junk                |
| [Gmail]/Trash           | \Trash               |
| Work                    | \HasNoChildren       |
| Work/Projects           | \HasNoChildren       |
```

---

### folder expunge

Permanently delete messages marked as deleted.

```bash
himalaya folder expunge [OPTIONS] [NAME]
```

**Arguments:**
- `[NAME]` - Folder to expunge (default: `INBOX`)

---

### flag add/set/remove

Manage email flags.

```bash
himalaya flag add [OPTIONS] <ID> <FLAGS>...
himalaya flag set [OPTIONS] <ID> <FLAGS>...
himalaya flag remove [OPTIONS] <ID> <FLAGS>...
```

**Standard flags:** `seen`, `answered`, `flagged`, `deleted`, `draft`

**Examples:**
```bash
# Mark as read
himalaya flag add 12345 seen

# Mark as starred
himalaya flag add 12345 flagged

# Remove seen flag
himalaya flag remove 12345 seen
```

---

### account list

List configured accounts.

```bash
himalaya account list
```

---

### account configure

Interactive account setup wizard.

```bash
himalaya account configure <ACCOUNT>
```

**Example:**
```bash
himalaya account configure gmail-work
```

---

## Scripting Patterns

### Get all IDs from a sender as space-separated list

```bash
ids=$(himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "@spam.com" | jq -r '.[].id' | tr '\n' ' ')
```

### Batch delete with single command

```bash
himalaya message move -f "[Gmail]/All Mail" "[Gmail]/Trash" $ids
```

### Filter by date client-side (workaround for Gmail)

```bash
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "@example.com" | \
  jq --arg date "2025-01-01" '[.[] | select(.date[:10] < $date)]'
```

### Count emails from sender

```bash
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "@example.com" | jq 'length'
```

### Export email to markdown with frontmatter

```bash
himalaya -o json message read -f "[Gmail]/All Mail" 12345 | \
  jq -r '"---\nfrom: \(.from)\nsubject: \(.subject)\ndate: \(.date)\n---\n\n\(.body)"'
```
