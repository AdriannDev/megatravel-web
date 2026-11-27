import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { expect, test } from "vitest";
import HomePage from "./page";

test("renders the public page heading and description in Spanish", () => {
  const html = renderToStaticMarkup(<HomePage />);

  expect(html).toContain('<h1 class="font-bold">Megatravel</h1>');
  expect(html).toContain("<p>Programas de viaje.</p>");
});
