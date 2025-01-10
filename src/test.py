rtsp_urls = [
    "rtsp://917259933450:admin%40123@192.168.1.2:554/live",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/stream1",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/ch01/0",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/video1",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/ch01/main",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/cam/realmonitor?channel=1&subtype=0",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/Streaming/Channels/101",
    "rtsp://917259933450:admin%40123@192.168.1.2:554/h264Preview_01_main"
]

# Test code to try each URL
import cv2

def test_rtsp_stream(urls):
    for url in urls:
        print(f"Testing: {url}")
        cap = cv2.VideoCapture(url)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Success! Working URL: {url}")
                cap.release()
                return url
        cap.release()
        print("Failed, trying next URL...")
    
    return None

working_url = test_rtsp_stream(rtsp_urls)