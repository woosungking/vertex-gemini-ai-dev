"""
가상의 회사 "넥스트테크(NextTech)" 제품 매뉴얼 PDF 4개 생성
"""

from fpdf import FPDF
import os

OUTPUT_DIR = "sample_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MARGIN = 15


class ManualPDF(FPDF):
    def __init__(self, title):
        super().__init__()
        self.doc_title = title
        self.set_margins(MARGIN, MARGIN, MARGIN)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_fill_color(30, 80, 160)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"  NextTech Co., Ltd.  |  {self.doc_title}", fill=True, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"NextTech Co., Ltd. | Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(220, 230, 245)
        self.cell(0, 9, f"  {title}", fill=True, ln=True)
        self.ln(2)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(30, 80, 160)
        self.cell(0, 7, title, ln=True)
        self.set_text_color(0, 0, 0)

    def body(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_x(MARGIN)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullets(self, items):
        self.set_font("Helvetica", "", 10)
        self.set_x(MARGIN)
        for item in items:
            self.set_x(MARGIN)
            self.multi_cell(0, 6, f"  - {item}")
        self.ln(2)


# ============================================================
# PDF 1: NT-S100 스마트 스피커
# ============================================================
def create_pdf1():
    pdf = ManualPDF("NT-S100 Smart Speaker Manual")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "NT-S100 Smart Speaker", align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, "User Manual v2.1  |  NextTech Co., Ltd.", align="C", ln=True)
    pdf.ln(5)

    pdf.chapter_title("1. Product Overview")
    pdf.body("The NT-S100 is NextTech's flagship smart speaker featuring 360-degree surround sound, built-in AI assistant, and seamless smart home integration. With a 4-inch woofer and dual tweeters, it delivers rich, room-filling audio.")
    pdf.section_title("Key Specifications")
    pdf.bullets([
        "Dimensions: 148mm (H) x 99mm (D)",
        "Weight: 1.36 kg",
        "Connectivity: Wi-Fi 6, Bluetooth 5.2, 3.5mm AUX",
        "Power: 30W (15W woofer + 2x7.5W tweeters)",
        "Supported formats: AAC, MP3, FLAC, WAV, OGG",
    ])

    pdf.chapter_title("2. Setup & Installation")
    pdf.section_title("2.1 Initial Setup")
    pdf.body("1. Place the NT-S100 on a flat, stable surface at least 20cm away from walls.\n2. Connect the power adapter to the DC IN port on the back.\n3. Download the NextTech Home app from the App Store or Google Play.\n4. Open the app and tap 'Add Device' > 'NT-S100'.\n5. Follow the on-screen instructions to connect to your Wi-Fi network.")
    pdf.section_title("2.2 Voice Assistant Activation")
    pdf.body("Say 'Hey NextTech' to activate the voice assistant. The LED ring will turn blue when the assistant is listening. You can change the wake word in the app under Settings > Voice > Wake Word.")

    pdf.chapter_title("3. Controls & Indicators")
    pdf.section_title("Top Panel Controls")
    pdf.bullets([
        "Volume +/-: Adjust speaker volume",
        "Mic Mute: Toggle microphone on/off (LED turns red when muted)",
        "Action Button: Activate assistant / pause/resume playback",
        "Power: Long press 3 seconds to power off",
    ])
    pdf.section_title("LED Ring Status")
    pdf.bullets([
        "Solid white: Standby mode",
        "Pulsing blue: Listening for commands",
        "Spinning orange: Processing request",
        "Solid red: Microphone muted",
        "Flashing yellow: Wi-Fi connection issue",
    ])

    pdf.chapter_title("4. Troubleshooting")
    pdf.section_title("Device not connecting to Wi-Fi")
    pdf.body("Ensure your router is broadcasting on 2.4GHz or 5GHz band. The NT-S100 supports both bands. If connection fails, try resetting the device by holding the Action button for 10 seconds until the LED ring flashes white.")
    pdf.section_title("Poor audio quality")
    pdf.body("Check that the speaker is not placed near metal objects or other wireless devices. Ensure the audio source bitrate is at least 128kbps. For best results, use FLAC or WAV files for local playback.")

    pdf.output(f"{OUTPUT_DIR}/NT-S100_Smart_Speaker_Manual.pdf")
    print("Created: NT-S100_Smart_Speaker_Manual.pdf")


# ============================================================
# PDF 2: NT-W200 스마트워치
# ============================================================
def create_pdf2():
    pdf = ManualPDF("NT-W200 SmartWatch Manual")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "NT-W200 SmartWatch", align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, "User Manual v1.5  |  NextTech Co., Ltd.", align="C", ln=True)
    pdf.ln(5)

    pdf.chapter_title("1. Product Overview")
    pdf.body("The NT-W200 is a premium smartwatch combining health monitoring, fitness tracking, and smart notifications in a sleek 44mm aluminum case. Featuring a 1.9-inch AMOLED display with always-on capability and up to 7 days battery life.")
    pdf.section_title("Key Specifications")
    pdf.bullets([
        "Display: 1.9-inch AMOLED, 410x502 resolution",
        "Case: 44mm aluminum with sapphire crystal glass",
        "Battery: 420mAh, up to 7 days typical use",
        "Water resistance: 5ATM (50 meters)",
        "Sensors: Heart rate, SpO2, ECG, skin temperature, accelerometer, gyroscope",
        "Connectivity: Bluetooth 5.3, Wi-Fi 802.11 b/g/n, NFC",
    ])

    pdf.chapter_title("2. Getting Started")
    pdf.section_title("2.1 Charging")
    pdf.body("Attach the magnetic charging cable to the back of the watch. A full charge takes approximately 90 minutes. The watch will display a charging animation when connected. Avoid charging in temperatures below 0C or above 45C.")
    pdf.section_title("2.2 Pairing with Smartphone")
    pdf.body("1. Power on the watch by pressing the side button for 3 seconds.\n2. Install the NextTech Fit app on your smartphone.\n3. Open the app and tap 'Pair New Device'.\n4. Select 'NT-W200' from the device list.\n5. Confirm the pairing code displayed on both devices.")

    pdf.chapter_title("3. Health & Fitness Features")
    pdf.section_title("3.1 Heart Rate Monitoring")
    pdf.body("The NT-W200 continuously monitors your heart rate 24/7. For accurate readings, wear the watch snugly on your wrist, about 1-2 finger widths above the wrist bone. High heart rate alerts can be configured in the app (default: 150 BPM).")
    pdf.section_title("3.2 Sleep Tracking")
    pdf.body("Wear the watch while sleeping to track sleep stages (light, deep, REM). Sleep data is synced to the app each morning. For best accuracy, enable Auto Sleep Detection in Settings > Health > Sleep.")
    pdf.section_title("3.3 Workout Modes")
    pdf.bullets([
        "Running, Walking, Cycling, Swimming",
        "HIIT, Yoga, Strength Training",
        "Golf, Tennis, Basketball",
        "Custom workout mode available",
    ])

    pdf.chapter_title("4. Troubleshooting")
    pdf.section_title("Watch not syncing with app")
    pdf.body("Ensure Bluetooth is enabled on your smartphone. Try toggling Bluetooth off and on. If the issue persists, forget the device in Bluetooth settings and re-pair. Make sure the NextTech Fit app has location permissions enabled.")

    pdf.output(f"{OUTPUT_DIR}/NT-W200_SmartWatch_Manual.pdf")
    print("Created: NT-W200_SmartWatch_Manual.pdf")


# ============================================================
# PDF 3: NT-R300 로봇 청소기
# ============================================================
def create_pdf3():
    pdf = ManualPDF("NT-R300 Robot Vacuum Manual")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "NT-R300 Robot Vacuum", align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, "User Manual v3.0  |  NextTech Co., Ltd.", align="C", ln=True)
    pdf.ln(5)

    pdf.chapter_title("1. Product Overview")
    pdf.body("The NT-R300 is an intelligent robot vacuum cleaner with LiDAR navigation, 3000Pa suction power, and automatic dirt disposal. It creates precise floor maps and supports multi-floor mapping for homes with multiple levels.")
    pdf.section_title("Key Specifications")
    pdf.bullets([
        "Suction power: 3000Pa (max)",
        "Dustbin capacity: 400ml (robot) + 3L (auto-empty station)",
        "Battery: 5200mAh, up to 180 minutes runtime",
        "Navigation: LiDAR + AI obstacle avoidance",
        "Noise level: 65dB (standard mode)",
        "Compatible surfaces: Hardwood, tile, carpet (up to 20mm pile)",
    ])

    pdf.chapter_title("2. Setup")
    pdf.section_title("2.1 Charging Station Placement")
    pdf.body("Place the charging station against a wall with at least 0.5m clearance on each side and 1.5m in front. Keep the area around the station clear of obstacles. Connect the station to a power outlet using the provided cable.")
    pdf.section_title("2.2 First-Time Mapping")
    pdf.body("1. Place the robot on the charging station and power it on.\n2. Open the NextTech Clean app and add the NT-R300.\n3. Tap 'Start Mapping' to begin the initial room scan.\n4. The robot will explore your home and create a floor map (15-30 minutes).\n5. Review and edit the map in the app to label rooms and set no-go zones.")

    pdf.chapter_title("3. Cleaning Modes")
    pdf.bullets([
        "Auto Mode: Intelligent room-by-room cleaning",
        "Spot Mode: Intensive cleaning of a specific area (1.5m x 1.5m)",
        "Edge Mode: Cleans along walls and corners",
        "Quiet Mode: Reduced suction for noise-sensitive environments",
        "Max Mode: Maximum suction for deep carpet cleaning",
        "Scheduled Cleaning: Set up to 7 weekly schedules",
    ])

    pdf.chapter_title("4. Maintenance")
    pdf.section_title("4.1 Cleaning the Dustbin")
    pdf.body("Empty the dustbin after each cleaning session or when the app notifies you. Remove the dustbin by pressing the release button on the back. Rinse with water and allow to dry completely before reinstalling.")
    pdf.section_title("4.2 Brush Maintenance")
    pdf.body("Clean the main brush every 2 weeks by removing it from the bottom panel. Use the included cleaning tool to remove hair and debris. Replace the main brush every 6-12 months depending on usage.")

    pdf.chapter_title("5. Troubleshooting")
    pdf.section_title("Robot getting stuck frequently")
    pdf.body("Update the floor map by running a new mapping session. Add virtual walls in the app to block problem areas. Ensure cables and small objects are removed from the floor before cleaning.")

    pdf.output(f"{OUTPUT_DIR}/NT-R300_Robot_Vacuum_Manual.pdf")
    print("Created: NT-R300_Robot_Vacuum_Manual.pdf")


# ============================================================
# PDF 4: NT-C400 스마트 카메라
# ============================================================
def create_pdf4():
    pdf = ManualPDF("NT-C400 Security Camera Manual")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "NT-C400 Smart Security Camera", align="C", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, "User Manual v1.8  |  NextTech Co., Ltd.", align="C", ln=True)
    pdf.ln(5)

    pdf.chapter_title("1. Product Overview")
    pdf.body("The NT-C400 is a 4K outdoor security camera with AI-powered person detection, color night vision, and two-way audio. Built for all-weather use with IP67 rating, it integrates seamlessly with the NextTech Home ecosystem.")
    pdf.section_title("Key Specifications")
    pdf.bullets([
        "Resolution: 4K (3840x2160) at 30fps",
        "Field of view: 130 degrees diagonal",
        "Night vision: Color up to 10m, IR up to 30m",
        "Storage: Local microSD (up to 256GB) + Cloud storage",
        "Weather resistance: IP67 (dust-tight, waterproof up to 1m)",
        "Audio: Built-in microphone + speaker, two-way communication",
        "Power: Wired (12V DC) or solar panel (optional)",
    ])

    pdf.chapter_title("2. Installation")
    pdf.section_title("2.1 Mounting")
    pdf.body("Choose a location with a clear view of the area you want to monitor. The camera should be mounted at 2.5-3m height for optimal coverage. Use the included mounting template to mark drill holes. Ensure the mounting surface can support at least 2kg.")
    pdf.section_title("2.2 Network Setup")
    pdf.body("1. Download the NextTech Home app and create an account.\n2. Tap '+' > 'Add Camera' > 'NT-C400'.\n3. Scan the QR code on the bottom of the camera.\n4. Enter your Wi-Fi credentials (2.4GHz or 5GHz supported).\n5. Wait for the LED to turn solid green indicating successful connection.")

    pdf.chapter_title("3. AI Detection Features")
    pdf.section_title("3.1 Person Detection")
    pdf.body("The NT-C400 uses on-device AI to distinguish people from animals, vehicles, and other motion. Enable Person Detection in the app under Camera Settings > Detection > Person. Adjust sensitivity (1-10) to reduce false alerts.")
    pdf.section_title("3.2 Facial Recognition")
    pdf.body("Add familiar faces in the app to receive personalized alerts. Go to Settings > Faces > Add Face and follow the enrollment process. The camera can store up to 100 face profiles locally.")
    pdf.section_title("3.3 Activity Zones")
    pdf.body("Draw custom detection zones in the app to focus alerts on specific areas. Up to 4 activity zones can be configured per camera. Zones can be scheduled to activate only during specific hours.")

    pdf.chapter_title("4. Storage & Privacy")
    pdf.section_title("4.1 Local Storage")
    pdf.body("Insert a microSD card (Class 10 or higher recommended) into the slot on the bottom of the camera. The camera supports continuous recording or event-based recording. Local footage is encrypted with AES-256.")
    pdf.section_title("4.2 Privacy Mode")
    pdf.body("Enable Privacy Mode in the app to pause all recording and detection. The LED will turn solid orange when Privacy Mode is active. You can schedule Privacy Mode to activate automatically (e.g., during work hours).")

    pdf.chapter_title("5. Troubleshooting")
    pdf.section_title("Camera offline in app")
    pdf.body("Check that the camera LED is solid green. If flashing red, the camera has lost Wi-Fi connection. Press the reset button for 5 seconds to restart the network configuration. Ensure your router's 2.4GHz band is enabled.")

    pdf.output(f"{OUTPUT_DIR}/NT-C400_Security_Camera_Manual.pdf")
    print("Created: NT-C400_Security_Camera_Manual.pdf")


if __name__ == "__main__":
    create_pdf1()
    create_pdf2()
    create_pdf3()
    create_pdf4()
    print(f"\nAll 4 PDFs created in '{OUTPUT_DIR}/' folder")
