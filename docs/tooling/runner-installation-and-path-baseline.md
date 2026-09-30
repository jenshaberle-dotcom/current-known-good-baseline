# RCC General-Pool Runner Baseline

Status: current-known-good mandatory portfolio baseline  
Control ID: CKGB-RUNNER-POOL-002  
Owner: Runner Control Center (RCC)

## Purpose

The portfolio has one physical CI/workload runner architecture: the RCC General Pool.

Every project other than RCC is a consumer. A project may define what a workload needs, but it must not define which physical runner exists, how many pool members exist, how a runner is registered, or how runner lifecycle is managed.

## Authority split

### RCC owns

- General Linux / General Windows physical fleet identity;
- current pool `desired_count` and scale/reconcile;
- physical registration/service/listener lifecycle;
- repository-facade fanout;
- atomic reservation and exact assignment;
- runtime/profile materialization;
- capability overlays;
- qualification and clean-state proof;
- recovery and retirement.

### Consumer repositories own

- workload identity;
- required platform;
- runtime/dependency requirements;
- required capabilities;
- bounded parallelism semantics;
- exact source/workflow contract;
- product/effect semantics.

Consumers must be cardinality-blind.

## Baseline vs capability overlays

Keep the common fleet baseline deliberately small.

PowerShell 7 is a fleet baseline capability where RCC/workload architecture requires it and must be qualified from the same execution identity used by CI.

Everything that is not genuinely common is provisioned by RCC as a prepackaged/content-addressed capability overlay. Examples include:

- Kaggle CLI and authenticated provider binding;
- Godot and export templates;
- alternate Python versions;
- Azure CLI and Bicep;
- Docker;
- .NET SDK variants;
- project dependency environments.

A capability requirement does not create a specialist runner class.

## Forbidden consumer authority

Active consumer code, workflows, tests, current docs and Re-Entry state must not contain:

- project-owned physical runner inventories;
- project `desired_count`, `min_active`, `max_active` for physical capacity;
- project runner profiles as host truth;
- static facade/member lists;
- fixed pool ordinals or cardinality regexes;
- warm-runner heartbeat routing;
- GitHub-hosted fallback as a normal route;
- broad project labels that bypass RCC reservation;
- project-side runner start/stop/register/deregister logic;
- host-specific tool installation used to manufacture a specialist runner.

## Workload transaction

```text
consumer Demand-v2
  -> RCC validates repository + exact source/workflow
  -> RCC resolves platform/runtime/capabilities
  -> RCC materializes and qualifies required capabilities
  -> RCC selects free General-Pool capacity
  -> atomic reservation
  -> exact repository facade
  -> ephemeral assignment
  -> exact-source workload
  -> result verification
  -> deterministic cleanup
  -> reservation release
```

Missing capacity/capability is an explicit RCC execution state. It must not silently fall back to a retired project runner or hosted runner.

## Migration and retirement

A migration is complete only after real replacement proof and hard retirement:

```text
inventory old authority
-> introduce Demand-v2 replacement
-> prove exact General-Pool workload
-> prove no active reservation/work
-> drain old routing
-> stop/deregister old runner
-> verify registration removal
-> remove obsolete service/root when safe
-> delete old code/workflows/docs/issues
-> prove absence with regression guards
```

No blind deletion and no `--replace`.

Historical evidence may remain only when it is structurally non-executable and clearly classified as history.

## Specialist exception

A specialist physical runner is exceptional. It requires a written technical proof that the workload cannot be implemented safely/correctly through:

`General Pool + RCC baseline + content-addressed capability overlay`.

Existing labels, local paths, convenience, setup time or historical configuration are not sufficient evidence.

## Portfolio regression rule

New projects start Demand-v2-only. Existing active projects migrate to this baseline and physically retire superseded runners. A change that reintroduces a second runner architecture is a regression and must fail CI.
