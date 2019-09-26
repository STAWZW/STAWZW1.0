import tensorflow as tf
from alexnet import alexnet
import numpy as np
import sys

class_name = ['changyan', 'baiban', 'hongtui']
result = {}
result['changyan'] = '肠炎病'
result['hongtui'] = '红腿病'
result['baiban'] = '白斑综合症'
def test_image(path_image):
    img_string = tf.read_file(path_image)
    img_decoded = tf.image.decode_png(img_string, channels=3)
    img_resized = tf.image.resize_images(img_decoded, [227, 227])
    img_resized = tf.reshape(img_resized, shape=[1, 227, 227, 3])
    fc8 = alexnet(img_resized, 1, 3)
    score = tf.nn.softmax(fc8)
    max_prod = np.max(score)
    max = tf.argmax(score, 1)
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, "./tmp/checkpoints/model_epoch17.ckpt")
        gl = sess.run(max_prod).flatten().tolist()
        print(gl)
        print('["肠炎病", "白斑综合症", "红腿病"]')
        prob = sess.run(max)[0]

# test_image('F:/Anaconda3-5.3/SpyderWork/diseasePhoto/changyans/010.jpeg')
# test_image('D:/pythonApp/PythonApp/PythonImageModel/tensorflow_alexnet_classify-master/1.jpg')
if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        url = sys.argv[i]
        test_image(url)
