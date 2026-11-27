import type { Metadata } from "next";
import React from "react";

export const metadata = {
  robots: { index: false },
} satisfies Metadata;

export default function AdminPage() {
  return (
    <main>
      <h1>CMS</h1>
    </main>
  );
}
