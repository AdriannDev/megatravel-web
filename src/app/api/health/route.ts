import { sql } from "drizzle-orm";
import { connection } from "next/server";
import { getDb } from "../../../db/client";

export async function GET() {
  await connection();

  try {
    await getDb().execute(sql`select 1`);
    return new Response(null, { status: 200 });
  } catch {
    return new Response(null, { status: 503 });
  }
}
