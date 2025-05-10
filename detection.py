import cv2
import numpy as np
import tflite_runtime.interpreter as tflite

class Detector:
    def __init__(self, model_path):
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def detect(self, frame):
        input_shape = self.input_details[0]['shape']
        input_tensor = cv2.resize(frame, (input_shape[2], input_shape[1]))
        input_tensor = np.expand_dims(input_tensor, axis=0).astype(np.uint8)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_details[0]['index'])
