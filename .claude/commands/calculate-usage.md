---
argument-hint: [percent-used] [time-MST]
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
- Resets every **Wednesday at 3:59 PM MST**
- Total cycle length: **168 hours** (7 days)

**Calculate hours elapsed since last reset (anchor to Wednesday 3:59 PM):**

Count full days from Wednesday 3:59 PM to current day, then add remaining hours:

| Current Day | Full days since Wed 3:59 PM | Base hours |
|-------------|----------------------------|------------|
| Wed (after 3:59 PM) | 0 | 0 |
| Thu | 1 | 24 |
| Fri | 2 | 48 |
| Sat | 3 | 72 |
| Sun | 4 | 96 |
| Mon | 5 | 120 |
| Tue | 6 | 144 |
| Wed (before 3:59 PM) | 6 | 144 |

```
# Calculate hours from current time to 3:59 PM
if current_day == Wednesday and current_time < 3:59 PM:
    # Before reset - use previous cycle
    hours_from_359pm = (15.98 - current_hour_decimal)
    hours_elapsed = 168 - hours_from_359pm
else:
    hours_elapsed = base_hours_from_table + (current_hour - 15.98)
    # Adjust if current time is before 3:59 PM on that day
    if current_time < 3:59 PM:
        hours_elapsed = base_hours_from_table - (15.98 - current_hour_decimal)

expected_percent = (hours_elapsed / 168) * 100
```

**Simple method:** Count hours directly from Wed 3:59 PM to now:
- Wed 3:59 PM → Thu 3:59 PM = 24h
- Thu 3:59 PM → Fri 3:59 PM = 24h
- etc., then add/subtract hours for current time vs 3:59 PM

### 3. Workday Calculation (Simple)

The Wednesday 4pm reset means the first real workday is Thursday. Weekdays = 1, weekend days = 0.375 each.

| Day | Day Value | Cumulative | Expected % |
|-----|-----------|------------|------------|
| Thu | 1 | 1 | 17.4% |
| Fri | 1 | 2 | 34.8% |
| Sat | 0.375 | 2.375 | 41.3% |
| Sun | 0.375 | 2.75 | 47.8% |
| Mon | 1 | 3.75 | 65.2% |
| Tue | 1 | 4.75 | 82.6% |
| Wed | 1 | 5.75 | 100% |

Total cycle = 5.75 work units

```
workday_expected = (cumulative_days / 5.75) * 100
workday_variance = actual_usage - workday_expected
```

### 4. Calculate Variance (Hourly)

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

## Output

Output both calculations:

```
Workday: +3% ahead (2.375/5.75 days)
Hourly:  -12% behind
```

Format:
- **Workday line**: variance + cumulative days fraction
- **Hourly line**: variance only
- Use `On track` if within ±2%
