import bencoder
from peer import get_all_peers

TORRENT_PATH = 'torrent_files/ubuntu.torrent'


def read_torrent_file(torrent_path) -> bytes:
    with open(torrent_path, 'rb') as torrent_file:
        torrent_data = torrent_file.read()
        return torrent_data


if __name__ == '__main__':
    torrent_data = read_torrent_file(TORRENT_PATH)
    decoded_torrent = bencoder.decode(torrent_data)
    peers = get_all_peers(decoded_torrent)
