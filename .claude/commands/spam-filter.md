---
argument-hint: [email-address]
description: Scan inbox for spam, create filters, and bulk-delete spam emails
---

# Spam Filter Workflow

Scan inbox for potential spam and create filters to block them.

## Usage

```bash
/spam-filter                           # Scan richard.stock@gmail.com (default)
/spam-filter rebeca.stock@gmail.com    # Scan specific email account
```

**Email account:** $ARGUMENTS (default: richard.stock@gmail.com)

## Instructions

You are helping the user identify and filter spam from their Gmail inbox. Follow these steps:

### Step 1: Determine Email Account

If `$ARGUMENTS` is provided and looks like an email address, use it. Otherwise, default to `richard.stock@gmail.com`.

### Step 2: Search Inbox (Past 2 Weeks)

Search for emails from the past 2 weeks:

```python
mcp__google_workspace__search_gmail_messages(
    query="in:inbox newer_than:14d",
    user_google_email="<email>",
    page_size=100
)
```

Then fetch metadata for all messages to identify senders:

```python
mcp__google_workspace__get_gmail_messages_content_batch(
    message_ids=[...],
    user_google_email="<email>",
    format="metadata"
)
```

### Step 3: Analyze and Categorize Senders

Group emails by sender domain and categorize them:

**SPAM CANDIDATES** - Marketing, newsletters, promotions:
- Retail marketing (store-news@, offers@, deals@)
- Newsletter services (substack, beehiiv, mailchimp)
- Social media notifications (linkedin, facebook)
- Financial spam (credit offers, loan spam)
- Political campaigns
- Promotional emails with clickbait subjects

**LEGITIMATE** - Keep these:
- Order confirmations (amazon auto-confirm, shipment tracking)
- Banking/financial statements (actual account notifications)
- Receipts and invoices from purchases you made
- Personal contacts
- Work-related emails

Present findings to user in a table format:

```
| Sender | Domain | Count | Recommendation |
|--------|--------|-------|----------------|
| Amazon Marketing | store-news@amazon.ca | 3 | SPAM |
| Amazon Orders | auto-confirm@amazon.ca | 2 | KEEP |
```

### Step 4: Get User Confirmation

Ask the user:
- Which spam candidates to filter (can say "all" or list specific ones)
- Any legitimate emails incorrectly flagged
- Any additional senders to filter that weren't flagged

### Step 5: Create Filters and Clean Up

For each confirmed spam sender:

1. **Create filter** for the domain (prefer `@domain.com` over specific addresses):
   ```python
   mcp__google_workspace__create_gmail_filter(
       user_google_email="<email>",
       from_address="@spam-domain.com",
       delete=True
   )
   ```

2. **Search for ALL existing emails** from that sender in inbox:
   ```python
   mcp__google_workspace__search_gmail_messages(
       query="from:@spam-domain.com in:inbox",
       user_google_email="<email>",
       page_size=100
   )
   ```

3. **Trash all existing emails**:
   ```python
   mcp__google_workspace__batch_modify_gmail_message_labels(
       message_ids=[...],
       add_label_ids=["TRASH"],
       remove_label_ids=["INBOX"],
       user_google_email="<email>"
   )
   ```

### Step 6: Summary

Report back:
- Number of filters created
- Number of emails trashed
- List of filtered domains

## Important Notes

- **Check actual From address** - Spammers use fake display names (e.g., "Lendify" from `@finopulses.com`)
- **Subdomains need separate filters** - `@tim.example.com` is different from `@example.com`
- **Prefer domain filters** - `@domain.com` catches all addresses from that domain
- **Filters only affect future emails** - Must manually trash existing emails after creating filter
