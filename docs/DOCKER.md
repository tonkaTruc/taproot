# Docker Guide for Taproot ToolKit

## Building the Image

Build the Docker image with:

```bash
docker build -t taproot-toolkit:latest .
```

## Running the Container

### Basic Usage

Show help:
```bash
docker run --rm taproot-toolkit:latest
```

Run a specific command:
```bash
docker run --rm taproot-toolkit:latest taproot network list-interfaces
```

### Network Operations

For network operations that require host network access:

```bash
# List interfaces
docker run --rm --network host taproot-toolkit:latest taproot network list-interfaces

# Capture packets (requires privileges)
docker run --rm --privileged --network host taproot-toolkit:latest \
    taproot network capture -i eth0 -c 20
```

### Media Processing

Mount a directory with media files:

```bash
# List streams in a pcap file
docker run --rm -v $(pwd)/data:/data taproot-toolkit:latest \
    taproot media list-streams /data/audio.pcap

# Export audio
docker run --rm -v $(pwd)/data:/data taproot-toolkit:latest \
    taproot media export-audio /data/audio.pcap -o /data/output.wav

# Stream audio file to RTP
docker run --rm --network host -v $(pwd)/data:/data taproot-toolkit:latest \
    taproot media stream-audio /data/audio.wav --dest-ip 239.0.0.1 --dest-port 5004
```

### Interactive Shell

Start an interactive session:

```bash
docker run --rm -it --network host taproot-toolkit:latest /bin/bash
```

Then run commands inside:
```bash
taproot --help
taproot network list-interfaces
taproot media --help
```

## Verifying GStreamer

Check GStreamer installation:

```bash
docker run --rm taproot-toolkit:latest gst-inspect-1.0 --version
docker run --rm taproot-toolkit:latest gst-inspect-1.0 | head -20
```

## Notes

- Use `--network host` for network operations
- Use `--privileged` for packet capture operations
- Mount volumes with `-v` to access local files
- The `taproot` CLI command is available globally in the container
