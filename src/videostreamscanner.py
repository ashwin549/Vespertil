import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
from scapy.all import ARP, Ether, srp
import netifaces

def get_local_ip():
    """Get the local IP address of the device"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))  # Doesn't actually connect
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def scan_network():
    """Scan the local network for all active devices"""
    # Get local IP and network interface
    local_ip = get_local_ip()
    network = local_ip.rsplit('.', 1)[0] + '.0/24'
    
    # Create ARP request packet
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # Send packet and get responses
    result = srp(packet, timeout=3, verbose=0)[0]
    
    # Return list of active IP addresses
    return [received.psrc for sent, received in result]

def check_common_ports(ip):
    """Check if common video streaming ports are open"""
    common_ports = [554, 80, 8080, 8554, 8000]  # RTSP, HTTP, common alternate ports
    open_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    
    return open_ports

def check_for_stream(ip, port):
    """Check if there's a video stream at the given IP and port"""
    # Try common streaming endpoints
    endpoints = [
        f'http://{ip}:{port}/video',
        f'http://{ip}:{port}/stream',
        f'http://{ip}:{port}/mjpeg',
        f'rtsp://{ip}:{port}/live',
        f'http://{ip}:{port}/video.mjpg'
    ]
    
    for endpoint in endpoints:
        try:
            if endpoint.startswith('rtsp'):
                # For RTSP, just try to connect
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(1)
                result = client.connect_ex((ip, port))
                client.close()
                if result == 0:
                    return endpoint
            else:
                # For HTTP, try to get headers
                response = requests.head(endpoint, timeout=1)
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    if any(x in content_type.lower() for x in ['video', 'stream', 'mjpeg']):
                        return endpoint
        except:
            continue
    return None

def find_video_streams():
    """Main function to find video streams on the network"""
    print("Scanning network for devices...")
    active_ips = scan_network()
    
    streams_found = []
    
    print(f"Found {len(active_ips)} active devices. Checking for video streams...")
    
    def check_device(ip):
        open_ports = check_common_ports(ip)
        for port in open_ports:
            stream_url = check_for_stream(ip, port)
            if stream_url:
                streams_found.append(stream_url)
                print(f"Found potential stream: {stream_url}")
    
    # Use ThreadPoolExecutor to scan multiple devices concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(check_device, active_ips)
    
    return streams_found

if __name__ == "__main__":
    streams = find_video_streams()
    if streams:
        print("\nFound video streams:")
        for stream in streams:
            print(stream)
    else:
        print("\nNo video streams found on the network.")