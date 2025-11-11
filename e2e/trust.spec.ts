// e2e/trust.spec.ts
const { test, expect } = require('@playwright/test');
test('public trust page loads', async ({ page }) => {
  await page.goto('http://localhost:3000/trust');
  await expect(page.getByText('Trust Center')).toBeVisible();
});
