from pathlib import Path

import pytest

from taproot.media.rtp_extractor import RTPStreamExtractor
from taproot.network.packet.replay import get_cap_store_path
from tests import log

CAP_STORE = Path(get_cap_store_path())

@pytest.fixture(params=CAP_STORE.glob('.ref_ST2110-30*'))
def cap_store_file(request) -> Path:
    return request.param


def test_cap_store(cap_store_file):
    log.info(cap_store_file.absolute())


def test_list_streams(cap_store_file):
    """Test listing RTP streams from a pcap file."""

    # Extract streams
    log.info(f"Testing RTP stream extraction from: {cap_store_file}")
    extractor = RTPStreamExtractor(use_ptp=False)
    extractor.extract_from_pcap(str(cap_store_file))

    if streams := extractor.list_streams():
        log.info(f"Found {len(streams)} RTP stream(s):")
        for ssrc, info in streams:
            log.info(f"SSRC: {ssrc:#010x}")
            log.info(f"  Payload Type: {info.payload_type} ({extractor.get_payload_type_name(info.payload_type)})")
            log.info(f"  Packets: {info.packet_count}")
            log.info(f"  Sequence: {info.first_seq} -> {info.last_seq}")
            log.info(f"  Timestamp Range: {info.first_timestamp} -> {info.last_timestamp}")
            log.info(f"  Duration: {info.duration:.3f}s")
            log.info(f"  Packets Lost: {info.packets_lost} ({info.packet_loss_rate:.2f}%)")
            log.info(f"  Out of Order: {info.packets_out_of_order}")
            log.info(" ")
        assert True

    else:
        # Debug: check if any packets were read
        log.debug(f"Debug: Number of SSRCs in streams dict: {len(extractor.streams)}")
        assert False, "No RTP streams found!"
