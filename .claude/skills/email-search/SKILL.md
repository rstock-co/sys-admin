---
description: Search emails using natural language. Converts request to `se` command with appropriate flags.
---

# Email Search Skill

Translate the user's natural language email search request into the appropriate `se` command.

## The `se` Command

```
se [-d days] [-s] [-a account] [-h]

Flags:
  -d <days>    Days to search back (default: 14)
  -s           Search Sent folder instead of Inbox
  -a <account> Limit to one account (main, rstock-co, rebeca)
  -h           Show help

Examples:
  se              Search inbox, last 14 days
  se -s -d 30     Search sent, last 30 days
  se -a main      Search only main account
  se -s -a rebeca -d 7   Search rebeca's sent, last 7 days
```

## Contacts

Contacts are stored in `~/.config/contacts.txt`. Format:
- `Name: email1, email2` - searches FROM (or TO for sent)
- `Name: subject:keyword` - searches subject line
- `* All *` - search all emails without contact filter

## Workflow

1. Parse the user's natural language request
2. Determine the flags needed:
   - **Sent folder?** → add `-s`
   - **Specific account?** → add `-a <account>`
   - **Time range?** → add `-d <days>`
3. Run the command using Bash tool
4. The command opens fzf for contact selection, then displays results

## Examples of Natural Language → Command

| User says | Command |
|-----------|---------|
| "search my sent emails from last month" | `se -s -d 30` |
| "check main account inbox for last week" | `se -a main -d 7` |
| "search all sent from rebeca's account, 60 days" | `se -s -a rebeca -d 60` |
| "search emails" | `se` |
| "look through sent on rstock-co" | `se -s -a rstock-co` |

## Account Names

- `main` - richard.stock@gmail.com
- `rstock-co` - rstock.co@gmail.com
- `rebeca` - rebeca.stock@gmail.com
