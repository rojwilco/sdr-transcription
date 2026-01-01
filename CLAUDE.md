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
- [ ] **[P1]** Add audio recording/buffering capability
- [ ] **[P1]** Implement audio quality enhancement (noise reduction, normalization)
- [ ] **[P0]** Create audio chunk processing for real-time transcription
- [ ] **[P0]** Add configuration system for frequencies and settings

**Definition of Done:**
- **[P0]** User can modify frequency settings via config file and restart to tune different stations
- **[P1]** Audio quality is noticeably improved (less static/noise)
- **[P1]** System buffers audio without impacting stream playback
- **[P0]** Configuration changes take effect without code modifications

### Stage 3: Speech-to-Text Integration (On-Demand)
- [ ] **[P0]** Integrate Deepgram speech recognition engine (with configurable fallback options)
- [ ] **[P0]** Implement on-demand transcription activation (via MQTT command or web interface)
- [ ] **[P0]** Handle real-time audio stream processing when active
- [ ] **[P1]** Store transcription output with timestamps
- [ ] **[P0]** Auto-stop transcription after configurable timeout or explicit stop command

**Definition of Done:**
- **[P0]** User can click a button on web interface to start transcription
- **[P0]** Live transcription text appears on web page in real-time
- **[P0]** User can send MQTT command to start/stop transcription remotely
- **[P0]** Transcription automatically stops after configured timeout
- **[P1]** Transcription history is viewable with timestamps
- **[P0]** User can verify transcription accuracy by comparing with heard audio

### Stage 4: Keyword & EAS Detection
- [ ] **[P1]** Implement keyword detection system (from transcribed text)
  - **[P1]** Create configurable keyword/phrase lists
  - **[P1]** Implement confidence scoring
- [ ] **[P0]** Add EAS (Emergency Alert System) detection (direct from audio signal)
  - **[P0]** Integrate existing EAS detection tools (e.g., multimon-ng, dsp-eas)
  - **[P0]** EAS header tone detection (853 Hz + 960 Hz dual-tone)
  - **[P0]** SAME (Specific Area Message Encoding) protocol parsing
  - **[P0]** EAS runs in parallel with transcription pipeline for faster alerts

**Definition of Done:**
- **[P1]** User can add/remove keywords via config file
- **[P1]** Web interface highlights detected keywords in transcription
- **[P0]** EAS alerts are detected and decoded without transcription running
- **[P0]** User can trigger test EAS tone and verify detection within seconds
- **[P1]** System logs show keyword matches with confidence scores
- **[P0]** EAS detection shows SAME header details (event type, area codes, duration)

### Stage 5: Notification System (MQTT)
- [ ] **[P0]** Implement MQTT publisher for alerts
- [ ] **[P0]** Publish EAS alerts to MQTT (immediate, high-priority topic)
- [ ] **[P1]** Publish keyword matches to MQTT (standard topic)
- [ ] **[P0]** Implement MQTT command subscription for transcription control
  - **[P0]** Start/stop transcription commands
  - **[P0]** Transcription status reporting
- [ ] **[P0]** Add alert metadata (timestamp, severity, message content)
- [ ] **[P0]** Configure MQTT broker connection settings
- [ ] **[P0]** Enable Home Assistant and other MQTT consumer integration
- [ ] **[P0]** Add basic logging

**Definition of Done:**
- **[P0]** User can subscribe to MQTT topics with `mosquitto_sub` and see messages
- **[P0]** EAS alerts appear on `noaa/eas/alerts` topic within 5 seconds of detection
- **[P1]** Keyword matches appear on `noaa/keywords` topic with full context
- **[P0]** User can send MQTT command to `noaa/transcription/control` to start/stop transcription
- **[P0]** Home Assistant automation receives and displays alerts
- **[P0]** MQTT messages include valid JSON with timestamp, severity, and content
- **[P0]** System status published to `noaa/status` topic (online/offline)

### Stage 6: Containerization & Deployment
- [ ] **[P0]** Create Dockerfile for the application
- [ ] **[P0]** Configure USB device mapping for RTL-SDR dongle
  - **[P0]** Use `--device=/dev/bus/usb` or specific device mapping
  - **[P0]** Add necessary privileges for USB access
- [ ] **[P0]** Set up docker-compose for easy deployment
- [ ] **[P0]** Add environment variable configuration for:
  - **[P0]** MQTT broker settings
  - **[P0]** Deepgram API key
  - **[P0]** Frequency and SDR settings
  - **[P0]** EAS detection parameters
- [ ] **[P1]** Create volume mounts for persistent data (logs, recordings, config)
- [ ] **[P0]** Document container deployment and USB troubleshooting

**Definition of Done:**
- **[P0]** User can run `docker-compose up -d` and system starts successfully
- **[P0]** RTL-SDR device is accessible within container (verify with `rtl_test`)
- **[P0]** User can modify `.env` file to change all settings without rebuilding image
- **[P0]** Container restarts automatically on failure or system reboot
- **[P1]** Logs persist across container restarts in mounted volume
- **[P0]** User can deploy on fresh system with only Docker installed
- **[P0]** README includes complete setup instructions from zero to running

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
