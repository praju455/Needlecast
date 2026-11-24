import { expect, test } from "@playwright/test";

for (const [path, heading, evidence] of [
  ["/", "Fraud detection workspace", "Sample test transactions"],
  ["/data", "Datasets", "Fraud by split"],
  ["/reduction", "Feature reduction", "Explained variance"],
  ["/scoring", "Transaction scoring", "Score transaction"],
  ["/comparison", "Model comparison", "Benchmark metrics"],
  ["/diagnostics", "Diagnostics", "Circuit register"],
  ["/roadmap", "Development roadmap", "Foundation and scaffold"],
]) {
  test(`shows ${path} with placeholder labels`, async ({ page }) => {
    await page.goto(path);
    await expect(page.getByRole("heading", { level: 1, name: heading })).toBeVisible();
    await expect(page.getByText("Placeholder data", { exact: true })).toBeVisible();
    await expect(page.getByText(evidence).first()).toBeVisible();
    if (path === "/scoring") {
      await page.getByRole("button", { name: "Pick a sample" }).click();
      await page.getByRole("button", { name: "Score transaction" }).click();
      await expect(page.getByRole("heading", { name: "Scoring trace" })).toBeVisible();
    }
  });
}
