import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import subprocess
from cv_bridge import CvBridge
import cv2

class RealSenseStreamer(Node):
    def __init__(self):
        super().__init__('realsense_ffmpeg_streamer')
        self.bridge = CvBridge()

        # Start FFmpeg subprocess
        self.ffmpeg = subprocess.Popen([
            'ffmpeg',
            '-f', 'rawvideo',
            '-pixel_format', 'bgr24',
            '-video_size', '640x480',
            '-framerate', '30',
            '-i', '-',
            '-f', 'mpegts',
            '-codec:v', 'mpeg1video',
            '-b:v', '800k',
            'http://10.234.3.14:8081/mysecret123'
        ], stdin=subprocess.PIPE)

        # Subscribe to RealSense color image topic
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            if frame.shape != (480, 640, 3):
                # Optional: resize if RealSense is outputting different resolution
                frame = cv2.resize(frame, (640, 480))
            self.ffmpeg.stdin.write(frame.tobytes())
        except Exception as e:
            self.get_logger().error(f"Failed to process frame: {e}")

    def destroy_node(self):
        # Properly close FFmpeg
        if self.ffmpeg:
            try:
                self.ffmpeg.stdin.close()
                self.ffmpeg.wait()
            except Exception:
                pass
        super().destroy_node()

def main():
    rclpy.init()
    node = RealSenseStreamer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
