# Public listing and submission checklist

## Repository release values prepared for a future directory submission

- Package name: `agentic-course-redesign`
- Version: `0.2.3` repository release and inactive universal-directory
  submission candidate; published `v0.2.2` remains rollback source
- Display name: `Agentic Course Redesign`
- Short description: `Gated evidence-led redesign`
- Category: `Education & Research`
- Repository: <https://github.com/gpochs/Agentic-Course-Redesign-System>
- Submission type: `Skills only`
- Skills: six
- Starter prompts: three
- Positive reviewer cases: nine
- Negative reviewer cases: eight
- MCP server, connector, UI, screenshots, authentication, and demo credentials:
  not applicable

Repository release `v0.2.3` uses matching exact-version archives, checksums,
inventories and validation evidence. The historical `v0.2.1` live release
reports `immutable=false`, and its attached
`system-release-validation-v0.2.1.json` internally identifies the earlier
v0.2.0 archive, so it must not be used as later-version archive evidence.
Any later OpenAI Platform upload must use an exact validated candidate archive
whose manifest, tests and release notes match. It must not infer directory
publication from the GitHub release.

## Owner-supplied blockers

Do not replace these markers with guesses. The verified owner must complete and
confirm each item before upload:

- [ ] `[VERIFIED_PUBLISHER_NAME]`: exact individual or business identity already
  verified in the OpenAI Platform. Update both `author.name` and
  `interface.developerName` to this confirmed value if it is not exactly
  `gpochs`.
- [ ] `[OPENAI_ORGANIZATION_AND_PROJECT]`: organization and project that own the
  verified identity and submission.
- [ ] `[APPS_MANAGEMENT_WRITE_SUBMITTER]`: person whose organization role has
  Apps Management set to Write.
- [ ] `[PUBLIC_WEBSITE_HTTPS_URL]`: public product or project website matching
  the verified publisher.
- [ ] `[PUBLIC_SUPPORT_HTTPS_URL]`: public support page with a real support
  process. No support email has been invented in this package.
- [ ] `[PUBLIC_PRIVACY_POLICY_HTTPS_URL]`: public policy that accurately explains
  local files, optional external research, data egress, and applicable services.
- [ ] `[PUBLIC_TERMS_HTTPS_URL]`: public terms matching the publisher and plugin.
- [ ] `[SUPPORTED_COUNTRIES_OR_REGIONS]`: locations where publisher, support,
  policies, and terms are ready.
- [ ] `[POLICY_ATTESTATION_OWNER]`: authorised person who has reviewed the final
  listing, skill tree, prompts, tests, availability, and attestations.

For skills-only upload validation, the four public URLs are optional manifest
fields. OpenAI's submission guide and final checklist nevertheless tell
submitters to provide public website, support, privacy, and terms URLs matching
the publisher. They are therefore omitted from this candidate manifest rather
than populated with invalid placeholder URLs, and treated as release blockers.

## Final owner actions

- [x] Preserve the published `v0.2.1` base, tag, assets and checksums unchanged.
- [x] Build and validate exact `v0.2.2` repository assets whose archive name,
  byte count and SHA-256 match their report; publish them with the matching tag.
- [x] Complete v0.2.3 validation and obtain separate commit and GitHub
  publication authorisation.
- [ ] Replace or confirm publisher fields in both custom and public manifests.
- [ ] Add the four verified HTTPS URLs to the final public manifest and portal.
- [ ] Run all local validators against the final file tree.
- [ ] Test the final ZIP in a supported local marketplace and a new chat.
- [ ] Create a Skills only draft in the OpenAI plugin submission portal.
- [ ] Upload the final bundle, prompts, tests, availability, and release notes.
- [ ] Wait for every skill safety/security scan to pass.
- [ ] Complete attestations only after checking the final draft.
- [ ] Submit for review; do not describe submission as publication.
- [ ] After approval, let the verified publisher choose when to publish.
- [ ] Verify the live universal-directory entry before making availability claims.
