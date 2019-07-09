from video_util.cam import RealsenseCam
from server_util.server import VideoStreamingServer, VideoStreamingHandler


server_name = 'Fuck You'


if __name__ == "__main__":
    cam = RealsenseCam()
    cam.start_streams()

    with VideoStreamingServer(cam=cam, device_identifier=server_name,
                              server_address=('localhost', 0), RequestHandlerClass=VideoStreamingHandler) as server:
        print('Starting server on port {}'.format(server.socket.getsockname()[1]))
        server.serve_forever()
