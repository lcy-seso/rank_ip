import pdb
import os
import sys
import gzip
import logging

import paddle.v2 as paddle
import reader
from network import ranknet


def get_logger(log_file_name):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file_name)
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def train_ranknet(num_passes, save_dir):
    logger = get_logger("train_01_13.log")
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    train_data_path = ("/Users/ying/Documents/codes/rank_ip/preprocess/data/"
                       "2018_05_05/processed/train.txt.shuf")

    feature_dim = 7
    train_reader = paddle.batch(
        paddle.reader.shuffle(
            reader.train_reader(train_data_path), buf_size=10240),
        batch_size=400)

    cost = ranknet(feature_dim)
    parameters = paddle.parameters.create(cost)

    trainer = paddle.trainer.SGD(
        cost=cost,
        parameters=parameters,
        update_equation=paddle.optimizer.AdaGrad(
            learning_rate=3e-3,
            regularization=paddle.optimizer.L2Regularization(rate=1e-3)))

    def event_handler(event):
        if isinstance(event, paddle.event.EndIteration):
            if event.batch_id % 1000 == 0:
                logger.info("Pass %d Batch %d Cost %.9f" %
                            (event.pass_id, event.batch_id, event.cost))
                with gzip.open(
                        os.path.join(
                            save_dir,
                            "ranknet_params_pass_%02d_batch_%05d.tar.gz" %
                            (event.pass_id, event.batch_id)), "w") as f:
                    trainer.save_parameter_to_tar(f)

        if isinstance(event, paddle.event.EndPass):
            with gzip.open(
                    os.path.join(save_dir, "ranknet_params_%05d.tar.gz" %
                                 (event.pass_id)), "w") as f:
                trainer.save_parameter_to_tar(f)

    trainer.train(
        reader=train_reader,
        event_handler=event_handler,
        num_passes=num_passes)


if __name__ == "__main__":
    paddle.init(use_gpu=False, trainer_count=4)
    train_ranknet(num_passes=50000, save_dir="models_05_05")
