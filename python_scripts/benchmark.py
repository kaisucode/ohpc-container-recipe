
import argparse
import tensorflow as tf
from tensorflow import keras
import numpy as np
import time

def preprocess(): 
    (X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()

    X_train_scaled = X_train/255
    X_test_scaled = X_test/255

    y_train_encoded = keras.utils.to_categorical(y_train, num_classes=10, dtype='float32')
    y_test_encoded = keras.utils.to_categorical(y_test, num_classes=10, dtype='float32')
    return X_train_scaled, y_train_encoded

def concat_data(x, y, val): 
    return x[:val], y[:val]

def benchmark_model(a_model, args): 
    startTime = time.perf_counter()
    hist = a_model.fit(X_train_scaled, y_train_encoded, epochs=args.num_epochs)
    elapsed_time = time.perf_counter() - startTime
    best_accuracy = hist.history['accuracy'][np.argmin(hist.history['loss'])]
    return elapsed_time, best_accuracy

def parseArguments(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_epochs", type=int, default=10)
    parser.add_argument("--num_data", type=int, default=50)
    parser.add_argument("--is_gpu", action="store_true")
    parser.add_argument("--has_two_gpu", action="store_true")
    args = parser.parse_args()
    return args


def log_info(model_name, elapsed_time, best_accuracy): 
    ret_str = [
            "model_name: {}\n".format(model_name),
            "elapsed_time: {}\n".format(elapsed_time),
            "best_accuracy: {:.2%}\n".format(best_accuracy),
            "---------------\n"
            ]
    return "".join(ret_str)

def get_custom_model(): 

    a_model = keras.models.Sequential()

    a_model.add(tf.keras.layers.Conv2D(filters=128,kernel_size=3,padding="same", activation="relu", input_shape=[32,32,3]))
    a_model.add(tf.keras.layers.Conv2D(filters=128,kernel_size=3,padding="same", activation="relu", input_shape=[32,32,3]))
    a_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    a_model.add(tf.keras.layers.Conv2D(filters=256,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.Conv2D(filters=256,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    a_model.add(tf.keras.layers.Conv2D(filters=1024,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.Conv2D(filters=1024,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    a_model.add(tf.keras.layers.Conv2D(filters=512,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.Conv2D(filters=512,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.Conv2D(filters=512,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    a_model.add(tf.keras.layers.Conv2D(filters=64,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.Conv2D(filters=64,kernel_size=3,padding="same", activation="relu"))
    a_model.add(tf.keras.layers.MaxPool2D(pool_size=2,strides=2,padding='valid'))
    a_model.add(tf.keras.layers.Flatten())
    a_model.add(tf.keras.layers.Dropout(0.5,noise_shape=None,seed=None))
    a_model.add(tf.keras.layers.Dense(units=128,activation='relu'))
    a_model.add(tf.keras.layers.Dense(units=10,activation='softmax'))

    print(a_model.summary())
    return a_model

def load_models(): 
    model_list = {
            #  "custom_model": get_custom_model(),
            "resnet101": tf.keras.applications.resnet.ResNet101(weights=None, input_shape=(32, 32, 3), classes=10),
            "resnet152": tf.keras.applications.resnet.ResNet152(weights=None, input_shape=(32, 32, 3), classes=10),
            "vgg16": tf.keras.applications.VGG16(weights=None, input_shape=(32, 32, 3), classes=10),
            #  "resnet50": tf.keras.applications.ResNet50(weights=None, input_shape=(32, 32, 3), classes=10),
            }

    for model_name in model_list: 
        model_list[model_name].compile(optimizer='SGD',
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    return model_list


if __name__ == "__main__": 

    logs = ""
    args = parseArguments()

    X_train_scaled, y_train_encoded = concat_data(*preprocess(), args.num_data)

    if args.has_two_gpu: 
        print("Benchmarking with two GPUs")

        mirrored_strategy = tf.distribute.MirroredStrategy(devices=["/GPU:0", "/GPU:1"])
        print("Number of devices: {}".format(mirrored_strategy.num_replicas_in_sync))

        compiled_model_list = {}
        with mirrored_strategy.scope():
            model_list = load_models()
        for model_name in model_list: 
            elapsed_time, best_accuracy = benchmark_model(model_list[model_name], args)
            logs += log_info(model_name, elapsed_time, best_accuracy)
            print(logs)

    elif args.is_gpu: 
        print("Benchmarking with GPU")
        with tf.device('/GPU:0'):
            model_list = load_models()
            for model_name in model_list: 
                elapsed_time, best_accuracy = benchmark_model(model_list[model_name], args)
                logs += log_info(model_name, elapsed_time, best_accuracy)
                print(logs)
    else: 
        print("Benchmarking with CPU")
        with tf.device('/CPU:0'):
            model_list = load_models()
            for model_name in model_list: 
                elapsed_time, best_accuracy = benchmark_model(model_list[model_name], args)
                logs += log_info(model_name, elapsed_time, best_accuracy)
                print(logs)

    print(logs)


