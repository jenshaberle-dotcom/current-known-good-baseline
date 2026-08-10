#!/usr/bin/env bash
set -euo pipefail

release="${GODOT_RELEASE:-4.7.1-stable}"
expected="${GODOT_EXPECTED_VERSION:-4.7.1.stable.official.a13da4feb}"
root="${NOVI_RUNNER_TOOLCHAIN_ROOT:-${HOME}/.cache/NOVI/RunnerToolchain}"
cache_root="${root}/Cache/Godot/${release}"
install_root="${root}/Godot/${release}"
lock_root="${root}/Locks"
lock_dir="${lock_root}/godot-${release}.lock"
release_root="https://github.com/godotengine/godot/releases/download/${release}"
archive_name="Godot_v${release}_linux.x86_64.zip"
archive="${cache_root}/${archive_name}"
sums="${cache_root}/SHA512-SUMS.txt"

mkdir -p "$cache_root" "$lock_root"

cleanup_lock() {
  rmdir "$lock_dir" 2>/dev/null || true
}

for _ in $(seq 1 60); do
  if mkdir "$lock_dir" 2>/dev/null; then
    trap cleanup_lock EXIT
    break
  fi
  sleep 2
done
if [[ ! -d "$lock_dir" ]]; then
  echo "Timed out waiting for NOVI Linux toolchain lock: $lock_dir" >&2
  exit 1
fi

find_godot() {
  find "$install_root" -maxdepth 1 -type f -name 'Godot_*_linux.x86_64' -print -quit 2>/dev/null || true
}

binary="$(find_godot)"
if [[ -n "$binary" ]] && [[ -x "$binary" ]]; then
  version="$($binary --version | tr -d '\r\n')"
  if [[ "$version" == "$expected" ]]; then
    echo "NOVI Linux runner toolchain HIT: $binary"
    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
      echo "status=HIT" >> "$GITHUB_OUTPUT"
      echo "godot=$binary" >> "$GITHUB_OUTPUT"
      echo "root=$root" >> "$GITHUB_OUTPUT"
    fi
    exit 0
  fi
fi

echo "NOVI Linux runner toolchain REPAIR required."
curl --fail --location --silent --show-error --connect-timeout 30 --max-time 120 --retry 3 --retry-delay 2 \
  "$release_root/SHA512-SUMS.txt" --output "$sums"

expected_hash="$(grep "  ${archive_name}$" "$sums" | awk '{print toupper($1)}')"
if [[ -z "$expected_hash" ]]; then
  echo "No SHA-512 entry for $archive_name" >&2
  exit 1
fi

needs_download=1
if [[ -f "$archive" ]]; then
  actual_hash="$(sha512sum "$archive" | awk '{print toupper($1)}')"
  if [[ "$actual_hash" == "$expected_hash" ]]; then
    needs_download=0
    echo "CACHE HIT verified archive: $archive_name"
  fi
fi

if [[ $needs_download -eq 1 ]]; then
  partial="${archive}.partial"
  rm -f "$partial"
  curl --fail --location --silent --show-error --connect-timeout 30 --max-time 600 --retry 3 --retry-delay 2 \
    "$release_root/$archive_name" --output "$partial"
  actual_hash="$(sha512sum "$partial" | awk '{print toupper($1)}')"
  if [[ "$actual_hash" != "$expected_hash" ]]; then
    rm -f "$partial"
    echo "SHA-512 mismatch for $archive_name" >&2
    exit 1
  fi
  mv -f "$partial" "$archive"
fi

staging="${root}/Staging/Godot-$(date +%s)-$$"
rm -rf "$staging"
mkdir -p "$staging"
unzip -q "$archive" -d "$staging"
staged_binary="$(find "$staging" -maxdepth 1 -type f -name 'Godot_*_linux.x86_64' -print -quit)"
chmod +x "$staged_binary"
version="$($staged_binary --version | tr -d '\r\n')"
if [[ "$version" != "$expected" ]]; then
  echo "Godot version mismatch. Expected '$expected', got '$version'." >&2
  exit 1
fi

rm -rf "$install_root"
mkdir -p "$(dirname "$install_root")"
mv "$staging" "$install_root"
binary="$(find_godot)"
chmod +x "$binary"

echo "NOVI Linux runner toolchain REPAIR complete: $binary"
if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "status=REPAIR" >> "$GITHUB_OUTPUT"
  echo "godot=$binary" >> "$GITHUB_OUTPUT"
  echo "root=$root" >> "$GITHUB_OUTPUT"
fi
