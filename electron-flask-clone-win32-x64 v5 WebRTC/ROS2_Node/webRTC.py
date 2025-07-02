import asyncio
import cv2
import websockets
import json
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.sdp import candidate_from_sdp
from av import VideoFrame
import numpy as np
SIGNALING_SERVER = "ws://10.234.3.14:8082"  # Change to your signaling server address

# Global variable to store the latest frame
latest_frame = None

class ROSCameraSubscriber(Node): 
    def __init__(self):
        super().__init__('camera_web_rtc_bridge')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        global latest_frame
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            latest_frame = cv_image
        except Exception as e:
            self.get_logger().error(f"Error converting image: {e}")

class ROSVideoStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()

    async def recv(self):
        global latest_frame
        pts, time_base = await self.next_timestamp()

        # Wait for a valid frame
        while latest_frame is None:
            await asyncio.sleep(0.01)

        frame = latest_frame.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

async def run_offer():
    pc = RTCPeerConnection()
    pc.addTrack(ROSVideoStreamTrack())

    async with websockets.connect(SIGNALING_SERVER) as ws:
        offer = await pc.createOffer()
        await pc.setLocalDescription(offer)
        await ws.send(json.dumps({"offer": {"type": pc.localDescription.type, "sdp": pc.localDescription.sdp}}))

        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if "answer" in data:
                answer = data["answer"]
                await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))
            elif "candidate" in data:
                candidate = data["candidate"]
                parsed_candidate = candidate_from_sdp(candidate["candidate"])
                parsed_candidate.sdpMid = candidate["sdpMid"]
                parsed_candidate.sdpMLineIndex = candidate["sdpMLineIndex"]
                await pc.addIceCandidate(parsed_candidate)

def main():
    rclpy.init()
    node = ROSCameraSubscriber()

    thread = asyncio.get_event_loop().run_in_executor(None, rclpy.spin, node)

    try:
        asyncio.run(run_offer())
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
