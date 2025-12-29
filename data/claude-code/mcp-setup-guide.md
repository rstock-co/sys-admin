# MCP Server Setup Guide for Claude Code

## The Three Scopes

| Scope | Flag | Storage | Use Case |
|-------|------|---------|----------|
| `local` | `-s local` (default) | `~/.claude.json` (project-specific) | **Use this.** Personal servers for current project |
| `project` | `-s project` | `.mcp.json` in project root | Team-shared, requires approval prompt |
| `user` | `-s user` | `~/.claude.json` (global) | Available in all projects |

**Key insight:** `local` is the default and stores config in your user settings but scoped to the specific project. This avoids the approval prompt issues of `project` scope.

---

## Quick Setup (Recommended)

```bash
cd /path/to/your/project

# Add a stdio server (local scope is default)
claude mcp add <name> --env KEY=value -- <command> [args]

# Example: Google Sheets MCP
claude mcp add google-sheets \
  --env SERVICE_ACCOUNT_PATH=/path/to/credentials.json \
  -- uvx mcp-google-sheets@latest
```

---

## Transport Types

### stdio (local process)
```bash
claude mcp add <name> -- <command> [args]

# Examples
claude mcp add airtable --env AIRTABLE_API_KEY=xxx -- npx -y airtable-mcp-server
claude mcp add postgres -- npx -y @bytebase/dbhub --dsn "postgresql://..."
```

### HTTP (remote server)
```bash
claude mcp add --transport http <name> <url>

# Examples
claude mcp add --transport http notion https://mcp.notion.com/mcp
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

### SSE (deprecated, use HTTP)
```bash
claude mcp add --transport sse <name> <url>
```

---

## JSON Config Method

```bash
claude mcp add-json <name> '<json>'

# Example
claude mcp add-json my-server '{"command":"uvx","args":["some-mcp@latest"],"env":{"API_KEY":"xxx"}}'
```

---

## Managing Servers

```bash
# List all servers
claude mcp list

# Get details
claude mcp get <name>

# Remove server
claude mcp remove <name>

# Inside Claude REPL
/mcp                    # Check status, authenticate OAuth servers
/mcp enable <name>      # Enable a disabled server
```

---

## Common Mistakes

### Wrong: Using project scope without understanding approval
```bash
claude mcp add my-server -s project -- npx server
# Creates .mcp.json, requires approval prompt that may not appear
```

### Right: Use local scope (default)
```bash
claude mcp add my-server -- npx server
# Stored in ~/.claude.json scoped to this project, works immediately
```

### Wrong: Forgetting the `--` separator
```bash
claude mcp add my-server npx -y server  # Breaks
```

### Right: Use `--` before the command
```bash
claude mcp add my-server -- npx -y server  # Works
```

---

## Environment Variables

```bash
# Single env var
claude mcp add server --env API_KEY=xxx -- command

# Multiple env vars
claude mcp add server --env KEY1=xxx --env KEY2=yyy -- command
```

---

## Verification Steps

1. Add the server:
   ```bash
   claude mcp add my-server -- command
   ```

2. Verify via CLI:
   ```bash
   claude mcp list
   # Should show: my-server: command - ✓ Connected
   ```

3. Verify in Claude REPL:
   ```bash
   cd /project && claude
   > /mcp
   # Should show server listed
   ```

---

## Scope Precedence

If same server name exists in multiple scopes:
1. `local` wins over
2. `project` wins over
3. `user`

---

## Troubleshooting

### Server not showing in `/mcp`
- Use `local` scope (default), not `project` scope
- Ensure you're in the correct project directory
- Run `claude mcp list` outside REPL to verify

### "Connection closed" errors
- Check command path is correct
- Verify environment variables are set
- Test command manually in terminal

### OAuth servers
- Add server first, then run `/mcp` in REPL
- Select server and choose "Authenticate"
- Browser opens for OAuth flow
