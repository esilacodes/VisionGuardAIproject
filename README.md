🛡️ VisionGuard AI

AI-Powered Security Camera System with Real-Time Human Detection

VisionGuard AI is a desktop security application that goes beyond simple motion detection. Built with YOLOv8 neural networks, it recognises actual humans — ignoring shadows, lighting changes, and background noise — and alerts you instantly when a restricted zone is breached.

📸 Features
FeatureDescription🤖 YOLOv8 Human DetectionDetects people with confidence scoring — not just motion🔁 Multi-Person TrackingCentroid tracker assigns unique IDs to each person🌡️ Real-Time HeatmapShows where people spend the most time (with time-decay)🚧 Restricted Zone SystemDraw custom zones on the feed — breach triggers instant alert🌙 Night Vision (CLAHE)Adaptive contrast enhancement in LAB colour space🔐 AES-256 EncryptionAll snapshots stored encrypted + LZMA compressed🔔 Persistent NotificationsEvery alert saved to SQLite with timestamp and type✈️ Telegram AlertsPhoto + message sent to your Telegram on zone breach🎨 Dark / Light ThemeFull theme switching from Settings👤 User AccountsRegister, login, change username/password, delete account

📁 Project Structure
VisionGuard AI/
│
├── main.py                         # Entry point
│
├── backend/
│   ├── camera.py                   # Camera loop, YOLOv8, tracker, heatmap, zones
│   ├── database.py                 # SQLite — users, detections, notifications
│   ├── encryption.py               # AES-256 CBC + LZMA encrypt/decrypt
│   ├── notifier.py                 # Telegram Bot API integration
│   └── log_manager.py              # System event logging
│
├── config/
│   └── settings.py                 # Colours, theme, global config
│
├── gui/
│   ├── login/
│   │   ├── login_page.py           # Login/Register container
│   │   ├── login_tab.py            # Login form
│   │   └── signin_tab.py           # Register form
│   │
│   ├── dashboard/
│   │   ├── dashboard_page.py       # Main dashboard (sidebar + all pages)
│   │   ├── settings_page.py        # Settings container
│   │   └── settings_tab.py         # Account, Telegram, Appearance settings
│   │
│   └── shared/
│       ├── components.py           # Reusable UI components
│       ├── logs_viewer.py          # System logs viewer widget
│       └── message_box.py          # Custom modal dialogs
│
├── logs/                           # Auto-generated log files
├── requirements.txt
└── .env                            # Telegram credentials (not committed)

⚙️ Installation
1. Clone the repository
bashgit clone https://github.com/yourusername/visionguard-ai.git
cd visionguard-ai
2. Create a virtual environment (recommended)
bashpython -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt

On first run, YOLOv8 automatically downloads the yolov8n.pt model weights (~6 MB). An internet connection is required for the first launch only.

4. Set up Telegram (optional)
Create a .env file in the project root:
envTELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
To get these:

Open Telegram and search for @BotFather
Send /newbot and follow the steps to get your token
Send any message to your bot, then visit:
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
Find your chat_id in the JSON response

5. Run the application
bashpython main.py

🚀 How to Use
Starting Detection

Launch the app and create an account or log in
Go to the Dashboard or Live page
Click ▶ Start — YOLOv8 begins detecting people immediately

Drawing a Restricted Zone

Make sure the camera is running
Click ✏ Draw Zone in the control panel
Click and drag on the Live Feed canvas to draw a rectangle
Anyone entering that area triggers a Zone Breach alert + Telegram notification

Overlays

🌡 Heatmap — Shows movement density (red = high traffic, blue = low)
🔁 Trajectories — Draws movement paths for each tracked person
🌙 Night Vision — CLAHE enhancement for low-light environments

Settings

Change username or password
Update Telegram handle
Test Telegram connection with the built-in test button
Switch between Dark and Light theme


🔧 Requirements
Python          3.10+
customtkinter   >= 5.2.0
opencv-python   >= 4.8.0
Pillow          >= 10.0.0
numpy           >= 1.24.0
ultralytics     >= 8.0.0
requests        >= 2.31.0
cryptography    >= 41.0.0
python-dotenv   >= 1.0.0

🔐 Security & Privacy

All detection snapshots are encrypted with AES-256 CBC before being written to the database
Images are also LZMA compressed to reduce storage size
A unique IV (initialisation vector) is generated for every encryption operation
The SQLite database file is stored locally — no cloud, no external servers
Telegram credentials are stored in .env and never committed to version control


🧠 How the AI Works
Camera Frame
     │
     ▼
┌─────────────────────────────┐
│  YOLOv8n Neural Network     │  ← detects persons (class 0)
│  confidence threshold: 45%  │  ← ignores low-confidence detections
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  Centroid Tracker           │  ← assigns stable IDs across frames
│  Euclidean distance match   │  ← links same person between frames
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  Zone Checker               │  ← checks if person centre is inside zone
│  Heatmap Accumulator        │  ← adds to density map with time-decay
└─────────────────────────────┘
     │
     ▼
┌─────────────────────────────┐
│  Alert + Save + Notify      │  ← encrypt snapshot, save to DB, send Telegram
└─────────────────────────────┘

📋 Pages Overview
PageDescriptionDashboardCamera feed + control panel + live statsLiveFull-screen camera with sensitivity sliderRecordsAll saved detections with encrypted snapshot viewerNotificationsAlert history with unread badge, filter by typeLogsSystem event log viewerSettingsAccount management, Telegram setup, themeAboutFeature list, usage guide, tech stack

🛠️ Technologies Used
TechnologyPurposePython 3.10+Core languageCustomTkinterModern GUI frameworkOpenCVCamera capture, image processing, CLAHEYOLOv8 (ultralytics)Real-time human detectionNumPyHeatmap accumulationSQLite3Local database for users, detections, notificationscryptographyAES-256 CBC encryptionLZMAImage compression before encryptionPillowImage conversion between OpenCV and tkinterrequestsTelegram Bot API communicationpython-dotenvSecure credential loading from .env

📄 License
This project is licensed under the MIT License.

👨‍💻 Authors
Developed as an AI-assisted capstone project demonstrating real-time computer vision, secure local storage, and desktop GUI development with Python.


"Classical security systems detect motion. VisionGuard AI detects people."
