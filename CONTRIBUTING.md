# Contributing

Contributions are welcome when they preserve the lecturer-in-the-loop design
and data boundary.

1. Open an issue describing the course-independent problem.
2. Change the shared core before changing a platform adapter.
3. Use synthetic fixtures only.
4. Add or update validation that would catch the regression.
5. Run all public scrub, unit, adapter and package checks.
6. Document platform-specific claims with current official sources and label
   anything not exercised in a real client.

Never submit real course material to this public repository. That includes
institution-internal or restricted content, private-subscription content,
copyrighted source text, assessment or answer-key content, personal data,
local absolute paths, credentials, generated caches and enabled runtime state.
Use synthetic fixtures even when a lecturer would be authorised to process the
real material in a private, approved runtime.
