import "dotenv/config";
import express from "express";
import {WebhookClient} from "discord.js";
import cron from "node-cron";
import fs from "fs";
import path from "path";
import csv from "csv-parser";
import {fileURLToPath} from "url";

// Convert import.meta.url to a file path
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function getTodaysVerse(
  callback: (verse: string, link: string) => void
) {
  const today = new Date().toISOString().split("T")[0]; // Get today's date in YYYY-MM-DD format
  const csvFilePath = path.resolve(__dirname, "../assets/verses.csv");

  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on("data", (row) => {
      if (row.date === today) {
        console.log(row);
        callback(row.verse, row.link);
      }
    })
    .on("end", () => {
      console.log("CSV file successfully processed");
    });
}

const app = express();
const port = process.env.PORT || 3000;

const url = process.env.WEBHOOK_URL;
if (!url) {
  console.error("Webhook URL is required");
  process.exit(1);
}
// Initialize the WebhookClient with the webhook URL
const webhookClient = new WebhookClient({url});

// Schedule a task to run every day at 9:00 AM
// cron.schedule("0 9 * * *", () => {
// for testing
cron.schedule("*/5 * * * * *", () => {
  getTodaysVerse((verse, link) => {
    webhookClient
      .send(`Today's Bread Reading is ${verse}: ${link}`)
      .then(() => console.log("Message sent successfully"))
      .catch(console.log);
  });
});

app.get("/", (req, res) => {
  res.send("Express server with cron job is running!");
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
