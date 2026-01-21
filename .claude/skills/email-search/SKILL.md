---
description: Search emails using natural language. Converts request to `sec` command with appropriate flags.
---

# Email Search Skill

Translate the user's natural language email search request into the appropriate `sec` command.

## The `sec` Command (non-interactive)

```
sec [-d days] [-s] [-a account] <contact|all>

Arguments:
  <contact>    Contact name from contacts.txt (case-insensitive)
  all          Search all emails without contact filter

Flags:
  -d <days>    Days to search back (default: 14)
  -s           Search Sent folder instead of Inbox
  -a <account> Limit to one account (main, rstock-co, rebeca)
  -h           Show help

Examples:
  sec -s -d 30 "Mike Bullin"      Search sent to Mike, 30 days
  sec -s -d 30 all                All sent emails, 30 days
  sec -d 60 "E-Transfers"         Subject search, 60 days
  sec -a main "GIS"               Search GIS in main account inbox
```

## Contacts

Contacts are stored in `~/.config/contacts.txt`. Format:
- `Name: email1, email2` - searches FROM (or TO for sent)
- `Name: subject:keyword` - searches subject line

To see available contacts: `grep -v '^#' ~/.config/contacts.txt | cut -d: -f1`

## Workflow

1. **ALWAYS read contacts first:** `cat ~/.config/contacts.txt` - user input is often voice-to-text with spelling errors
2. Match the user's request to actual contact names (fuzzy match - "Mike Bullen" → "Mike Bullin")
3. Parse the natural language request for flags:
   - **Sent folder?** → add `-s`
   - **Specific account?** → add `-a <account>`
   - **Time range?** → add `-d <days>`
4. Run the command using Bash tool (contact name comes LAST)
5. Results table shows: DATE | ACCOUNT | FROM | SUBJECT | ID
6. **Offer to read emails** - Ask the user which email(s) they want to read
7. **Read requested emails** using: `himalaya message read -a <account> -f <folder> <id>`
   - Use INBOX for regular searches, `[Gmail]/Sent Mail` for `-s` searches
   - Format output using the Email Report Format below

## Email Report Format

When displaying a read email, use this exact format:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              EMAIL CONTENT                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

From:    [sender name and email]
To:      [recipient name and email]
Date:    [formatted date]
Subject: [subject line]

────────────────────────────────────────────────────────────────────────────────

[Email body - clean up signature images/cruft, keep the actual message content]

╔══════════════════════════════════════════════════════════════════════════════╗
║                              AI SUMMARY                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

[2-4 sentence summary of what the email is about, key points, and any action items]

╔══════════════════════════════════════════════════════════════════════════════╗
║                            ACTION ITEMS                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

[List any tasks the user needs to complete based on the email. If none, omit this section entirely.]

• [Action item 1]
• [Action item 2]

╔══════════════════════════════════════════════════════════════════════════════╗
║                      ACTIONS CLAUDE CAN TAKE                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

[Suggest actions I can help with using Himalaya. Only include relevant options:]

• Draft a reply - I'll write a response for your review before sending
• Forward to someone - Specify who and I'll prepare the forward
• Archive/move this email - Move to a specific folder
• Search related emails - Find other emails in this thread or from this sender
```

**Formatting rules:**
- Strip out image placeholders like `[cid:image...]` and `<#part type=image...>`
- Clean up excessive signature repetition in reply chains
- Keep the most recent message prominent, summarize older thread context if needed
- Date format: `January 8, 2026` (not raw format)
- **Action Items section:** Only show if the email contains actual tasks for the user (meetings to confirm, documents to send, decisions to make). Omit entirely if it's just informational.
- **Actions Claude Can Take:** Only list options that make sense for this specific email. Don't list all 4 options every time.

## Examples of Natural Language → Command

| User says | Command |
|-----------|---------|
| "search sent emails from last month" | `sec -s -d 30 all` |
| "check main account inbox for last week" | `sec -a main -d 7 all` |
| "search sent from rebeca's account, 60 days" | `sec -s -a rebeca -d 60 all` |
| "search emails from Mike Bullin" | `sec "Mike Bullin"` |
| "find emails to GIS in the last 30 days" | `sec -d 30 "GIS"` |
| "sent emails to Jason last week" | `sec -s -d 7 "Jason"` |

## Account Names

| Account | Email |
|---------|-------|
| `main` | richard.stock@gmail.com |
| `rstock-co` | rstock.co@gmail.com |
| `rebeca` | rebeca.stock@gmail.com |
