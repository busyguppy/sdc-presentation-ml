from keras.callbacks import Callback


class TestCallback(Callback):
    def __init__(self, test_data):
        self.test_data = test_data

    def on_epoch_end(self, epoch, logs=None):
        x, y = self.test_data
        test_result = self.model.evaluate(x, y, verbose=0)
        if epoch == 0:
            self.model.history.history['test_loss'] = []
            self.model.history.history['test_accuracy'] = []
        self.add_to_history(test_result)
        t = 1

    def add_to_history(self, test_result):
        test_loss, test_acc = test_result
        self.model.history.history['test_loss'].append(test_loss)
        self.model.history.history['test_accuracy'].append(test_acc)
