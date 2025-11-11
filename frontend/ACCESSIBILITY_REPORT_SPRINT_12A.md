Accessibility Scan Report - Sprint 12-A (Automated checklist and remediation suggestions)

Scope: Trust & Transparency pages and components added in Sprint 12-A

Automated checks (recommend running axe or Lighthouse locally):
- Color contrast: Ensure text meets 4.5:1 for normal text and 3:1 for large text.
- Focus order: All interactive elements reachable via keyboard tab order.
- Landmark roles: Header, main, nav, aside elements present for screen readers.
- Form labels: Inputs must have associated labels or aria-label attributes.
- Images: All informative images must have alt text; decorative images should have empty alt attributes.
- Buttons: Use <button> elements for actions; links for navigation.
- Semantic headings: Page headings (h1..h3) used sequentially.

Manual checks and remediation suggestions:
1. Keyboard navigation: Verify modal focus trap in DeleteOrgConfirmModal. If focus leaks, implement focus-trap library or React focus management.
2. Color contrast: Update Tailwind color tokens if contrast fails in dark mode (e.g., increase text brightness or background darkness).
3. Skip link: Add a "Skip to content" link for keyboard users.
4. Live regions: Use aria-live for status messages (e.g., deletion request status updates).
5. Table semantics: Add scope='col' to table headers and ensure table has caption if needed.
6. Accessible forms: Ensure inputs have associated labels and error messages are connected via aria-describedby.
7. Responsive text sizing: Verify zoom 200% doesn't break layout.

Follow-up actions to automate:
- Integrate axe-core in CI to run accessibility checks on critical pages.
- Run manual usability tests with screen reader (NVDA / VoiceOver).

Estimated effort to remediate any issues: 2-8 hours depending on findings. I can help implement fixes if you want me to run an a11y pass next.


Automated axe-playwright guidance:
- Run `cd e2e && npm ci && node axe-test.js` to perform local accessibility scan against /trust.
- Reports are written to e2e/axe-report.json when violations are found.
