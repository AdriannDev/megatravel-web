import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { expect, test } from "vitest";
import AdminPage, { metadata } from "./page";

test("renders the CMS heading and disables indexing", () => {
  const html = renderToStaticMarkup(<AdminPage />);

  expect(html).toContain("<h1>CMS</h1>");
  expect(metadata.robots.index).toBe(false);
});
