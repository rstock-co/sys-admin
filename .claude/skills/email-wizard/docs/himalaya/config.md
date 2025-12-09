# Himalaya Configuration

Config file location: `~/.config/himalaya/config.toml`

## Current Configuration

```toml
[accounts.richard-main]
default = true
email = "richard.stock@gmail.com"
display-name = "Richard Stock"
downloads-dir = "/home/neo/Downloads"
folder.alias.trash = "[Gmail]/Trash"
folder.alias.sent = "[Gmail]/Sent Mail"
folder.alias.drafts = "[Gmail]/Drafts"
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.login = "richard.stock@gmail.com"
backend.encryption.type = "tls"
backend.auth.type = "password"
backend.auth.raw = "<app-password>"
message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 465
message.send.backend.login = "richard.stock@gmail.com"
message.send.backend.encryption.type = "tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "<app-password>"
```

## Gmail Configuration Template

To add a new Gmail account:

```toml
[accounts.account-name]
default = false
email = "user@gmail.com"
display-name = "Display Name"
downloads-dir = "/home/neo/Downloads"

# Gmail folder aliases (required for proper trash/sent behavior)
folder.alias.trash = "[Gmail]/Trash"
folder.alias.sent = "[Gmail]/Sent Mail"
folder.alias.drafts = "[Gmail]/Drafts"

# IMAP backend
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.login = "user@gmail.com"
backend.encryption.type = "tls"
backend.auth.type = "password"
backend.auth.raw = "<16-char-app-password>"

# SMTP for sending
message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 465
message.send.backend.login = "user@gmail.com"
message.send.backend.encryption.type = "tls"
message.send.backend.auth.type = "password"
message.send.backend.auth.raw = "<16-char-app-password>"
```

## Getting an App Password

1. Go to https://myaccount.google.com/apppasswords
2. Create app password for "Mail" / "Other (Himalaya)"
3. Copy the 16-character password (no spaces)
4. Use this for `backend.auth.raw`

**Note:** Regular Gmail passwords don't work - you must use an App Password.

## Configuration Options

### Account Options

| Option | Description |
|--------|-------------|
| `default` | Set as default account (only one can be true) |
| `email` | Email address |
| `display-name` | Name shown in sent emails |
| `downloads-dir` | Where to save attachments |

### Folder Aliases

Required for Gmail to work correctly:

| Alias | Gmail Folder |
|-------|--------------|
| `folder.alias.trash` | `[Gmail]/Trash` |
| `folder.alias.sent` | `[Gmail]/Sent Mail` |
| `folder.alias.drafts` | `[Gmail]/Drafts` |

### Backend Options (IMAP)

| Option | Description |
|--------|-------------|
| `backend.type` | `imap` |
| `backend.host` | IMAP server hostname |
| `backend.port` | IMAP port (993 for TLS) |
| `backend.login` | IMAP username (email) |
| `backend.encryption.type` | `tls` or `starttls` |
| `backend.auth.type` | `password` or `oauth2` |
| `backend.auth.raw` | Password/token value |

### Send Backend Options (SMTP)

| Option | Description |
|--------|-------------|
| `message.send.backend.type` | `smtp` |
| `message.send.backend.host` | SMTP server hostname |
| `message.send.backend.port` | SMTP port (465 for SSL, 587 for STARTTLS) |
| `message.send.backend.login` | SMTP username (email) |
| `message.send.backend.encryption.type` | `tls` or `starttls` |
| `message.send.backend.auth.type` | `password` or `oauth2` |
| `message.send.backend.auth.raw` | Password/token value |

## Multiple Accounts

Add additional accounts with unique names:

```toml
[accounts.personal]
default = true
email = "personal@gmail.com"
# ... rest of config

[accounts.work]
default = false
email = "work@company.com"
# ... rest of config
```

Switch accounts with `-a` flag:

```bash
himalaya -a work envelope list
himalaya -a personal message read 123
```

## Wizard Setup

Run the interactive wizard to create a new account:

```bash
himalaya account configure <account-name>
```

The wizard will prompt for all settings interactively.
