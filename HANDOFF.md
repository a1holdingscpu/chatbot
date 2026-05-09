# Infrastructure Audit: Live State vs. Documented State

**Date:** 2026-05-09
**Branch:** `claude/audit-system-drift-wnWYc`
**Source:** Parallel four-agent live audit (Mac Mini runtime, Mac Mini PostgreSQL, VPS n8n export, VPS PostgreSQL) synthesized against `MEMORY.md`.

---

## Scope

- Mac Mini M4 runtime (processes, ports, Docker, Ollama, crons)
- Mac Mini PostgreSQL (`clue_runtime`, `n8n_local`)
- VPS n8n (82 workflows — 57 active, 25 inactive)
- VPS PostgreSQL (`blitz` — 14 schemas, 144 tables; `mcp` — 8 legacy tables; plus `ceiba`, `langfuse`, `orchestrator`, `n8n` databases)

---

## Critical Drift (action required)

### 1. Langfuse is crashlooping on VPS
- **Documented:** "Healthy (fixed crashloop 2026-04-19)"
- **Actual:** `Restarting (1) 38 seconds ago` — active crashloop.
- **Impact:** Trace pipeline is blind. APO M2 Phase 3 evals, council Langfuse tracing, and all LLM observability are NOT recording.

### 2. Seven SSH tunnels dead (exit 255)
All cross-machine tunnels are crashed and not recovering:

| Tunnel | Status |
|---|---|
| `com.clue.n8n-mcp-tunnel` | exit 255 |
| `com.clue.blitz-db-tunnel` | exit 255 |
| `com.dealiq.extractor-tunnel` | exit 255 — **documented as UNLOADED but still loaded** |
| `com.voxmaestro.tunnel` | exit 255 |
| `com.clue.runtime-tunnel` | exit 255 |
| `ai.openclaw.jneutron-tunnel` | exit 255 |
| `ai.openclaw.pg-tunnel` | exit 255 |
| `com.memory.ollama-tunnel` | exit 255 |

VPS connectivity is severed. n8n MCP, blitz DB access from Mac, VoxMaestro reverse tunnel, J-Neutron — all down.

### 3. Brain bind mismatch — exposed on all interfaces
- **Documented:** Plist sets `OPENCLAW_HOST=127.0.0.1`
- **Actual:** `lsof` shows brain listening on `*:8800` (all interfaces). The launch script or brain code overrides the plist env var. Brain is reachable from any network.

### 4. Outreach workflow IDs are LOCAL, not VPS — MEMORY.md is ambiguous
The 7 "disabled" workflow IDs (`6ZhZFeQGvTaQaw0u`, `uXFxLI9jXRtOrg6c`, etc.) **do not exist in VPS n8n**. They're local n8n workflows.

VPS has its own inactive outreach workflows with different IDs:
- `82ZKbxvRoPcA19Y9` — Vegas SMB
- `DZRiGYUXccTQECxv` — DealiQ Outreach
- `4fY25zUq4Cee79Yz` — Gentic Drip

MEMORY.md doesn't clarify which machine they're on.

---

## Active Issues (not in MEMORY.md)

### 5. Daily Summary Report failing daily
Workflow `poh35MI0YA0yqjIR` — error: `Node 'Query LLM Costs' hasn't been executed.` Failing since at least 2026-05-05. Undocumented.

### 6. Workflow Backup failing for 4 consecutive days
`iaVCWoEIgUJUEGTZ` — 4 failures since 2026-05-06. Daily backups are not happening.

### 7. `agent-orchestrator-qdrant-1` unhealthy on VPS
Separate from `governed-mcp-spine` Qdrant (which is healthy). Undocumented.

### 8. `spine-egress-proxy` unhealthy
Documented as known, VPS rebuild pending. Confirmed still down.

---

## Orphan / Undocumented Running Code

| Process | PID | Port | Notes |
|---|---|---|---|
| GBP scraper | 1147 + 3 Chromium | `:8855` (`*`) | Running 3 days. Outbound paused. Consuming resources for nothing. |
| accomplish-sandbox | 564 | – | Python 3.9, running since boot. No MEMORY.md entry. |
| ai.openclaw.guardian | loaded | – | Running but not explicitly documented as a service. |
| imessage-claude | exit 1 | – | Loaded, crashed, not recovering. |

---

## Security: Wide-Open Listeners

Bound to `*` (all interfaces) and reachable from any network if firewall allows:

| Service | Port | Should Be |
|---|---|---|
| Brain | `:8800` | `127.0.0.1` (plist says so, code ignores it) |
| Kokoro TTS | `:8880` | `127.0.0.1` (no reason for external access) |
| CE MLX | `:11436` | `127.0.0.1` or Tailscale IP |
| Ollama | `:11434` | `0.0.0.0` intentional (VPS relay), documented |
| GBP scraper | `:8855` | Should not be running at all |

---

## Orphan Data

| Location | Item | Notes |
|---|---|---|
| Mac Mini PG | `monthly_spend_pre_optiong_2026_05_04` | Backup table from Option G migration. Safe to drop. |
| VPS PG | `mcp` database (8 tables) | Legacy pre-migration tables overlap with `blitz`. Orphan. |
| VPS PG | `ceiba` database | Documented as ARCHIVED. Data persists. Expected. |
| VPS PG | `orchestrator` database | Not documented anywhere in MEMORY.md. |
| VPS PG | `apo` schema — 11 tables (not 10) | MEMORY.md says "skills + 10 others". Actual: 11 tables total. |
| Mac Mini PG | `apo` schema — 3 tables (not 2) | MEMORY.md boundary note says 2 (`baseline_metrics` + `skill_registry`). Phase 3 added `eval_runs`. |

---

## What Matches (confirmed good)

- Mac Mini uptime 3.5d
- All 6 Docker containers on Mac Mini up and healthy
- Ollama: 6 models, both VSAI v7 variants, both embedding models
- Jake correctly decommissioned — no port, no process, no model
- prop-enricher correctly Tailscale-bound (`100.122.223.120:7700`)
- VPS `governed-mcp-spine` stack: all services healthy (10d uptime)
- VPS KORA brain: healthy (6d uptime)
- VPS gentic-conversation: healthy (4d uptime)
- Mac Mini crontab: 11 entries, all correct (anomaly observer, drip-watch, APO baseline, skill sync, harvester, session janitor, federation drift)
- VPS crontab: 6 entries, all properly secretized post-sweep
- `clue_runtime` schema well-organized: 24 tables + governance/entity/policy/monitoring layers
- `blitz` schema: 14 schemas, 144 tables, RLS on shared/gentic tables, immutable audit log, proper role separation (`mcp`, `blitz_rw`, `blitz_ro`, `n8n_app`, `agent_worker`, `gentic_api`, `mcp_ro`)

---

## VPS n8n: Full Inventory (82 workflows, not 38)

### 57 active
9 Broker endpoints, 5 Chappie tools, 5 GAN components, 4 VSAI flows, 3 DealiQ enrichment, 2 Gentic pipeline webhooks (with auth hardening from F9), system monitoring, error handling, Smart AI Router, iRELOP scoring, and more.

### 25 inactive
All outreach-related flows (3 Broker call/voicemail, DealiQ outreach/nurture, Vegas SMB, Gentic drip/prospect sequence), all 3 CEIBA flows, legacy DealiQ pipelines, AEO scraper, and system resource monitor.

---

## Recommended Actions

### P0 — Fix now
1. Restart Langfuse container or diagnose crashloop (`docker logs langfuse --tail 50`)
2. Restart SSH tunnels (`~/bin/ssh-tunnel-clean` then `launchctl kickstart` each)
3. Kill GBP scraper — burning resources during outbound pause

### P1 — Fix this week
4. Fix brain bind — either fix `launch-brain.sh` to respect `OPENCLAW_HOST` or rebind to `127.0.0.1` in code
5. Rebind Kokoro TTS and CE MLX to `127.0.0.1`
6. Investigate Daily Summary Report + Workflow Backup failures on VPS
7. Unload `com.dealiq.extractor-tunnel` (documented as UNLOADED, actually still loaded)

### P2 — Housekeeping
8. Update MEMORY.md: apo boundary (3 tables Mac Mini, 11 VPS), outreach IDs are LOCAL not VPS, Langfuse status
9. Drop `monthly_spend_pre_optiong_2026_05_04` backup table
10. Assess `mcp` database and `orchestrator` database — migrate or archive
11. Document or kill `accomplish-sandbox`, `guardian`, `imessage-claude`

---

## Handoff Notes

- This document captures the audit performed by the parallel agents that had live access. The branch `claude/audit-system-drift-wnWYc` does **not** carry runtime credentials; P0/P1 fixes must be executed from the session that has Mac Mini + VPS access.
- Once P0 fixes land, append a "Post-fix verification" section here with the new state of: Langfuse container, the eight SSH tunnels, GBP scraper PID(s), and any MEMORY.md updates.
- MEMORY.md was referenced throughout the audit but does not exist in this monorepo. Confirm whether it lives in a separate repo or whether this monorepo is itself part of the documented drift.
