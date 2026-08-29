# Source Policy

`wiki/sources.md` declares external read-only roots. It contains exactly one fenced `json` block with an array of three-key objects:

```json
[
  {
    "alias": "archive",
    "root": "/absolute/path/to/read-only-source",
    "access": "read-only"
  }
]
```

An empty array is valid. Aliases match `^[a-z0-9]+(?:-[a-z0-9]+)*$` and are unique. `root` is absolute; `access` is exactly `read-only`. Unknown, missing, or duplicate keys, malformed JSON, duplicate aliases, or another access value invalidate the whole external policy.

An external reference uses `<alias>: <relative-posix-path>`. The selected root must exist as a real nonsymlink directory, and the resolved file must remain within it. Missing unused roots do not block workspace sources or another alias.

The guard rejects sensitive filenames, symlink traversal, unsupported extensions, unrepresentable references, and files over its size limit. It resolves and hashes active sources before and after editing. Keep absolute roots in local configuration and out of published package metadata.
