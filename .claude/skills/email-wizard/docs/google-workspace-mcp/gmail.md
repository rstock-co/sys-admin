# Google Workspace MCP - Gmail Tools

The Google Workspace MCP server provides Gmail access through these tools.

## Available Tools

### search_gmail_messages

Search for emails using Gmail query syntax.

**Parameters:**
- `query` (required): Gmail search query
- `user_google_email` (required): User's Gmail address
- `page_size` (optional): Max results (default: 10)

**Gmail Query Syntax:**
- `from:sender@example.com` - From specific sender
- `to:recipient@example.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `in:inbox` / `in:trash` / `in:spam` - In specific folder
- `is:unread` / `is:read` - Read status
- `is:starred` - Starred emails
- `has:attachment` - Has attachments
- `after:2025/01/01` - After date
- `before:2025/12/31` - Before date
- `older_than:7d` / `newer_than:1m` - Relative dates
- `label:labelname` - Has specific label

**Example:**
```
mcp__google_workspace__search_gmail_messages(
  query="from:amazon.com after:2025/01/01",
  user_google_email="richard.stock@gmail.com",
  page_size=25
)
```

**Returns:** Message IDs and Thread IDs with Gmail web links.

---

### get_gmail_message_content

Get full content of a single email.

**Parameters:**
- `message_id` (required): Gmail message ID
- `user_google_email` (required): User's Gmail address

**Example:**
```
mcp__google_workspace__get_gmail_message_content(
  message_id="19aea575d4e322a7",
  user_google_email="richard.stock@gmail.com"
)
```

**Returns:** Subject, From, To, Cc, and full body content.

---

### get_gmail_messages_content_batch

Get content of multiple emails in one request.

**Parameters:**
- `message_ids` (required): List of message IDs (max 25)
- `user_google_email` (required): User's Gmail address
- `format` (optional): `"full"` (default) or `"metadata"`

**Example:**
```
mcp__google_workspace__get_gmail_messages_content_batch(
  message_ids=["id1", "id2", "id3"],
  user_google_email="richard.stock@gmail.com",
  format="metadata"
)
```

---

### get_gmail_thread_content

Get all messages in a conversation thread.

**Parameters:**
- `thread_id` (required): Gmail thread ID
- `user_google_email` (required): User's Gmail address

**Example:**
```
mcp__google_workspace__get_gmail_thread_content(
  thread_id="19aea575d4e322a7",
  user_google_email="richard.stock@gmail.com"
)
```

---

### get_gmail_threads_content_batch

Get multiple threads in one request.

**Parameters:**
- `thread_ids` (required): List of thread IDs (max 25)
- `user_google_email` (required): User's Gmail address

---

### send_gmail_message

Send an email.

**Parameters:**
- `to` (required): Recipient email
- `subject` (required): Email subject
- `body` (required): Email body
- `user_google_email` (required): Sender's Gmail address
- `body_format` (optional): `"plain"` (default) or `"html"`
- `cc` (optional): CC recipient
- `bcc` (optional): BCC recipient
- `thread_id` (optional): For replies - thread to reply in
- `in_reply_to` (optional): Message-ID being replied to
- `references` (optional): Chain of Message-IDs for threading

**Example - New email:**
```
mcp__google_workspace__send_gmail_message(
  to="recipient@example.com",
  subject="Hello",
  body="Hi there!",
  user_google_email="richard.stock@gmail.com"
)
```

**Example - Reply:**
```
mcp__google_workspace__send_gmail_message(
  to="recipient@example.com",
  subject="Re: Original Subject",
  body="Thanks for your email!",
  user_google_email="richard.stock@gmail.com",
  thread_id="19aea575d4e322a7"
)
```

---

### draft_gmail_message

Create a draft email.

**Parameters:** Same as `send_gmail_message`, but `to` is optional.

**Example:**
```
mcp__google_workspace__draft_gmail_message(
  subject="Draft Subject",
  body="Draft content...",
  user_google_email="richard.stock@gmail.com"
)
```

---

### list_gmail_labels

List all labels/folders in the account.

**Parameters:**
- `user_google_email` (required): User's Gmail address

**Returns:** Label IDs, names, and types.

---

### modify_gmail_message_labels

Add or remove labels from a message.

**Parameters:**
- `message_id` (required): Gmail message ID
- `user_google_email` (required): User's Gmail address
- `add_label_ids` (optional): List of label IDs to add
- `remove_label_ids` (optional): List of label IDs to remove

**Common operations:**
- Archive: Remove `INBOX` label
- Delete: Add `TRASH` label
- Star: Add `STARRED` label
- Mark unread: Remove `UNREAD` label

**Example - Archive:**
```
mcp__google_workspace__modify_gmail_message_labels(
  message_id="19aea575d4e322a7",
  user_google_email="richard.stock@gmail.com",
  remove_label_ids=["INBOX"]
)
```

---

### batch_modify_gmail_message_labels

Modify labels on multiple messages at once.

**Parameters:**
- `message_ids` (required): List of message IDs
- `user_google_email` (required): User's Gmail address
- `add_label_ids` (optional): Labels to add
- `remove_label_ids` (optional): Labels to remove

---

### manage_gmail_label

Create, update, or delete labels.

**Parameters:**
- `action` (required): `"create"`, `"update"`, or `"delete"`
- `user_google_email` (required): User's Gmail address
- `name` (optional): Label name (required for create)
- `label_id` (optional): Label ID (required for update/delete)
- `label_list_visibility`: `"labelShow"` or `"labelHide"`
- `message_list_visibility`: `"show"` or `"hide"`

---

## Configured Accounts

| Email | Status |
|-------|--------|
| richard.stock@gmail.com | Active |
| rebeca.stock@gmail.com | Active |

## Tips

1. **Search is powerful**: Use Gmail's query syntax for precise searches
2. **Batch operations**: Use batch tools when dealing with multiple messages
3. **Thread vs Message**: Threads contain multiple messages in a conversation
4. **Label IDs**: Use `list_gmail_labels` to get label IDs for modify operations
