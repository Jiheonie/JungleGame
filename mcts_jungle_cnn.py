import numpy as np
import argparse
import h5py
from dljungle.agent import pg
from dljungle.encoders.base import get_encoder_by_name
from keras.api.models import Sequential
from keras.api.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
# from large import layers
from cnn.medium import layers
# from small import layers


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('output_file')
  args = parser.parse_args()
  output_file = args.output_file

  np.random.seed(1)

  X = np.load('features12000.npy')
  Y = np.load('labels12000.npy')

  samples = X.shape[0]

  board_size = 9 * 7

  X = X.reshape(samples, 9, 7, 5)
  Y = Y.reshape(samples, board_size * 4)

  train_samples = int(0.9 * samples)
  X_train, X_test = X[:train_samples], X[train_samples:]
  Y_train, Y_test = Y[:train_samples], Y[train_samples:]

  model = Sequential()
  model.add(Conv2D(32, kernel_size=(3, 3),
                  activation='relu',
                  input_shape=(9, 7, 5)))
  for layer in layers((9, 7, 5)):
    model.add(layer=layer)
  model.add(Dense(9 * 7 * 4, activation='softmax'))
  model.summary()

  model.compile(loss='categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])

  model.fit(X_train, Y_train, 
            batch_size=64, 
            epochs=25, 
            verbose=1, 
            validation_data=(X_test, Y_test))

  score = model.evaluate(X_test, Y_test, verbose=0)

  print('Test loss: ', score[0])
  print('Test accuracy: ', score[1])

  encoder = get_encoder_by_name('oneplane')

  new_agent = pg.PolicyAgent(model, encoder)

  with h5py.File(output_file, 'w') as outf:
    new_agent.serialize(outf)


if __name__ == '__main__':
  main()