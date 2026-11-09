# aspace-rrsi-adapter

Adapter A'Space pour `rrsi` (Regularized Recursive Self-Improvement of
Agent Harnesses, Google Research) — gel `be50316`.

**Contrat seul** (§1.5) : aucune couture spécifique. La surface exposée est
le cœur pur de la méthode, hors-ligne :

- `rrsi.schedule.budget_table(T, b_min, b_max)` — ordonnancement des budgets
- `rrsi.config.RRSIConfig` — hyperparamètres (T=20, b_min=1, b_max=4)
- `rrsi.selection.select_round`, `rrsi.history.History`
- CLI : `python3 rrsi.py --help` / `status` (lecture seule)

**Jamais** : tout appel modèle (Claude sur Vertex AI), les domaines
`eng` / `workspace` (runners, passerelle MCP, socket locale), le tiers
`third_party/archipelago` (runners de benchmark, httpx), tout appel réseau.

**Télémétrie** : aucun SDK ; les occurrences du mot-clé sont des faux
positifs (segments de trajectoire / ELF) — voir
`rrsi-TELEMETRY-AUDIT.md`.

Smoke test : `pytest aspace-rrsi-adapter/smoke_test.py -q`
(5 tests, hors-ligne).
