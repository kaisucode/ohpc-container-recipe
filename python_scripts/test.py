import tensorflow as tf

msg = tf.constant('Hello')
sess = tf.Session()
print(sess.run(msg))
