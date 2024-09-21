import "dotenv/config";
import express from "express";
import { WebhookClient } from "discord.js";
import cron from "node-cron";
// import { DiscordRequest } from "../utils";
const app = express();
const port = process.env.PORT || 3000;
const url = process.env.WEBHOOK_URL;
if (!url) {
    console.error("Webhook URL is required");
    process.exit(1);
}
// Initialize the WebhookClient with the webhook URL
const webhookClient = new WebhookClient({ url });
// Schedule a task to run every day at 9:00 AM
cron.schedule("* * * * * *", () => {
    webhookClient
        .send("Good morning! Here is your daily message.")
        .then(() => console.log("Message sent successfully"))
        .catch(console.error);
});
app.get("/", (req, res) => {
    res.send("Express server with cron job is running!");
});
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
