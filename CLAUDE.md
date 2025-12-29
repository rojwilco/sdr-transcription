# SDR Transcription Project

## Project Overview

This project captures NOAA Weather Radio broadcasts using Software Defined Radio (SDR) technology and processes them for keyword and Emergency Alert System (EAS) detection.

## Ultimate Goal

Create a system that:
1. Captures live NOAA Weather Radio broadcasts via RTL-SDR
2. Transcribes speech in real-time
3. Detects keywords and EAS alerts
4. Generates notifications to external applications

## Current State

**Status**: Stage 1 - Basic FM Streaming ✓

The application currently:
- Captures FM radio at 162.55 MHz (NOAA Weather Radio)
- Streams audio through a Flask web server
- Converts raw SDR audio to MP3 format
- Provides a simple web-based audio player

**Key Files**:
- `fm_player/app.py` - Flask server with audio pipeline
- `fm_player/templates/index.html` - Web interface

## Project Stages

### Stage 1: FM Streaming (COMPLETE)
- [x] Capture FM radio signal using rtl_fm
- [x] Convert audio to streamable format (MP3)
- [x] Serve audio stream via web interface
- [x] Test with NOAA Weather Radio frequency

**Definition of Done:**
- ✓ User can navigate to web interface and hear live NOAA weather radio
- ✓ Audio plays continuously without dropouts
- ✓ Web interface is accessible from any browser on the network

### Stage 2: Audio Processing Pipeline
- [ ] Add audio recording/buffering capability
- [ ] Implement audio quality enhancement (noise reduction, normalization)
- [ ] Create audio chunk processing for real-time transcription
- [ ] Add configuration system for frequencies and settings

**Definition of Done:**
- User can modify frequency settings via config file and restart to tune different stations
- Audio quality is noticeably improved (less static/noise)
- System buffers audio without impacting stream playback
- Configuration changes take effect without code modifications

### Stage 3: Speech-to-Text Integration (On-Demand)
- [ ] Integrate Deepgram speech recognition engine (with configurable fallback options)
- [ ] Implement on-demand transcription activation (via MQTT command or web interface)
- [ ] Handle real-time audio stream processing when active
- [ ] Store transcription output with timestamps
- [ ] Auto-stop transcription after configurable timeout or explicit stop command

**Definition of Done:**
- User can click a button on web interface to start transcription
- Live transcription text appears on web page in real-time
- User can send MQTT command to start/stop transcription remotely
- Transcription automatically stops after configured timeout
- Transcription history is viewable with timestamps
- User can verify transcription accuracy by comparing with heard audio

### Stage 4: Keyword & EAS Detection
- [ ] Implement keyword detection system (from transcribed text)
  - Create configurable keyword/phrase lists
  - Implement confidence scoring
- [ ] Add EAS (Emergency Alert System) detection (direct from audio signal)
  - Integrate existing EAS detection tools (e.g., multimon-ng, dsp-eas)
  - EAS header tone detection (853 Hz + 960 Hz dual-tone)
  - SAME (Specific Area Message Encoding) protocol parsing
  - EAS runs in parallel with transcription pipeline for faster alerts

**Definition of Done:**
- User can add/remove keywords via config file
- Web interface highlights detected keywords in transcription
- EAS alerts are detected and decoded without transcription running
- User can trigger test EAS tone and verify detection within seconds
- System logs show keyword matches with confidence scores
- EAS detection shows SAME header details (event type, area codes, duration)

### Stage 5: Notification System (MQTT)
- [ ] Implement MQTT publisher for alerts
- [ ] Publish EAS alerts to MQTT (immediate, high-priority topic)
- [ ] Publish keyword matches to MQTT (standard topic)
- [ ] Implement MQTT command subscription for transcription control
  - Start/stop transcription commands
  - Transcription status reporting
- [ ] Add alert metadata (timestamp, severity, message content)
- [ ] Configure MQTT broker connection settings
- [ ] Enable Home Assistant and other MQTT consumer integration
- [ ] Add basic logging

**Definition of Done:**
- User can subscribe to MQTT topics with `mosquitto_sub` and see messages
- EAS alerts appear on `noaa/eas/alerts` topic within 5 seconds of detection
- Keyword matches appear on `noaa/keywords` topic with full context
- User can send MQTT command to `noaa/transcription/control` to start/stop transcription
- Home Assistant automation receives and displays alerts
- MQTT messages include valid JSON with timestamp, severity, and content
- System status published to `noaa/status` topic (online/offline)

### Stage 6: Containerization & Deployment
- [ ] Create Dockerfile for the application
- [ ] Configure USB device mapping for RTL-SDR dongle
  - Use `--device=/dev/bus/usb` or specific device mapping
  - Add necessary privileges for USB access
- [ ] Set up docker-compose for easy deployment
- [ ] Add environment variable configuration for:
  - MQTT broker settings
  - Deepgram API key
  - Frequency and SDR settings
  - EAS detection parameters
- [ ] Create volume mounts for persistent data (logs, recordings, config)
- [ ] Document container deployment and USB troubleshooting

**Definition of Done:**
- User can run `docker-compose up -d` and system starts successfully
- RTL-SDR device is accessible within container (verify with `rtl_test`)
- User can modify `.env` file to change all settings without rebuilding image
- Container restarts automatically on failure or system reboot
- Logs persist across container restarts in mounted volume
- User can deploy on fresh system with only Docker installed
- README includes complete setup instructions from zero to running

## Technical Considerations

### Current Dependencies
- Python + Flask
- rtl_fm (RTL-SDR tools)
- FFmpeg

### Future Dependencies
- Deepgram API (speech recognition - primary choice)
- EAS detection tools (multimon-ng, dsp-eas, or similar for SAME decoding)
- MQTT client library (paho-mqtt or similar)
- Configuration management system (to support alternative STT engines)
- Docker & Docker Compose (containerized deployment)

### Architecture Notes
- Dual Pipeline Architecture:
  - **Transcription Path** (on-demand): SDR → Audio Processing → Deepgram STT → Keyword Detection → MQTT Publish
  - **EAS Path** (always running): SDR → Audio Processing → EAS Decoder → MQTT Publish
- EAS detection runs continuously, independent of transcription
- Deepgram transcription only activated on-demand (MQTT command or web interface)
  - Reduces API costs by not transcribing 24/7
  - EAS alerts don't require transcription
- MQTT bidirectional: publishes alerts, subscribes to control commands
- MQTT output enables easy integration with Home Assistant and other automation systems
- Lightweight notification approach - no complex queuing needed
- Containerized deployment with Docker
  - RTL-SDR USB device mapped into container
  - Environment-based configuration
  - Easy deployment alongside Home Assistant

## Configuration

**Current Settings**:
- Frequency: 162.55 MHz (NOAA Weather Radio)
- Sample Rate: 48 kHz
- Gain: 30 dB

## Notes

- Project name "sdr-transcription" reflects the transcription goal
- Initial focus is on NOAA Weather Radio but architecture should support other frequencies
- EAS detection is critical for emergency notifications
- EAS alerts detected directly from audio signal using known tools (no transcription needed)
- Deepgram transcription is on-demand only (not continuous) to reduce API costs
  - Activated via MQTT command or web interface
  - EAS detection runs 24/7 without transcription costs
- Simple MQTT publishing for notifications - no heavy infrastructure needed
- MQTT enables easy integration with Home Assistant, Node-RED, and other automation platforms
- Dual pipeline approach: EAS detection runs continuously, transcription only when needed
- Application will be containerized with Docker
  - RTL-SDR USB device must be mapped into container (`--device=/dev/bus/usb`)
  - Requires privileged access or specific USB permissions
  - Docker Compose for simplified deployment and configuration
