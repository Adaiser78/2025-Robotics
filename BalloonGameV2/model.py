import cv2
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common
from pycoral.adapters import classify


class Model:

    def __init__(self):
        self.interpreter = make_interpreter('model_files/model_edgetpu.tflite')
        self.interpreter.allocate_tensors()
        self.labels = read_label_file('model_files/labels.txt')

    def assess(self, image):

        frame = cv2.flip(image, 1)
        size = common.input_size(self.interpreter)
        common.set_input(self.interpreter, cv2.resize(image, size, fx=0, fy=0, interpolation=cv2.INTER_CUBIC))
        self.interpreter.invoke()
        results = classify.get_classes(self.interpreter)

        # Print prediction and confidence score
        print(f'Label: {self.labels[results[0].id]}, Score: {results[0].score}')
        # Check the confidence score of the model's decision. If greater than 90%, classify as a hit

        if (self.labels[results[0].id] == "hit") and (results[0].score >= 0.90):
            return True
        else:
            return False
