---
name: email-management
description: Manage Gmail accounts using himalaya CLI and Google Workspace MCP. Use for searching, reading, deleting, moving, and organizing emails. Supports bulk operations, spam cleanup, and email export. Use when user asks about emails, inbox management, spam deletion, or email organization.
allowed-tools: Bash, Read, Write, Grep, Glob, mcp__google_workspace__search_gmail_messages, mcp__google_workspace__get_gmail_message_content, mcp__google_workspace__get_gmail_messages_content_batch, mcp__google_workspace__get_gmail_thread_content, mcp__google_workspace__send_gmail_message, mcp__google_workspace__draft_gmail_message, mcp__google_workspace__list_gmail_labels, mcp__google_workspace__modify_gmail_message_labels, mcp__google_workspace__batch_modify_gmail_message_labels, mcp__google_workspace__list_gmail_filters, mcp__google_workspace__create_gmail_filter, mcp__google_workspace__delete_gmail_filter
---

# Email Management

Manage Gmail accounts using two complementary tools:
- **Google Workspace MCP**: Best for searching, reading content, sending emails
- **Himalaya CLI**: Best for bulk operations (move, delete) - much faster than MCP for batch actions

## Strategy

1. **Use MCP to search and gather information** (fast, reliable search)
2. **Use Himalaya for bulk operations** (batch move/delete is much faster)
3. **Use MCP to send/draft emails** (better formatting support)

## Critical: Message ID Differences

**Gmail API (MCP) and Himalaya use DIFFERENT message IDs - they are NOT interchangeable!**

| Tool | ID Format | Example |
|------|-----------|---------|
| Gmail API (MCP) | Hexadecimal string | `19a82aa55f2a5f17` |
| Himalaya (IMAP) | Numeric integer | `163926` |

**Workflow implications:**
- If you search with MCP, you CANNOT use those IDs with Himalaya
- If you search with Himalaya, you CANNOT use those IDs with MCP
- For bulk delete: search AND delete with the same tool (Himalaya recommended)
- For reading content after MCP search: use MCP to read (IDs match)

## Default Account

**Unless the user specifies otherwise, always use `richard.stock@gmail.com` for all email operations.**

This applies to both:
- **Himalaya CLI**: Uses `richard-main` account (default, no `-a` flag needed)
- **Google Workspace MCP**: Use `user_google_email="richard.stock@gmail.com"`

## Configured Accounts

See [docs/himalaya/config.md](docs/himalaya/config.md) for current account setup.

| Account | Email | Tool | Notes |
|---------|-------|------|-------|
| richard-main | richard.stock@gmail.com | himalaya (default), MCP | **DEFAULT - use unless specified** |
| rebeca | rebeca.stock@gmail.com | MCP only (not yet in himalaya) | Must explicitly request |

## Common Workflows

### Search for emails from a sender

```bash
# Using MCP (preferred for search)
mcp__google_workspace__search_gmail_messages(query="from:sender@example.com", user_google_email="richard.stock@gmail.com")

# Using himalaya
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "sender@example.com"
```

### Bulk delete emails from a sender

**Use Himalaya for the entire workflow** (search + delete must use same tool due to ID differences):

```bash
# Pipe IDs directly to xargs (CORRECT - passes IDs as separate arguments)
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "@spammy.com" | jq -r '.[].id' | xargs himalaya message move -f "[Gmail]/All Mail" "[Gmail]/Trash"
```

**For searching by sender name with spaces:**
```bash
# Filter with jq, pipe to xargs
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 | jq -r '.[] | select(.from.name == "Nicholas Moore") | .id' | xargs himalaya message move -f "[Gmail]/All Mail" "[Gmail]/Trash"
```

**For date filtering (e.g., before a specific date):**
```bash
# Filter by date with jq, pipe to xargs
himalaya -o json envelope list -f "[Gmail]/All Mail" -s 500 from "sender@example.com" | jq -r --arg date "2023-07-01" '.[] | select(.date[:10] < $date) | .id' | xargs himalaya message move -f "[Gmail]/All Mail" "[Gmail]/Trash"
```

> **Warning**: Do NOT store IDs in a variable and pass with `$ids` - this passes all IDs as a single string argument, causing "invalid digit found in string" errors. Always use `xargs` to pipe IDs directly.

### Read email content

```bash
# Using MCP (preferred - better formatting)
mcp__google_workspace__get_gmail_message_content(message_id="abc123", user_google_email="richard.stock@gmail.com")

# Using himalaya
himalaya message read -f "[Gmail]/All Mail" <ID>
```

### Move emails to folder

```bash
# Batch move (himalaya is faster for multiple IDs)
himalaya message move -f "[Gmail]/All Mail" "Label/Folder" ID1 ID2 ID3
```

### Export emails as text/markdown

```bash
# Single email
himalaya message read -f "[Gmail]/All Mail" <ID> > ~/emails/message.md

# With JSON metadata
himalaya -o json message read -f "[Gmail]/All Mail" <ID> | jq -r '"---\nfrom: \(.from)\nsubject: \(.subject)\ndate: \(.date)\n---\n\n\(.body)"'
```

## Gmail Folder Names

Gmail uses special folder names via IMAP:

| Purpose | Folder Name |
|---------|-------------|
| All emails | `[Gmail]/All Mail` |
| Trash | `[Gmail]/Trash` |
| Sent | `[Gmail]/Sent Mail` |
| Drafts | `[Gmail]/Drafts` |
| Spam | `[Gmail]/Spam` |
| Starred | `[Gmail]/Starred` |
| Inbox | `INBOX` |

**Important**: Always search `[Gmail]/All Mail` to find all emails (archived emails won't appear in INBOX).

## Finding Sender Email Addresses

**Never guess email addresses.** When user mentions a sender by name (e.g., "LinkedIn Job Alerts"), always:

1. **Search broadly first** using partial domain or keyword:
   ```bash
   himalaya -o json envelope list -f "[Gmail]/All Mail" -s 100 from "linkedin" 2>/dev/null | jq '[.[] | {name: .from.name, addr: .from.addr}] | unique'
   ```

2. **Identify the correct `from.name`** from results that matches what user asked for

3. **Filter by `.from.name`** in your jq query (exact match is more reliable than guessing addresses)

**Example**: User says "delete LinkedIn Job Alerts" → search `from "linkedin"` → find entries with `.from.name == "LinkedIn Job Alerts"` → filter on that name.

## Reference Documentation

- [Himalaya Commands](docs/himalaya/commands.md) - Full CLI reference
- [Himalaya Config](docs/himalaya/config.md) - Configuration format
- [Google Workspace MCP](docs/google-workspace-mcp/gmail.md) - MCP tool reference

## Gmail Filters

**Filters automatically process incoming emails** - use them to auto-trash spam instead of manually deleting.

### Why Filters > Manual Deletion

- **Filters catch future emails** - Once set, you never see that sender again
- **No API rate limits** - Unlike batch-deleting via MCP/Himalaya
- **Persistent** - Survives across sessions, no scripts to run
- **Filters only affect NEW emails** - Existing emails must be manually trashed

### List Existing Filters

```python
mcp__google_workspace__list_gmail_filters(user_google_email="richard.stock@gmail.com")
```

### Create a Filter (Auto-Trash)

```python
# Block all emails from a domain
mcp__google_workspace__create_gmail_filter(
    user_google_email="richard.stock@gmail.com",
    from_address="@spammy-domain.com",
    delete=True
)

# Block specific email address
mcp__google_workspace__create_gmail_filter(
    user_google_email="richard.stock@gmail.com",
    from_address="newsletter@example.com",
    delete=True
)
```

### Filter Options

| Parameter | Description |
|-----------|-------------|
| `from_address` | Sender email or domain (use `@domain.com` for entire domain) |
| `to_address` | Filter by recipient |
| `subject` | Filter by subject (partial match) |
| `query` | Custom Gmail search query |
| `delete` | Move to trash (True/False) |
| `archive` | Skip inbox (True/False) |
| `mark_read` | Mark as read (True/False) |
| `add_label_ids` | List of label IDs to apply |
| `never_spam` | Never mark as spam (True/False) |

### Delete a Filter

```python
mcp__google_workspace__delete_gmail_filter(
    user_google_email="richard.stock@gmail.com",
    filter_id="ANe1Bmj..."
)
```

### Recommended Spam Workflow

When user reports spam:

1. **Search inbox** to find the email and identify the ACTUAL sender domain
   ```python
   mcp__google_workspace__search_gmail_messages(query="subject:\"Spam Subject\"", user_google_email="richard.stock@gmail.com")
   mcp__google_workspace__get_gmail_message_content(message_id="...", user_google_email="richard.stock@gmail.com")
   ```

2. **Check the From header** - Spammers often use fake display names (e.g., "Lendify" but actually from `@finopulses.com`)

3. **Create filter for the ACTUAL domain** (not the display name)
   ```python
   mcp__google_workspace__create_gmail_filter(from_address="@finopulses.com", delete=True, ...)
   ```

4. **Trash existing emails** from that sender
   ```python
   mcp__google_workspace__batch_modify_gmail_message_labels(
       message_ids=["id1", "id2", ...],
       add_label_ids=["TRASH"],
       remove_label_ids=["INBOX"],
       user_google_email="richard.stock@gmail.com"
   )
   ```

### Common Gotchas

- **Subdomains are different**: Filter for `@example.com` won't catch `@mail.example.com` - create separate filters
- **Display names lie**: Always check the actual `From:` address, not what's shown in the email client
- **Filters are case-insensitive**: `@Example.com` and `@example.com` are equivalent
- **Existing emails unaffected**: After creating a filter, manually trash existing emails from that sender

---

## Tips

1. **Date filtering**: Himalaya's IMAP date filter is unreliable with Gmail. Filter client-side with jq:
   ```bash
   himalaya -o json envelope list -f "[Gmail]/All Mail" from "@example.com" | jq --arg date "2025-01-01" '[.[] | select(.date[:10] < $date)]'
   ```

2. **Batch operations**: Himalaya accepts multiple IDs in one command - always batch for speed.

3. **Account switching**: Use `-a account-name` with himalaya for non-default accounts.

4. **JSON output**: Always use `-o json` when scripting for reliable parsing.
