---
description: Search emails using natural language. Converts request to `sec` command with appropriate flags.
---

# Email Search Skill

Translate the user's natural language email search request into the appropriate `sec` command.

## The `sec` Command (non-interactive)

```
sec [-d days] [-s] [-u] [-a account] <contact|all>

Arguments:
  <contact>    Contact name from contacts.txt (case-insensitive)
  all          Search all emails without contact filter

Flags:
  -d <days>    Days to search back (default: 14)
  -s           Search Sent folder instead of Inbox
  -u           Unread only (new emails)
  -a <account> Limit to one account (main, rstock-co, rebeca)
  -h           Show help

Examples:
  sec -s -d 30 "Mike Bullin"      Search sent to Mike, 30 days
  sec -s -d 30 all                All sent emails, 30 days
  sec -u "Lee Waechter"           New/unread emails from Lee only
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
   - **Unread/new only?** → add `-u` (trigger words: "new", "unread", "any new", "haven't read")
   - **Specific account?** → add `-a <account>`
   - **Time range?** → add `-d <days>`
4. Run the command using Bash tool (contact name comes LAST)
5. Results table shows: FLAGS | DATE | ACCOUNT | FROM | SUBJECT | ID
   - The `R` flag means the email has been replied to
6. **Use AskUserQuestion tool** to let user select which email(s) to read (see Email Selection UI below)
7. **Read requested emails** using: `himalaya message read -a <account> -f <folder> <id>`
   - **Track the reply status** from the envelope list (R flag) - you'll need this for step 8
   - Use INBOX for regular searches, `[Gmail]/Sent Mail` for `-s` searches
   - Format output using the Email Report Format below

## Email Selection UI

After displaying search results, use the **AskUserQuestion tool** to let the user select emails interactively.

### Rules

- **Max 3 emails per question** (reserve 1 slot for pagination)
- Each option label: `[DATE] [STATUS] SUBJECT` (truncate subject if needed)
  - Status from FLAGS column: `*` = `[UNREAD]`, `R` = `[REPLIED]`, empty = `[READ]`
- Each option description: `From: SENDER`
- Enable `multiSelect: true` so user can pick multiple emails
- Header: `"Read email"`

### Pagination (more than 3 results)

When results exceed 3 emails, add pagination options:

| Results | Options shown |
|---------|---------------|
| 1-3 | Show all emails, no pagination |
| 4-6 | Show emails 1-3 + "More results (4-6)" |
| 7-9 | Show emails 1-3 + "More results (4-9)" |
| 10+ | Show emails 1-3 + "More results (4-10+)" |

When user selects "More results":
- Show next batch of 3 emails + "More results" if needed
- Add "Back to previous" option to go back

### Example AskUserQuestion call

```json
{
  "questions": [{
    "question": "Which email(s) would you like to read?",
    "header": "Read email",
    "multiSelect": true,
    "options": [
      {
        "label": "[Jan 14] [REPLIED] Re: Employment Proposal",
        "description": "From: Mike Bullin"
      },
      {
        "label": "[Jan 08] [UNREAD] RE: Employment Proposal",
        "description": "From: Mike Bullin"
      },
      {
        "label": "[Jan 05] [READ] Project Update",
        "description": "From: Mike Bullin"
      }
    ]
  }]
}
```

### If user types custom input

The AskUserQuestion tool always allows "Other" for custom input. Handle these cases:
- User types an email ID directly → read that email
- User types "all" → read all emails in current view
- User types "none" or "cancel" → end the search

## Fetching Your Reply (for emails with R flag)

When an email has the `R` flag (already replied), fetch the user's reply from the sent folder:

```bash
# Search sent folder for reply to this sender with matching subject
himalaya envelope list -a <account> -f "[Gmail]/Sent Mail" -w 200 --page-size 50 | grep -i "<sender_email_or_name>"
```

Look for emails with "Re:" or "RE:" prefix matching the original subject, sent AFTER the received email date. Read the most recent matching sent email.

## Email Report Format

When displaying a read email, use this exact format:

**If email has R flag (already replied), show YOUR REPLY section first:**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              YOUR REPLY                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

To:      [recipient]
Date:    [date you replied]
Subject: [subject line]

────────────────────────────────────────────────────────────────────────────────

[Your reply body - just your message, not the quoted thread]
```

**Then show the original email (use "ORIGINAL EMAIL" header for replied, "EMAIL CONTENT" for unreplied):**

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ORIGINAL EMAIL (or EMAIL CONTENT)                         ║
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

[2-4 sentence summary. If email was replied to, summarize the exchange and note what was said in the reply. Example: "Lee asked about Linux compatibility. You replied explaining how Microsoft 365 works through the browser. The thread is resolved unless you need to follow up."]

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
• Send a follow-up - I'll draft a follow-up message to your previous reply
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
- **IMPORTANT: For replied emails (R flag):**
  - Do NOT suggest "Draft a reply" - use "Send a follow-up" instead
  - The AI Summary should reference what the user already said in their reply
  - Only suggest follow-up if there's a reason to (e.g., unanswered question, pending action)

## Examples of Natural Language → Command

| User says | Command |
|-----------|---------|
| "search sent emails from last month" | `sec -s -d 30 all` |
| "check main account inbox for last week" | `sec -a main -d 7 all` |
| "search sent from rebeca's account, 60 days" | `sec -s -a rebeca -d 60 all` |
| "search emails from Mike Bullin" | `sec "Mike Bullin"` |
| "any new emails from Lee" | `sec -u "Lee Waechter"` |
| "check for unread emails from GIS" | `sec -u "GIS"` |
| "find emails to GIS in the last 30 days" | `sec -d 30 "GIS"` |
| "sent emails to Jason last week" | `sec -s -d 7 "Jason"` |

## Sending Replies

To send a reply programmatically (without opening an editor), use a two-step process:

```bash
# Generate template and pipe to send
himalaya template reply -a <account> -f <folder> <id> '<body>' | himalaya message send -a <account>
```

**Example:**
```bash
himalaya template reply -a rebeca -f INBOX 37655 'Hi Nicole,

Thanks for the info!

Quick question - how many of the 14 classes would they be missing by starting now?

Thanks,
Rebeca' | himalaya message send -a rebeca
```

**Notes:**
- `himalaya message reply` requires `$EDITOR` and opens an interactive editor - don't use it
- The template command generates proper headers (From, To, In-Reply-To, Subject)
- Single quotes in the body need escaping: `we'"'"'ll` or `we'\''ll`
- Always draft the email and show it to the user before sending

## Account Names

| Account | Email |
|---------|-------|
| `main` | richard.stock@gmail.com |
| `rstock-co` | rstock.co@gmail.com |
| `rebeca` | rebeca.stock@gmail.com |
