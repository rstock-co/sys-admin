---
argument-hint: <percent-used> <time-MST>
description: Calculate if Claude Code usage is ahead or behind schedule
---

# Claude Code Usage Calculator

Calculates whether your Claude Code usage is on track, ahead, or behind based on the billing cycle.

## Arguments

- `<percent-used>`: Your current usage percentage (e.g., `45` or `45%`)
- `<time-MST>`: Current time in Mountain Standard Time (e.g., `14:30` or `2:30pm`)

## Example Usage

```bash
/calculate-usage 45 14:30
/calculate-usage 72% 9:00am
```

## Instructions

When the user runs this command, perform the following calculation:

### 1. Parse Arguments

Extract from `$ARGUMENTS`:
- **Usage percent**: Strip `%` if present, convert to number
- **Time MST**: Parse the time (handle 24h or 12h format)

### 2. Determine Billing Cycle Position

**Assumptions:**
- Billing cycle is monthly, starting on the 1st
- Current date: Use today's date
- Month length: Use actual days in current month

**Calculate:**
```
days_elapsed = current_day + (current_hour / 24)
days_in_month = total days in current month
expected_percent = (days_elapsed / days_in_month) * 100
```

### 3. Calculate Variance

```
variance = actual_usage - expected_percent
```

- **Positive variance**: AHEAD (using faster than expected)
- **Negative variance**: BEHIND (have budget headroom)
- **Within ±2%**: ON TRACK

### 4. Calculate Time Equivalent

Convert variance to days/hours:
```
variance_in_days = (variance / 100) * days_in_month
```

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 CLAUDE CODE USAGE TRACKER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Current Usage:    {actual}%
 Expected Usage:   {expected}%
 Variance:         {variance}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 STATUS: {AHEAD / ON TRACK / BEHIND}

 {If AHEAD}
 You're {days}d {hours}h AHEAD of schedule
 At this pace, you'll hit 100% by {date}

 {If BEHIND}
 You're {days}d {hours}h BEHIND schedule
 You have extra budget headroom

 {If ON TRACK}
 Usage is aligned with billing cycle

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Billing Cycle: Day {current_day} of {days_in_month}
 Time (MST):    {time}
 Days Left:     {days_remaining}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Quick Mental Math Reference

For the user's reference when not running the command:

| Day of Month | Expected Usage |
|--------------|----------------|
| 1            | ~3%            |
| 5            | ~16%           |
| 10           | ~33%           |
| 15           | ~50%           |
| 20           | ~66%           |
| 25           | ~83%           |
| 30           | ~100%          |

## Notes

- MST = UTC-7 (no daylight saving adjustment)
- If billing cycle starts on a different day, user should specify
- Calculation assumes linear usage distribution is ideal
