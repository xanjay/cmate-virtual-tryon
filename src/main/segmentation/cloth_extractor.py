import os
from io import BytesIO
import tarfile
import tempfile
from six.moves import urllib

from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image

# %tensorflow_version 1.x
import tensorflow as tf

# define globals
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

MODEL_NAME = 'frozen_inference_graph-110871.pb'
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)


LABEL_NAMES = np.asarray(['BG', 'short_sleeved_shirt', 'long_sleeved_shirt',
                          'short_sleeved_outwear', 'long_sleeved_outwear',
                          'vest', 'sling', 'shorts', 'trousers', 'skirt', 'short_sleeved_dress',
                          'long_sleeved_dress', 'vest_dress', 'sling_dress'])

FULL_LABEL_MAP = np.arange(1, len(LABEL_NAMES)+1).reshape(len(LABEL_NAMES), 1)
# print(FULL_LABEL_MAP)


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = (513, 513)  # hxw

    def __init__(self, model_file):
        """Creates and loads pretrained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        # load model
        with open(model_file, 'rb') as f:
            graph_def = tf.GraphDef.FromString(f.read())

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in given path.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
          image: A PIL.Image object, raw input image.

        Returns:
          resized_image: RGB image resized from original input image.
          seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE[1] / max(width, height)
        target_size = (int(resize_ratio * width),
                       int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(
            target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map


def vis_segmentation(image, seg_map):
    """Visualizes input image, segmentation map and overlay view."""
    plt.figure(figsize=(10, 8)) # (w,h)
    grid_spec = gridspec.GridSpec(2, 3, width_ratios=[7,7,1])

    plt.subplot(grid_spec[0,0])
    plt.imshow(image)
    plt.axis('off')
    plt.title('input image')

    plt.subplot(grid_spec[0,1])
    plt.imshow(seg_map)
    plt.axis('off')
    plt.title('segmentation map')

    image_array = np.asarray(image)
    seg_image = np.zeros(image_array.shape, dtype='int32')
    mask = np.where(seg_map==5)
    seg_image[mask] = image_array[mask]
    plt.subplot(grid_spec[1,0])
    plt.imshow(seg_image, interpolation='nearest')
    plt.axis('off')
    plt.title('segmentation image')

    plt.subplot(grid_spec[1,1])
    plt.imshow(image)
    plt.imshow(seg_map, alpha=0.7)
    plt.axis('off')
    plt.title('segmentation overlay')

    unique_labels = np.unique(seg_map)
    # print(unique_labels)
    ax = plt.subplot(grid_spec[1,2])
    plt.imshow(
        FULL_LABEL_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
    ax.yaxis.tick_right()
    plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
    plt.xticks([], [])
    ax.tick_params(width=0.0)
    plt.grid('off')
    plt.show()


"""## Select a pretrained model
We have trained the DeepLab model using various backbone networks. Select one from the MODEL_NAME list.
"""

TEST_IMAGES = ["C:\\Users\\sanja\\Desktop\\pose_test\\" +
               item for item in os.listdir("C:\\Users\\sanja\\Desktop\\pose_test")]

IMAGE_URL = TEST_IMAGES[2]


def run_visualization(image_path):
    """Inferences DeepLab model and visualizes result."""
    try:
        original_im = Image.open(image_path)
    except Exception:
        print('Cannot retrieve image: ' + image_path)
        return

    MODEL = DeepLabModel(MODEL_PATH)

    print('running deeplab on image %s...' % image_path)
    resized_im, seg_map = MODEL.run(original_im)
    print(resized_im.size, seg_map.shape)
    
    # set al upper clothes as vest
    seg_map[(seg_map>0)&(seg_map<7)] = 5 # 1-6
    seg_map[(seg_map>9)&(seg_map<15)] = 5 # 10-14

    vis_segmentation(resized_im, seg_map)


# image_url = IMAGE_URL
# run_visualization(image_url)

def extract_cloth(image_path):
    """Inferences DeepLab model and return cloth segmentation."""
    MODEL = DeepLabModel(MODEL_PATH)
    print('deeplab model loaded successfully!')
    try:
        original_im = Image.open(image_path)
    except Exception:
        print('Cannot retrieve image: ' + image_path)
        return

    print('running deeplab on image %s...' % image_path)
    resized_im, seg_map = MODEL.run(original_im)
    
    # set all upper clothes as vest
    seg_map[(seg_map>0)&(seg_map<7)] = 5 # 1-6
    seg_map[(seg_map>9)&(seg_map<15)] = 5 # 10-14

    # extract cloth
    resized_img = np.asarray(resized_im)
    seg_image = np.zeros(resized_img.shape, dtype='uint8')
    mask = np.where(seg_map==5)
    seg_image[mask] = resized_img[mask]

    return resized_img, seg_image
