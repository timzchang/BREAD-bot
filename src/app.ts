import "dotenv/config";
import express from "express";
import {WebhookClient} from "discord.js";
import fs from "fs";
import path from "path";
import csv from "csv-parser";
import dedent from "dedent";
import {fileURLToPath} from "url";
import {CronJob} from "cron";

// Convert import.meta.url to a file path
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

type BreadRow = {
  date: string;
  link: string;
  season: string;
  theme: string;
  verse: string;
};
export function getTodaysVerse(callback: (row?: BreadRow) => void) {
  const today = new Date().toISOString().split("T")[0]; // Get today's date in YYYY-MM-DD format
  const csvFilePath = path.resolve(__dirname, "../lib/verses.csv");

  fs.createReadStream(csvFilePath)
    .pipe(csv())
    .on("data", (row) => {
      if (row.date === today) {
        console.log(row);
        callback(row);
      } else {
        callback();
      }
    })
    .on("end", () => {
      console.log("CSV file successfully processed");
    });
}

function getMessage(row?: BreadRow) {
  if (!row) {
    return dedent`
      Good Morning! 🌅 🕊️
      Today's reading is not available. 🙏
      Have a blessed Day! 🙌`;
  }
  const {link, season, theme, verse} = row;
  return dedent`
    Good Morning! 🌅 🕊️
    Let's take some time to be with the Lord in this season of ${season}. 🙏
    How to read BREAD:
    B - Be Still
    R - Read
    E - Encounter
    A - Apply
    D - Devote
    For more information, visit https://realitysf.com/wp-content/uploads/2024/01/BREAD-2024-Digital-Guide.pdf

    This week's theme is: ${theme}.
    Today's reading is from ${verse}: ${link}
    Have a blessed day! 🙌
  `;
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
CronJob.from({
  cronTime: "0 9 * * *",
  // cronTime: "*/5 * * * * *",  // for testing
  onTick: function () {
    getTodaysVerse((row) => {
      const message = getMessage(row);
      console.log(message);
      webhookClient
        .send(message)
        .then(() => console.log("Message sent successfully"))
        .catch(console.log);
    });
  },
  start: true,
  timeZone: "America/Los_Angeles",
});

app.get("/", (_, res) => {
  res.send("Express server with cron job is running!");
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
