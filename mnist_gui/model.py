import tensorflow as tf
import numpy as np


def prediction(test_data):
    """ 进行模型训练与预测 """
    is_train = False

    # 数据准备
    mnist = tf.keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    # 将数据后增加一维使其适应CNN模型
    train_images = train_images.reshape((60000, 28, 28, 1))
    test_images = test_images.reshape((10000, 28, 28, 1))

    # 设置训练参数
    train_epochs = 5  # 训练轮数
    batch_size = 100  # 单次训练样本数（批次大小）

    # 数据归一化
    train_images = train_images / 255.0
    test_images = test_images / 255.0

    if is_train:

        # 建立模型
        model = tf.keras.models.Sequential()

        model.add(tf.keras.layers.Conv2D(32, (5, 5), activation='relu', input_shape=(28, 28, 1)))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))

        model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))

        model.add(tf.keras.layers.Flatten())

        model.add(tf.keras.layers.Dense(256, activation='relu'))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(10, activation='softmax'))

        # 定义训练模式
        model.compile(optimizer='adam',  # 传递优化器实例
                      loss='sparse_categorical_crossentropy',  # 传递用于判断的损失函数
                      metrics=['accuracy'])  # 监控训练

        # 训练模型
        model.fit(train_images, train_labels,
                  # validation_split=0.2,
                  epochs=train_epochs,
                  batch_size=batch_size,
                  verbose=2)

        model.save('model')

    else:
        model = tf.keras.models.load_model('model')

    # 评估模型
    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('Test accuracy:', test_acc)
    print('Test loss:', test_loss)

    # 进行预测并输出结果
    predictions = model.predict(test_data)
    output = str()
    num = int(predictions.shape[0])
    for i in range(num):
        output += str(np.argmax(predictions[i]))

    return output
