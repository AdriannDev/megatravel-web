import { afterAll, beforeAll, expect, test, vi } from "vitest";
import { getDb } from "../../../db/client";
import { GET } from "./route";

vi.mock("next/server", () => ({ connection: async () => {} }));

const testDatabaseUrl = process.env.TEST_DATABASE_URL;
if (!testDatabaseUrl) {
  throw new Error("TEST_DATABASE_URL is required for database tests");
}

beforeAll(() => {
  vi.stubEnv("DATABASE_URL", testDatabaseUrl);
});

afterAll(async () => {
  try {
    await getDb().$client.end();
  } finally {
    vi.unstubAllEnvs();
  }
});

test("returns 200 when PostgreSQL responds", async () => {
  const response = await GET();

  expect(response.status).toBe(200);
  expect(await response.text()).toBe("");
});

test("returns 503 without exposing the database error", async () => {
  vi.spyOn(getDb(), "execute").mockRejectedValueOnce(new Error("database error"));

  const response = await GET();

  expect(response.status).toBe(503);
  expect(await response.text()).toBe("");
});
