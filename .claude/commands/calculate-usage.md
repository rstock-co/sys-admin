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

**Billing cycle:**
- Resets every **Monday at 12:00 PM (noon) MST**
- Total cycle length: **168 hours** (7 days)

**Calculate hours elapsed since last reset:**
```
# Find hours since last Monday 12:00 PM MST
current_day_of_week = 0 (Mon) to 6 (Sun)
hours_since_monday_midnight = (current_day_of_week * 24) + current_hour

# Adjust for noon reset (subtract 12 hours, handle wrap-around)
if current_day == Monday AND current_hour < 12:
    # Before reset - we're in previous week's cycle
    hours_elapsed = 168 - (12 - current_hour)
else:
    hours_elapsed = hours_since_monday_midnight - 12
    if hours_elapsed < 0:
        hours_elapsed += 168

expected_percent = (hours_elapsed / 168) * 100
```

### 3. Calculate Variance

```
variance = actual_usage - expected_percent
```

- **Positive variance**: AHEAD (using faster than expected)
- **Negative variance**: BEHIND (have budget headroom)
- **Within ±2%**: ON TRACK

### 4. Calculate Time Equivalent

Convert variance to hours:
```
variance_in_hours = (variance / 100) * 168
variance_days = floor(variance_in_hours / 24)
variance_hours = variance_in_hours % 24
```

## Output Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 CLAUDE CODE USAGE TRACKER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Current Usage:    {actual}%
 Expected Usage:   {expected}%
 Variance:         {+/-variance}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 STATUS: {AHEAD / ON TRACK / BEHIND}

 {If AHEAD}
 You're {days}d {hours}h AHEAD of schedule
 At this pace, you'll hit 100% by {day} {time}

 {If BEHIND}
 You're {days}d {hours}h BEHIND schedule
 You have extra budget headroom

 {If ON TRACK}
 Usage is aligned with billing cycle

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Cycle Progress:   {hours_elapsed}h of 168h ({percent_through}%)
 Time (MST):       {day_name} {time}
 Next Reset:       Monday 12:00 PM MST
 Hours Until Reset: {hours_remaining}h

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Quick Mental Math Reference

For the user's reference when not running the command:

| Time Since Reset    | Expected Usage |
|---------------------|----------------|
| Mon 12:00 PM (0h)   | 0%             |
| Mon 6:00 PM (6h)    | ~4%            |
| Tue 12:00 PM (24h)  | ~14%           |
| Wed 12:00 PM (48h)  | ~29%           |
| Thu 12:00 PM (72h)  | ~43%           |
| Fri 12:00 PM (96h)  | ~57%           |
| Sat 12:00 PM (120h) | ~71%           |
| Sun 12:00 PM (144h) | ~86%           |
| Mon 12:00 PM (168h) | 100% (reset)   |

**Quick rule:** Each full day ≈ 14.3% of budget

## Notes

- MST = UTC-7 (Mountain Standard Time, no daylight saving)
- Reset occurs every Monday at 12:00 PM (noon) MST
- Calculation assumes linear usage distribution is ideal
