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

### Stage 2: Audio Processing Pipeline
- [ ] Add audio recording/buffering capability
- [ ] Implement audio quality enhancement (noise reduction, normalization)
- [ ] Create audio chunk processing for real-time transcription
- [ ] Add configuration system for frequencies and settings

### Stage 3: Speech-to-Text Integration
- [ ] Integrate Deepgram speech recognition engine (with configurable fallback options)
- [ ] Implement real-time transcription pipeline
- [ ] Handle continuous audio stream processing
- [ ] Store transcription output with timestamps

### Stage 4: Keyword & EAS Detection
- [ ] Implement keyword detection system
- [ ] Add EAS (Emergency Alert System) specific detection
  - EAS header tone detection (853 Hz + 960 Hz)
  - EAS message parsing (SAME protocol)
- [ ] Create configurable keyword/phrase lists
- [ ] Implement confidence scoring

### Stage 5: Notification System
- [ ] Design notification API/webhook system
- [ ] Implement integration with external applications
- [ ] Add alert severity levels
- [ ] Create notification queue and delivery system
- [ ] Add logging and monitoring

## Technical Considerations

### Current Dependencies
- Python + Flask
- rtl_fm (RTL-SDR tools)
- FFmpeg

### Future Dependencies
- Deepgram API (speech recognition - primary choice)
- EAS tone detection library
- Notification service (webhooks, MQTT, etc.)
- Configuration management system (to support alternative STT engines)

### Architecture Notes
- Pipeline: SDR → Audio Processing → Transcription → Detection → Notification
- Real-time processing requirements
- Consider async/streaming architecture for scalability

## Configuration

**Current Settings**:
- Frequency: 162.55 MHz (NOAA Weather Radio)
- Sample Rate: 48 kHz
- Gain: 30 dB

## Notes

- Project name "sdr-transcription" reflects the transcription goal
- Initial focus is on NOAA Weather Radio but architecture should support other frequencies
- EAS detection is critical for emergency notifications
