# Automatic Email Routing

Filters that auto-route emails to labels and skip the inbox.

**Last Updated:** 2025-12-09

---

## Active Routing Rules

| From | Label | Action |
|------|-------|--------|
| `@linkedin.com` | LinkedIn | Label + Skip Inbox |
| `Fay.Stewart@sd76.ab.ca` | FAMILY/Kids School | Label + Skip Inbox |
| `noreply@mhpsd.edsby.com` | FAMILY/Kids School | Label + Skip Inbox |
| `drgibb@redrockdental.ca` | HEALTH/Dentist | Label + Skip Inbox |
| `notify@payments.interac.ca` | FINANCES/E-Transfers | Label + Skip Inbox |
| `catch@payments.interac.ca` | FINANCES/E-Transfers | Label + Skip Inbox |
| Subject: `INTERAC e-Transfer: Your` | FINANCES/E-Transfers | Label + Skip Inbox |

---

## Categories

### LinkedIn
- All LinkedIn notifications auto-archived with label

### Kids School
- SD76 teacher emails (Fay Stewart)
- Edsby notifications (school portal)

### Health
- Red Rock Dental (Dr. Gibb)

### Finances
- Interac e-transfer notifications (by sender and subject match)

---

## Deleted Filters

| Date | From | Label | Reason |
|------|------|-------|--------|
| 2025-12-09 | `noreply@hubspot.com` | WORK/[A] TechPOS | No longer needed |
