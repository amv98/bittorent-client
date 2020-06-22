import bencoder
from pprint import pprint
import random
import hashlib
import requests
from urllib.parse import urlencode

TORRENT_PATH = 'torrent_files/ubuntu.torrent'


def read_torrent_file(torrent_path) -> bytes:
    with open(torrent_path, 'rb') as torrent_file:
        torrent_data = torrent_file.read()
        return torrent_data


torrent_data = read_torrent_file(TORRENT_PATH)
decoded_torrent = bencoder.decode(torrent_data)

"""
#del decoded_torrent[b"info"][b"pieces"]
#pprint(decoded_torrent)
{b'announce': b'https://torrent.ubuntu.com/announce',
 b'announce-list': [[b'https://torrent.ubuntu.com/announce'],
                    [b'https://ipv6.torrent.ubuntu.com/announce']],
 b'comment': b'Ubuntu CD releases.ubuntu.com',
 b'creation date': 1571323134,
 b'info': {b'length': 2463842304,
           b'name': b'ubuntu-19.10-desktop-amd64.iso',
           b'piece length': 1048576}}

"""

def generate_peer_id() -> bytes:
    """
    Any 20-byte string used as a unique ID for the client.
    """
    return '-IZZ314-' + ''.join([str(random.randint(0, 9)) for _ in range(12)])

def generate_info_hash(torrent_data) -> bytes:
    info_dict = bencoder.encode(torrent_data[b'info'])
    info_sha1 = hashlib.sha1(info_dict)
    return info_sha1.digest()

def construct_request_parameters(torrent_data, port, event = 'started'):
    """
    info_hash
    peer_id
    port
    uploaded
    downloaded
    left
    compact
    no_peer_id
    event
    ip - Optional
    numwant - Optional
    key - Optional
    trackerid - Optional
    Event can have states started, stopped, completed.
    """
    info_hash = generate_info_hash(torrent_data) #rencode and create a 20 byte SHA1 hash or something else.
    peer_id = generate_peer_id()
    port = port
    if event == 'started':
        uploaded = 0 # initially when requesting is zero maybe change later
        downloaded = 0 #initially zero when requesting maybe change later
        left = torrent_data[b'info'][b'length']
    compact = 1 #the peers list response will be 6 bytes per peer. Most trackers only accept compact = 1
    no_peer_id = 'random' #this value is ignored if the compact value is 1.
    event = event
    ip = 'ip address' #we wont pass this as it only needed when request is passed through a proxy
    numwant = 'Optional'
    key = 'Optional'
    trackerid = 'Optional'

    return urlencode({'info_hash':info_hash,'peer_id':peer_id,'port':port,'uploaded':uploaded,'downloaded':downloaded,'left':left,'compact':compact,'event':event})

def get_tracker_response(torrent_data):
    port = random.randint(6578, 6588)
    parameters = construct_request_parameters(torrent_data, port)
    tracker_url = torrent_data[b'announce']
    request_url = f'{tracker_url.decode()}?{parameters}'
    #print(request_url)
    request = requests.get(request_url)
    #print(request.text)
    return request.content


if __name__ == '__main__':
    tracker_response = get_tracker_response(decoded_torrent)
    