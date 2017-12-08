import pdb
import os
import sys
import gzip

import paddle.v2 as paddle
import reader
from network import ranknet


def train_ranknet(num_passes, save_dir):
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    # train_data_path = "../preprocess/processed/train_test/train_pairs.txt"
    train_data_path = "../preprocess/data/11_28/train/pairs_train.txt"
    eval_data_path = "../preprocess/data/11_28/train/pairs_eval.txt"

    feature_dim = 8

    train_reader = paddle.batch(
        paddle.reader.shuffle(
            reader.train_reader(train_data_path), buf_size=102400),
        batch_size=24000)
    test_reader = paddle.batch(
        paddle.reader.shuffle(
            reader.train_reader(eval_data_path), buf_size=102400),
        batch_size=24000)

    cost = ranknet(feature_dim)
    parameters = paddle.parameters.create(cost)

    trainer = paddle.trainer.SGD(
        cost=cost,
        parameters=parameters,
        update_equation=paddle.optimizer.Adam(learning_rate=2e-4))

    def event_handler(event):
        if isinstance(event, paddle.event.EndIteration):
            if event.batch_id % 100 == 0:
                print "Pass %d Batch %d Cost %.9f" % (
                    event.pass_id, event.batch_id, event.cost)
                result = trainer.test(reader=test_reader)
                print("Test at Batch %d, %s \n" % (event.pass_id, result.cost))

        if isinstance(event, paddle.event.EndPass) and not event.pass_id % 50:
            with gzip.open(
                    os.path.join(save_dir, "ranknet_params_%d.tar.gz" %
                                 (event.pass_id)), "w") as f:
                trainer.save_parameter_to_tar(f)

    trainer.train(
        reader=train_reader,
        event_handler=event_handler,
        num_passes=num_passes)


if __name__ == '__main__':
    paddle.init(use_gpu=False, trainer_count=11)
    train_ranknet(num_passes=50000, save_dir="models")
