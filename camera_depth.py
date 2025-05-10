from arducam_tof_camera import Camera

def open_depth_camera():
    cam = Camera()
    cam.init()
    cam.start()
    return cam

def capture_depth_frame(cam):
    frame = cam.requestFrame(200)
    return frame.getDepthData()

def get_intrinsics(cam):
    def read_control(control):
        val = 0
        cam.getControl(control, val)
        return val / 100.0

    fx = read_control("INTRINSIC_FX")
    fy = read_control("INTRINSIC_FY")
    cx = read_control("INTRINSIC_CX")
    cy = read_control("INTRINSIC_CY")

    return [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]
    
def get_extrinsics(cam):
    def read_control(control):
        val = 0
        cam.getControl(control, val)
        return val / 100.0

    tx = read_control("EXTRINSIC_TX")
    ty = read_control("EXTRINSIC_TY")
    tz = read_control("EXTRINSIC_TZ")
    rx = read_control("EXTRINSIC_RX")
    ry = read_control("EXTRINSIC_RY")
    rz = read_control("EXTRINSIC_RZ")

    return [[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]]