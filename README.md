# Webhook Receiver – webhook-repo

This Flask app receives GitHub webhooks for Push, Pull Request, and Merge events, stores them in MongoDB, and displays them via a minimal UI that refreshes every 15 seconds.

## Setup Instructions

1. Install dependencies:
2. Run MongoDB locally.
3. Start the Flask app:
4. Add the webhook endpoint (`/webhook`) to your GitHub repo (action-repo).
5. Access the UI at `http://localhost:5000`
