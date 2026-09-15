import { serve } from "@hono/node-server";
import { desc, eq } from "drizzle-orm";
import { Hono } from "hono";
import { z } from "zod";

import { db, initDb } from "./db/client.js";
import { tasks } from "./db/schema.js";

const app = new Hono();

const createTaskSchema = z.object({
  title: z.string().min(1).max(200),
});

const apiKey = process.env.API_KEY ?? "";

app.use("*", async (c, next) => {
  if (!apiKey || c.req.path === "/health") {
    return next();
  }

  const provided = c.req.header("x-api-key");
  if (provided !== apiKey) {
    return c.json({ error: "Invalid or missing X-API-Key header" }, 401);
  }

  return next();
});

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/tasks", async (c) => {
  const rows = await db.select().from(tasks).orderBy(desc(tasks.createdAt));
  return c.json(rows);
});

app.post("/tasks", async (c) => {
  const parsed = createTaskSchema.safeParse(await c.req.json());
  if (!parsed.success) {
    return c.json({ error: parsed.error.flatten() }, 400);
  }

  const [row] = await db
    .insert(tasks)
    .values({ title: parsed.data.title })
    .returning();

  return c.json(row, 201);
});

app.patch("/tasks/:id/complete", async (c) => {
  const id = Number(c.req.param("id"));
  if (Number.isNaN(id)) {
    return c.json({ error: "Invalid task id" }, 400);
  }

  const [row] = await db
    .update(tasks)
    .set({ status: "done" })
    .where(eq(tasks.id, id))
    .returning();

  if (!row) {
    return c.json({ error: "Task not found" }, 404);
  }

  return c.json(row);
});

await initDb();

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port, hostname: "0.0.0.0" });
console.log(`Hono API listening on port ${port}`);
