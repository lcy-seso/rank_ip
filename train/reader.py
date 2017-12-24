import os
import pdb


def train_reader(data_path):
    def reader():
        with open(data_path, "r") as f:
            for line in f:
                pos, neg = line.strip().split("\t")
                pos_fea = map(float, pos.split("###")[1:])
                neg_fea = map(float, neg.split("###")[1:])
                yield pos_fea, neg_fea, [1.]

    return reader


def train_reader_12_24(data_path):
    def reader():
        with open(data_path, "r") as f:
            for line in f:
                pos, neg = line.strip().split("\t")
                pos_fea = map(float, pos.split()[1:])
                neg_fea = map(float, neg.split()[1:])
                yield pos_fea, neg_fea, [1.]

    return reader


def test_reader(data_path):
    def reader():
        with open(data_path, "r") as f:
            for line in f:
                feat = line.strip().split("\t")
                # yield map(float, feat[1:]), feat[0], feat[-1]
                yield map(float, feat[1:]), feat[0]

    return reader


if __name__ == "__main__":
    for idx, sample in enumerate(
            train_reader("../preprocess/data/11_28/train/pairs_train.txt")()):
        print sample
        if idx > 5: break
