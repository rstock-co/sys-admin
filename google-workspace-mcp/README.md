# Google Workspace MCP Server Setup

**Server:** [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) (965+ stars)
**Installed:** December 4, 2025

---

## What It Does

Allows Claude Code to interact with Google Workspace via natural language:
- **Gmail** - Read, send, search emails, manage labels
- **Google Calendar** - View, create, modify events
- **Google Drive** - Search, read, create files
- **Google Docs** - Read and edit documents
- **Google Sheets** - Read and edit spreadsheets

---

## Configuration

### Global MCP Config
**Location:** `~/.claude/.mcp.json`

```json
{
  "mcpServers": {
    "google_workspace": {
      "command": "uvx",
      "args": ["workspace-mcp", "--tool-tier", "core"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "188893630962-53fqg0prfuoljmfpe9ak8kmpe5nlqpnk.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "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",
        "OAUTHLIB_INSECURE_TRANSPORT": "1"
      }
    }
  }
}
```

### Google Cloud Project
**Project:** `arch-linux-sys-admin`
**Console:** https://console.cloud.google.com/

**Enabled APIs:**
- Gmail API
- Google Calendar API
- Google Drive API
- Google Docs API
- Google Sheets API

**OAuth Consent Screen:**
- User type: External (testing mode)
- Test user: `rstock.co@gmail.com`

---

## Credential Locations

| Purpose | Location |
|---------|----------|
| OAuth client credentials | `~/.claude/.mcp.json` (env vars) |
| User tokens (per-account) | `~/.credentials/` |
| Old Gmail MCP credentials | `~/.gmail-mcp/` (can delete) |

---

## Adding Multiple Accounts

The server supports multiple Google accounts. Each account authenticates separately.

**To add a new account:**
1. In Claude Code, make a request that requires authentication
2. A browser window opens for Google OAuth
3. Sign in with the Google account you want to add
4. Authorize the app
5. Credentials are stored in `~/.credentials/`

**To use a specific account:**
Ask Claude to use a specific email, e.g.:
- "Search my work@company.com inbox for invoices"
- "Send an email from personal@gmail.com to..."

---

## Usage Examples

### Gmail
```
"List my unread emails"
"Search for emails from Amazon in the last week"
"Send an email to john@example.com about the meeting"
"Show my Gmail labels"
```

### Calendar
```
"What's on my calendar today?"
"Create a meeting tomorrow at 2pm called 'Team Sync'"
"Show my events for next week"
```

### Drive
```
"Search my Drive for 'project proposal'"
"List files in my root Drive folder"
```

### Docs/Sheets
```
"Read the document called 'Meeting Notes'"
"Show me the contents of 'Budget 2025' spreadsheet"
```

---

## Tool Tiers

The server has three tool tiers configured via `--tool-tier`:

| Tier | Description |
|------|-------------|
| `core` | Essential tools (search, read, create, basic modify) - **Current** |
| `extended` | Core + management (labels, folders, batch operations) |
| `complete` | Full API access (comments, publishing, admin functions) |

To change tier, edit `~/.claude/.mcp.json` and modify the args:
```json
"args": ["workspace-mcp", "--tool-tier", "extended"]
```

---

## Troubleshooting

### "Access blocked" error during OAuth
Add yourself as a test user:
1. Google Cloud Console → APIs & Services → OAuth consent screen
2. Scroll to "Test users" → Add Users
3. Add your email address

### Server not starting
Check uvx is installed:
```bash
which uvx
```

Test the server manually:
```bash
uvx workspace-mcp --help
```

### Re-authenticate an account
Delete the credentials file for that account in `~/.credentials/` and re-authenticate.

### Enable more APIs
Go to Google Cloud Console → APIs & Services → Library and search for:
- Google Slides API
- Google Tasks API
- Google Forms API
- Google Chat API

---

## Cleanup Old Gmail MCP

The old single-account Gmail MCP can be removed:
```bash
rm -rf ~/.gmail-mcp/
```

---

## Links

- **Repository:** https://github.com/taylorwilsdon/google_workspace_mcp
- **Google Cloud Console:** https://console.cloud.google.com/
- **OAuth Credentials:** APIs & Services → Credentials
- **Enabled APIs:** APIs & Services → Library
