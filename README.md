# odin_temporal

A standalone Odin package, `temporal`, for validated civil dates, local times,
local date-times, and fixed-offset date-times. It is allocation-free and has no
dependency outside Odin's core libraries.

The package deliberately does not parse or format application text, look up
time zones, infer a machine-local zone, or perform calendar arithmetic.
`UTC_Offset.Unknown` preserves an RFC 3339 `-00:00` offset without inferring
UTC.

## Check

The supported Odin compiler is pinned in [`toolchain/odin.lock`](toolchain/odin.lock).
With it on `PATH`, run:

```sh
scripts/check.sh
```

## Integration

This repository is consumed by `odin_toml` as the `vendor/temporal` git
submodule. Odin clients can import the package by a relative path or map it
into a collection.
