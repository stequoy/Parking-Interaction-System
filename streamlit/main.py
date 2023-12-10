from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import tflite_runtime.interpreter as tflite
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
import itertools
import cv2

import streamlit as st

def draw_objects(draw, objs, scale_factor, labels):
  """Draws the bounding box and label for each object."""
  # COLORS = np.random.randint(0, 255, size=(len(labels), 4), dtype=np.uint8)
  for obj in objs:
    bbox = obj.bbox
    # color = tuple(int(c) for c in COLORS[obj.id])
    draw.rectangle([(bbox.xmin * scale_factor, bbox.ymin * scale_factor),
                    (bbox.xmax * scale_factor, bbox.ymax * scale_factor)], width=3)
    # font = ImageFont.truetype(size=15)
    # draw.text((bbox.xmin * scale_factor + 4, bbox.ymin * scale_factor + 4),
    #           '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
    #           fill=color)

def draw_objects1(draw, objs, scale_factor, labels):
  """Draws the bounding box and label for each object."""
  # COLORS = np.random.randint(0, 255, size=(len(labels), 4), dtype=np.uint8)
  for obj in objs:
    bbox = obj.bbox
    # color = tuple(int(c) for c in COLORS[obj.id])
    draw.rectangle([(bbox.xmin * scale_factor, bbox.ymin * scale_factor),
                    (bbox.xmax * scale_factor, bbox.ymax * scale_factor)], width=3)
    # font = ImageFont.truetype(size=15)
    draw.text((bbox.xmin * scale_factor + 4, bbox.ymin * scale_factor + 4),
              '%s' % labels.get(obj.id, obj.id))


st.header('EfficientDet Visualisation')
st.subheader('This application allows you to test EfficentDet model trained to detect car plates.')
st.write('This model is used in the alternative approach of project to detect number plates to send them to the server.')
image = st.file_uploader(label='Upload your image', type=['.jpg'])

letters=['0' ,'1' ,'2','3' ,'4' ,'5', '6', '7', '8','9', 'A', 'B', 'C', 'E' ,'H','K', 'M','O', 'P', 'T', 'X', 'Y']

def decode_batch(out):
    ret = []
    for j in range(out.shape[0]):
        out_best = list(np.argmax(out[j, 2:], 1))
        out_best = [k for k, g in itertools.groupby(out_best)]
        outstr = ''
        for c in out_best:
            if c < len(letters):
                outstr += letters[c]
        ret.append(outstr)
    return ret



if image is not None:
    st.success('File successfully uploaded.')
    st.subheader('Uploaded image')
    st.image(image)
    st.subheader('Step 1: Detect a car plate')
    st.write('At this point model is used to detect a car plate in the image.')
    TFLITE_FILENAME1 = "efficientdet-lite-platev3.tflite"
    INPUT_IMAGE = image
    LABELS_FILENAME = 'plates-labels.txt'

    # Load the TF Lite model
    labels = read_label_file(LABELS_FILENAME)
    interpreter = tflite.Interpreter(TFLITE_FILENAME1)
    interpreter.allocate_tensors()

    # Resize the image for input
    image = Image.open(INPUT_IMAGE)
    _, scale = common.set_resized_input(
        interpreter, image.size, lambda size: image.resize(size, Image.Resampling.LANCZOS))

    # Run inference
    interpreter.invoke()
    objs = detect.get_objects(interpreter, score_threshold=0.4, image_scale=scale)

    # Resize again to a reasonable size for display
    display_width = 500
    scale_factor = display_width / image.width
    height_ratio = image.height / image.width
    image = image.resize((display_width, int(display_width * height_ratio)))
    draw_objects(ImageDraw.Draw(image), objs, scale_factor, labels)
    st.image(image)
    if len(objs) == 1:
        obj = objs[0]
        x0 = obj.bbox.xmin * scale_factor
        y0 = obj.bbox.ymin * scale_factor
        x1 = obj.bbox.xmax * scale_factor
        y1 = obj.bbox.ymax * scale_factor
        cropped = image.crop((x0, y0, x1, y1))
        st.subheader('Step 2: Cut the car plate from the main image')
        st.image(cropped, use_column_width=True)
        choice = st.selectbox(label='Model choise', options=['OCR: CRNN', 'EfficientDetLight (symbols)'])
        if choice == 'OCR: CRNN':
            CRNN_PATH = 'model1_nomer.tflite'
            interpreter = tflite.Interpreter(model_path=CRNN_PATH)
            interpreter.allocate_tensors()
            # Get input and output tensors.
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            img = np.asarray(cropped)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (128, 64))
            img = img.astype(np.float32)
            img /= 255

            img1 = img.T
            img1.shape
            X_data1 = np.float32(img1.reshape(1, 128, 64, 1))
            input_index = (interpreter.get_input_details()[0]['index'])
            interpreter.set_tensor(input_details[0]['index'], X_data1)

            interpreter.invoke()

            net_out_value = interpreter.get_tensor(output_details[0]['index'])
            pred_texts = decode_batch(net_out_value)
            st.subheader('Result of OCR')
            st.subheader(pred_texts[0])

        elif choice == 'EfficientDetLight (symbols)':
            TFLITE_FILENAME2 = 'efficientdet-lite-letters.tflite'
            LABELS_FILENAME2 = 'labelslet.txt'
            labels2 = read_label_file(LABELS_FILENAME2)
            interpreter2 = tflite.Interpreter(TFLITE_FILENAME2)
            interpreter2.allocate_tensors()

            # Resize the image for input
            image = cropped
            _, scale = common.set_resized_input(
                interpreter2, image.size, lambda size: image.resize(size, Image.Resampling.LANCZOS))

            # Run inference
            interpreter2.invoke()
            objs = detect.get_objects(interpreter2, score_threshold=0.20, image_scale=scale)
            display_width = 500
            scale_factor = display_width / image.width
            height_ratio = image.height / image.width
            image = image.resize((display_width, int(display_width * height_ratio)))
            draw_objects1(ImageDraw.Draw(image), objs, scale_factor, labels2)
            st.subheader('Results of EfficientDetLight (symbols)')
            st.image(image)
            for obj in objs:
                print(obj)
else:
    st.info('Please upload a file.')


