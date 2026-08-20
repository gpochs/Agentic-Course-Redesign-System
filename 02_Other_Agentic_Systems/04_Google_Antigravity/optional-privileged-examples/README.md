# Optional privileged examples — inactive

Nothing in this folder is under `workspace-overlay/` or an Antigravity
auto-discovery path. The examples are documentation only and remain explicitly
disabled.

- `hooks.json.example` has top-level hook `enabled: false`.
- `mcp_config.json.example` has server `disabled: true` and all tools withheld.
- No plugin example is supplied because Google's current IDE plugin manifest
  documentation does not define a reliable disabled-by-default manifest field.

Do not rename, copy, install, or enable an example merely to make a capability
available. First complete a separate System Gate covering the exact file,
command/server, permissions, data egress, credentials handling, automatic
behaviour, risk, validation, and rollback. Keep credentials outside Git and the
course workspace.
