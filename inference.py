import argparse
import time
import os

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


def search_user_by_plate(car_plate):
    conn = psycopg2.connect("host=109.120.191.148 dbname=PostgreSQL-4323 user=user password=0HD9E7L5A0410WYD")

    # Open a cursor to perform database operations
    cursor = conn.cursor()

    # Prepare the SELECT SQL query.
    query = """
        SELECT * FROM users WHERE car_plate = %s
    """

    # Execute the query with the given car plate.
    cursor.execute(query, (car_plate,))

    # Fetch the row from the result of the query
    row = cursor.fetchone()

    # If a row was found, print it out.
    if row is not None:
        result = False
    else:
        result = True

    # Close cursor and the connection
    cursor.close()
    conn.close()

    return result

def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-m1', '--model1', required=True,
                      help='File path of .tflite file')
  parser.add_argument('-m2', '--model2', required=True,
                      help='File path of .tflite file')
  parser.add_argument('-i', '--input', required=True,
                      help='File path of image to process')
  parser.add_argument('-l1', '--labels1', help='File path of labels file')
  parser.add_argument('-l2', '--labels2', help='File path of labels file')
  parser.add_argument('-t', '--threshold', type=float, default=0.4,
                      help='Score threshold for detected objects')
  parser.add_argument('-o', '--output',
                      help='File path for the result image with annotations')
  args = parser.parse_args()

labels1 = read_label_file(args.labels1) if args.labels1 else {}
labels2 = read_label_file(args.labels2) if args.labels2 else {}
interpreter = make_interpreter(args.model1)
interpreter.allocate_tensors()

while True:
    photo = getPhoto.get()
     _, scale = common.set_resized_input(
        interpreter,
        image.size,
        lambda size: image.resize(size, Image.ANTIALIAS))
    interpreter.invoke()
    objs = detect.get_objects(interpreter, args.threshold, scale)
    if not objs:
      print('No objects detected')
    else:
      for obj in objs:
        if obj.score > 0.3:
            cropped = photo.crop((bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax))
            interpreter = make_interpreter(args.model2)
            interpreter.allocate_tensors()
            _, scale = common.set_resized_input(
               interpreter,
               image.size,
               lambda size: image.resize(size, Image.ANTIALIAS))
            interpreter.invoke()
            objs = detect.get_objects(interpreter, args.threshold, scale)
            if len(objs) == 8 or len(objs) == 9:
                object_labels = []
                for obj in objs:
                    object_labels.append(obj.bbox.xmin, labels2.get(obj.id, obj.id))
                object_labels.sort()
                plate = ''
                for i in object_labels:
                    plate += i[1]
                if search_user_by_plate(plate):
                    barrier.open()
            
            interpreter = make_interpreter(args.model1)
            interpreter.allocate_tensors()



  
    
  
if __name__ == '__main__':
  main()