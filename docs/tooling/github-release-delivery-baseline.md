# GitHub Release Delivery Baseline

Status: current-known-good conditional baseline
Control ID: CKGB-RELEASE-GITHUB-001
Origin: RCC + JAP real Windows application delivery work

## When to select

Select this profile for a versioned application or distributable artifact when GitHub is the canonical source repository and consumers need an install/update path that is independent of a source checkout.

It extends the release-management core in `docs/ckgb/architecture_lifecycle.md`.

## Core invariant

A published release is one immutable identity:

```text
repository_id
+ exact source SHA
+ VERSION
+ release tag
+ release manifest
+ release asset set
+ asset digest(s)
+ publisher identity where applicable
```

A release is not merely "a ZIP with a version name".

## Canonical flow

For a Windows/local application, the proven pattern is:

```text
VERSION on exact source
  -> CI/source qualification
  -> self-contained platform publish
  -> privileged/local signing if required
  -> signature + manifest + checksum verification
  -> staged runtime probe
  -> immutable GitHub Release/tag publication
  -> consumer download
  -> consumer verification
  -> staged install/update probe
  -> atomic/same-volume swap
  -> rollback on failure
  -> installed-version/runtime verification
```

Not every project requires Authenticode or a local publisher broker. The identity, checksum, staging and rollback concepts remain applicable.

## `gh` release-management contract

Use GitHub CLI inside a bounded release workflow/broker, not as an ad-hoc operator convention.

A qualified publisher should use operations equivalent to:

```text
gh release view <tag> --repo <repo>
gh api repos/<repo>/commits/<tag> --jq .sha
gh release create <tag> <assets...> --repo <repo> --target <exact-sha> ...
gh release view <tag> --repo <repo> --json assets
```

### Before `gh release create`

Verify at minimum:

- expected repository and immutable repository ID;
- checkout HEAD equals the intended release source;
- worktree is clean;
- version files agree;
- tag is deterministic from version;
- existing tag/release is either absent or resolves to the same exact source;
- a pre-existing release contains the complete required asset set;
- package digest matches the checksum sidecar/manifest;
- signatures/publisher identity are valid where required;
- runtime/package qualification has passed.

### Publication

Publish the tag against the exact source SHA using `--target <exact-sha>`. After publication, resolve the tag again and verify it still maps to that source. Re-read the release asset list and require all contract assets.

### Idempotency

If the immutable release already exists with the exact expected source and complete exact asset contract, classify it as already published rather than creating a second equivalent release.

If the tag exists but resolves to another source, fail closed. Do not retarget an immutable published version to make the pipeline pass.

## Artifact contract

A release package should normally include or accompany:

- platform/package artifact;
- SHA-256 sidecar or equivalent digest ledger;
- machine-readable release manifest with repository ID, source SHA, version and tag;
- updater/swap components needed by the consumer, when applicable;
- signer/publisher identity and per-file hashes when signing is part of the profile.

RCC currently publishes:

- `RCC-Control-Center-win-x64.zip`
- `RCC-Control-Center-win-x64.zip.sha256`

Its package embeds `RCC-RELEASE.json` and signed update/swap components.

## Publisher authority boundary

GitHub `contents: write` is publication authority, not automatically private-key/signing authority or privileged host authority.

Where signing requires a host-local publisher identity:

1. CI binds a request to exact repository ID/source/version/tag;
2. a narrowly scoped local publisher broker performs signing/package proof;
3. the broker returns proven assets and evidence, but no GitHub publication authority;
4. CI independently verifies the returned identity, signatures, hashes and manifest;
5. only then does CI perform `gh release create`.

This keeps the signing key out of normal CI while keeping publication auditable and exact-source bound.

## Consumer update contract

Routine updates must consume a release, not recreate one.

The consumer should:

1. discover only eligible non-draft/non-prerelease tags for its release namespace;
2. resolve exact repository/release identity;
3. download the exact expected assets;
4. verify SHA-256 and manifest;
5. verify signer/publisher where applicable;
6. extract to staging outside the live install directory;
7. perform a staged runtime/probe check;
8. perform an atomic/same-volume swap;
9. preserve rollback until the new install is proven;
10. record installed provenance/version.

The normal consumer must not clone source, invoke the SDK/compiler or sign release binaries merely to update an application.

## Transitional installer

An explicit installer may remain necessary for:

- first installation;
- migration from a legacy version that predates self-update;
- recovery when no trustworthy installed updater remains.

The transitional installer should still consume exact release assets where practical and must not become a second uncontrolled release channel.

Current evidence examples:

- JAP: `install-jap-control-center.ps1`, normally entered from WSL via `scripts/install_jap_windows_control_center.sh`;
- RCC: `install-rcc-control-center.ps1` for the transition/install path; `tools/windows/Build-Install-RccLocal.ps1` remains a developer/local build-install helper and is not the routine consumer update model.

## Release and host truth stay separate

A GitHub Release proves the release ledger and downloadable artifact identity. It does not by itself prove:

- the artifact was installed on a particular machine;
- the previous process was safely stopped;
- local user/runtime state was preserved;
- the new runtime launched successfully;
- a privileged mutation was authorized.

Local-app and privileged-control-plane profiles therefore add installation/runtime proof after release publication.

## Failure rules

Fail closed on:

- repository ID mismatch;
- source/tag/version mismatch;
- dirty release checkout;
- incomplete existing immutable release;
- changed or invalid checksum;
- release manifest identity mismatch;
- invalid signer/publisher identity when required;
- failed staged runtime probe;
- inability to preserve a safe rollback path before live replacement.

Do not treat a publication failure as permission to build or sign on the consumer machine.

## Evidence origins

RCC current main contains:

- `docs/releases/RCC-GITHUB-RELEASE-PROTOCOL-v1.md`;
- `.github/workflows/rcc-github-release-sync.yml`;
- `tools/windows/New-RccGitHubReleasePackage.ps1`;
- `tools/windows/Install-RccReleasePublisherBroker.ps1`;
- `tools/windows/Rcc-ReleasePublisherBroker.ps1`;
- `tools/windows/Rcc-StableSwap.ps1`;
- `tools/windows/Update-RccLocal.ps1`.

The RCC workflow performs exact source/version/tag checks, verifies existing immutable releases, consumes signed broker output, re-verifies signatures/hashes/manifest, invokes `gh release create ... --target <source>` and verifies the resulting tag/assets.

JAP current main tests and installer additionally prove the same core model with a self-contained Windows artifact, release checksum, `gh release create`, staged installation and rollback.
