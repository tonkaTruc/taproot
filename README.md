
# Taproot ToolKit

A network media QA toolkit for packet capture, analysis, network interface management, and SMPTE ST 2110 media processing.

## Installation

```bash
pip install -e .
```

## Usage

### List Network Interfaces

Display all available network interfaces:

```bash
taproot network list-interfaces
```

Output:
```
lo: ['127.0.0.1', '::1', '00:00:00:00:00:00']
eth0: ['192.168.1.100', 'fe80::a1b2:c3d4:e5f6%eth0', 'aa:bb:cc:dd:ee:ff']
```

### Packet Capture

Capture packets from a network interface:

```bash
# Capture 20 packets (default)
sudo taproot network capture -i eth0

# Capture specific number of packets
sudo taproot network capture -i eth0 -c 100

# Capture and save to a file in cap_store
sudo taproot network capture -i eth0 -c 100 --save my_capture.pcap
```

**Note:** Requires root/sudo privileges.

### Pcap File Management

List available pcap files in the cap_store directory:

```bash
taproot network list-pcaps
```

Replay a pcap file on a network interface:

```bash
# Replay all packets
sudo taproot network replay-pcap file.pcap -i eth0

# Replay first 100 packets with 0.1s interval
sudo taproot network replay-pcap file.pcap -i eth0 -c 100 -t 0.1

# Get pcap file info without replaying
taproot network replay-pcap file.pcap -i eth0 --info
```

### Packet Creation

Create and send custom packets:

```bash
# Send a UDP packet
sudo taproot network create-packet -i eth0 --src-ip 192.168.1.100 --dst-ip 192.168.1.1 --dport 5000

# Send a TCP packet with payload
sudo taproot network create-packet -i eth0 --protocol tcp --sport 8080 --dport 80 --payload "Hello"

# Send multiple packets
sudo taproot network create-packet -i eth0 --dst-ip 192.168.1.1 --dport 9999 -c 10
```

**Note:** Requires root/sudo privileges.

### Pcap Modification

Modify packet fields in pcap files:

```bash
# Anonymize source addresses
taproot network modify-pcap input.pcap output.pcap --anonymize

# Zero specific fields
taproot network modify-pcap input.pcap output.pcap --zero-ip-src --zero-mac-src

# Set specific values
taproot network modify-pcap input.pcap output.pcap --ip-src 10.0.0.1 --mac-src 00:11:22:33:44:55
```

### Pcap Inspection

Inspect packets in a pcap file:

```bash
# List all packets
taproot network inspect-pcap file.pcap

# Show detailed info for specific packet
taproot network inspect-pcap file.pcap -n 0 --layers --show-hex
```

### Multicast Group Management

Join and leave multicast groups:

```bash
# Join a multicast group
taproot network mcast-join -i eth0 --group 239.0.0.1

# Join a multicast group and capture 20 packets
sudo taproot network mcast-join -i eth0 --group 239.0.0.1 --capture 20

# Join, capture, and save packets to a file
sudo taproot network mcast-join -i eth0 --group 239.0.0.1 --capture 20 --save mcast_capture.pcap

# Leave a multicast group
taproot network mcast-leave -i eth0 --group 239.0.0.1
```

**Note:** The interface's IPv4 address is automatically detected. Packet capture requires root/sudo privileges. When using `--capture`, the command will automatically leave the multicast group after capturing the specified number of packets.

## SMPTE ST 2110 Media Processing

The toolkit includes comprehensive support for extracting and exporting media from SMPTE ST 2110 packet captures.

### Prerequisites

Install additional dependencies for media processing:

```bash
pip install numpy soundfile ffmpeg-python pillow
# Also requires FFmpeg: sudo apt-get install ffmpeg (Ubuntu/Debian)
```

### List RTP Streams

Analyze a pcap file and list all RTP streams:

```bash
taproot media list-streams audio.pcap
taproot media list-streams video.pcap --use-ptp
```

### Export Audio (ST 2110-30)

Export audio streams to WAV, FLAC, or MP3:

```bash
# Export to WAV (default)
taproot media export-audio audio.pcap -o output.wav

# Export to FLAC
taproot media export-audio audio.pcap -o output.flac --format flac

# Export to MP3
taproot media export-audio audio.pcap -o output.mp3 --format mp3 --bitrate 320

# Export specific stream with PTP timing
taproot media export-audio audio.pcap -o output.wav --ssrc 0x12345678 --use-ptp
```

### Export Video (ST 2110-20)

Export video streams to MP4, MOV, or other formats:

```bash
# Export to MP4 with H.264
taproot media export-video video.pcap -o output.mp4

# Export to MOV with ProRes (for editing)
taproot media export-video video.pcap -o output.mov --codec prores --prores-profile hq

# Export with H.265 for better compression
taproot media export-video video.pcap -o output.mp4 --codec h265 --crf 20
```

Supported codecs: **H.264** (most compatible), **H.265** (better compression), **ProRes** (editing)

### Export Ancillary Data (ST 2110-40)

Export captions, timecode, and metadata:

```bash
# Export all ancillary data to JSON
taproot media export-anc anc.pcap -o output.json

# Export captions to SRT subtitle file
taproot media export-anc anc.pcap -o captions.srt --type captions --format srt

# Export timecode to CSV
taproot media export-anc anc.pcap -o timecode.csv --type timecode --format csv
```

Supported ANC types: **CEA-608/708 Captions**, **SMPTE 12M Timecode**, **AFD/Bar Data**, **SCTE-104**, and more.

### Complete Workflow Example

```bash
# 1. Capture multicast audio stream
sudo taproot network mcast-join -i eth0 --group 239.0.0.1 --capture 1000 --save audio.pcap

# 2. List streams to verify
taproot media list-streams audio.pcap

# 3. Export to WAV
taproot media export-audio audio.pcap -o audio.wav
```

**For complete documentation**, see [docs/MEDIA.md](docs/MEDIA.md)

## File-to-RTP Streaming (GStreamer)

Stream audio and video files as RTP streams with ST2110 compliance.

### Prerequisites

Install GStreamer and Python bindings:

```bash
# Ubuntu/Debian
sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly python3-gi gir1.2-gstreamer-1.0

# Install Python dependencies
pip install -e ".[streaming]"
```

### Stream Audio File

Stream audio files to RTP (ST2110-30/31):

```bash
# Stream to multicast group
taproot media stream-audio audio.wav --dest-ip 239.0.0.1 --dest-port 5004

# Stream with custom parameters
taproot media stream-audio audio.flac --dest-ip 239.1.1.1 --dest-port 5004 \
    --sample-rate 48000 --channels 8 --bit-depth 24

# Stream with PTP synchronization
taproot media stream-audio audio.wav --dest-ip 239.0.0.1 --dest-port 5004 \
    --use-ptp --ptp-domain 0 -i eth0
```

### Stream Video File

Stream video files to RTP (ST2110-20):

```bash
# Stream to multicast group
taproot media stream-video video.mp4 --dest-ip 239.0.0.2 --dest-port 5005

# Stream 4K video
taproot media stream-video video.mov --dest-ip 239.1.1.2 --dest-port 5005 \
    --width 3840 --height 2160 --framerate 60

# Stream with PTP synchronization
taproot media stream-video video.mp4 --dest-ip 239.0.0.2 --dest-port 5005 \
    --use-ptp --ptp-domain 0 -i eth0
```

**Supported formats:** WAV, FLAC, MP3, MP4, MOV, AVI, MKV, and more.

**For complete documentation**, see [docs/STREAMING.md](docs/STREAMING.md)

### Getting Help

```bash
taproot --help              # Main help
taproot network --help      # Network commands help
taproot media --help        # Media commands help
taproot network capture --help  # Specific command help
```

## Development

For CLI architecture and development guide, see [docs/CLI.md](docs/CLI.md).

### Project Structure

```
toolkit/
├── taproot/
│   ├── cli.py                      # CLI entry point
│   ├── network/
│   │   ├── interfaces.py           # Network interface utilities
│   │   ├── multicast.py            # Multicast group management
│   │   ├── server.py               # Simple TCP server (future)
│   │   └── packet/
│   │       ├── capture.py          # Packet capture
│   │       ├── replay.py           # Pcap replay
│   │       ├── packet_creator.py   # Packet crafting (builder pattern)
│   │       └── packet_modifier.py  # Packet field modification
│   ├── media/                      # SMPTE ST 2110 media processing
│   │   ├── rtp_extractor.py        # RTP stream extraction & reassembly
│   │   ├── decoders/               # Media decoders
│   │   │   ├── st2110_20.py        # Video decoder
│   │   │   ├── st2110_30.py        # Audio decoder
│   │   │   └── st2110_40.py        # Ancillary data decoder
│   │   └── exporters/              # Media exporters
│   │       ├── audio.py            # Audio export (WAV, FLAC, MP3)
│   │       ├── video.py            # Video export (MP4, MOV, etc.)
│   │       └── ancillary.py        # ANC export (SRT, VTT, JSON, etc.)
│   └── custom_headers/
│       └── PTP.py                  # PTP protocol headers
├── Resources/
│   └── cap_store/                  # Pcap file storage
├── docs/
│   ├── CLI.md                      # CLI development guide
│   └── MEDIA.md                    # Media processing documentation
├── tests/                          # Test suite
└── pyproject.toml                  # Project configuration
```
