import { drizzle } from "drizzle-orm/node-postgres";

let db: ReturnType<typeof drizzle> | undefined;

export function getDb() {
  if (db) return db;

  const connectionString = process.env.DATABASE_URL;
  if (!connectionString) {
    throw new Error("DATABASE_URL is required");
  }

  db = drizzle({
    connection: { connectionString, connectionTimeoutMillis: 3_000 },
  });
  db.$client.on("error", () => console.error("PostgreSQL idle connection error"));
  return db;
}
