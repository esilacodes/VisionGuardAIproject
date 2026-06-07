🛡️ VisionGuard AI
AI-Powered Security Camera System with Real-Time Human Detection
VisionGuard AI is a desktop security application that goes beyond simple motion detection. Built with YOLOv8 neural networks, it recognises actual humans — ignoring shadows, lighting changes, and background noise — and alerts you instantly when a restricted zone is breached.

Features

YOLOv8 Human Detection — detects people with confidence scoring, not just motion
Multi-Person Tracking — centroid tracker assigns unique IDs to each person across frames
Real-Time Heatmap — shows where people spend the most time, with time-decay fading
Restricted Zone System — draw custom zones on the feed, breach triggers instant alert
Night Vision (CLAHE) — adaptive contrast enhancement in LAB colour space for low light
AES-256 Encryption — all snapshots stored encrypted and LZMA compressed
Persistent Notifications — every alert saved to SQLite with timestamp and type
Telegram Alerts — photo and message sent to your Telegram on zone breach
Dark and Light Theme — full theme switching from the Settings page
User Accounts — register, login, change username and password, delete account


Project Structure
main.py — entry point
backend/camera.py — camera loop, YOLOv8, centroid tracker, heatmap, zone system
backend/database.py — SQLite for users, detections, notifications
backend/encryption.py — AES-256 CBC encryption and LZMA compression
backend/notifier.py — Telegram Bot API integration
backend/log_manager.py — system event logging
config/settings.py — colours, theme, global configuration
gui/login/login_page.py — login and register container
gui/login/login_tab.py — login form
gui/login/signin_tab.py — register form
gui/dashboard/dashboard_page.py — main dashboard with sidebar and all pages
gui/dashboard/settings_page.py — settings container
gui/dashboard/settings_tab.py — account, Telegram, appearance settings
gui/shared/components.py — reusable UI components
gui/shared/logs_viewer.py — system logs viewer widget
gui/shared/message_box.py — custom modal dialogs
logs/ — auto-generated log files
requirements.txt — Python dependencies
.env — Telegram credentials, not committed to version control

Installation
Step 1 — Clone the repository
git clone https://github.com/yourusername/visionguard-ai.git
cd visionguard-ai
Step 2 — Create a virtual environment
python -m venv venv
On Windows: venv\Scripts\activate
On macOS and Linux: source venv/bin/activate
Step 3 — Install dependencies
pip install -r requirements.txt
On first run, YOLOv8 automatically downloads the yolov8n.pt model weights (around 6 MB). An internet connection is required for the first launch only.
Step 4 — Set up Telegram (optional)
Create a .env file in the project root with the following content:
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
To get these values: open Telegram and search for @BotFather, send /newbot and follow the steps to receive your token. Then send any message to your bot and visit https://api.telegram.org/bot YOUR TOKEN HERE /getUpdates to find your chat_id in the response.
Step 5 — Run the application
python main.py

How to Use
Starting Detection: launch the app, create an account or log in, go to the Dashboard or Live page, then click Start. YOLOv8 begins detecting people immediately.
Drawing a Restricted Zone: make sure the camera is running, click Draw Zone in the control panel, then click and drag on the Live Feed to draw a rectangle. Anyone entering that area triggers a Zone Breach alert and a Telegram notification with a photo.
Overlays: enable Heatmap to see movement density where red means high traffic and blue means low. Enable Trajectories to draw movement paths for each tracked person. Enable Night Vision for CLAHE enhancement in low-light environments.
Settings: change your username or password, update your Telegram handle, test the Telegram connection with the built-in test button, and switch between Dark and Light theme.

Requirements
Python 3.10 or higher
customtkinter 5.2.0 or higher
opencv-python 4.8.0 or higher
Pillow 10.0.0 or higher
numpy 1.24.0 or higher
ultralytics 8.0.0 or higher
requests 2.31.0 or higher
cryptography 41.0.0 or higher
python-dotenv 1.0.0 or higher

Security and Privacy
All detection snapshots are encrypted with AES-256 CBC before being written to the database. Images are also LZMA compressed to reduce storage size. A unique initialisation vector is generated for every encryption operation so no two encrypted files are identical. The SQLite database is stored locally on your machine — there is no cloud, no external server, and no data leaves your device. Telegram credentials are stored in the .env file and are never committed to version control.

How the AI Works
Each camera frame is passed to the YOLOv8n neural network, which detects persons using class 0 from the COCO dataset. Detections below a 45 percent confidence threshold are discarded to minimise false alarms. The confirmed detections are passed to the centroid tracker, which computes the centre point of each bounding box and matches it to the nearest centre from the previous frame using Euclidean distance. This gives each person a stable ID that persists across frames. The tracker output is then checked against all defined restricted zones — if a person's centre point falls inside a zone rectangle, a breach is recorded. At the same time the heatmap accumulator adds to the density map in the bounding box area and multiplies by a decay factor each frame so old movements fade over time. When a breach is confirmed, the system saves an AES-256 encrypted snapshot to the database, stores a notification, and sends a photo alert to Telegram.

Pages Overview
Dashboard — camera feed with control panel and live statistics
Live — full-screen camera view with sensitivity slider
Records — all saved detections with encrypted snapshot viewer
Notifications — alert history with unread badge and filter by type
Logs — system event log viewer
Settings — account management, Telegram setup, theme switching
About — feature list, usage guide, technology stack

Technologies Used
Python 3.10 — core language
CustomTkinter — modern desktop GUI framework
OpenCV — camera capture, image processing, CLAHE night vision
YOLOv8 by Ultralytics — real-time human detection neural network
NumPy — heatmap density accumulation
SQLite3 — local database for users, detections, and notifications
cryptography library — AES-256 CBC encryption
LZMA — image compression before encryption
Pillow — image conversion between OpenCV and tkinter formats
requests — Telegram Bot API HTTP communication
python-dotenv — secure credential loading from .env file

License
This project is licensed under the MIT License.

Authors
Developed as an AI-assisted capstone project demonstrating real-time computer vision, secure local storage, and modern desktop GUI development with Python.

"Classical security systems detect motion. VisionGuard AI detects people."
