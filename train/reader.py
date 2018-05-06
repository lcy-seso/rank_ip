import os
import pdb


def train_reader(data_path):
    def reader():
        with open(data_path, "r") as f:
            for line in f:
                pos, neg = line.strip().split("\t")
                pos_fea = map(float, pos.split("##"))
                neg_fea = map(float, neg.split("##"))
                yield pos_fea, neg_fea, [1.]

    return reader


def train_reader_12_24(data_path):
    def reader():
        with open(data_path, "r") as f:
            print data_path
            for idx, line in enumerate(f):
                try:
                    pos, neg = line.strip().split("\t")
                    pos_fea = map(float, pos.split()[1:])
                    neg_fea = map(float, neg.split()[1:])
                    yield pos_fea, neg_fea, [1.]
                except:
                    print idx

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
            train_reader(
                ("/Users/ying/Documents/codes/rank_ip/preprocess/data/"
                 "2018_05_05/processed/train.txt.shuf"))()):
        print(sample)
        if idx > 5: break
