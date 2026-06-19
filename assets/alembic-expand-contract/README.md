# Expand/contract migration examples

Two SQL files that demonstrate the migration-safety gate from
[Module 07](../../modules/07-iac-governance.md). Verified against the kit's
`tools/check_migrations.py`.

| File | What it is | Gate result |
|------|-----------|-------------|
| [`unsafe.sql`](unsafe.sql) | one destructive migration (rename + drop + mandatory column) | **exit 1** — blocked |
| [`safe.sql`](safe.sql) | the **expand** phase (additive only); contract deferred + acknowledged | **exit 0** — allowed |

```bash
KIT=../platform-starter-kit   # adjust to your kit clone
python3 $KIT/tools/check_migrations.py unsafe.sql   # exit 1
python3 $KIT/tools/check_migrations.py safe.sql     # exit 0
```

The lesson (`<kit>/docs/DATABASE-MIGRATIONS.md`): a destructive change becomes
safe by splitting it across releases — **expand** (add the new shape, dual-write)
ships first; **contract** (remove the old shape) ships only after no running
version references it. When a destructive step is genuinely unavoidable and the
expand phase already shipped, mark it deliberately with a trailing
`migration-safety: ack <reason>` comment (see the last line of `safe.sql`).
