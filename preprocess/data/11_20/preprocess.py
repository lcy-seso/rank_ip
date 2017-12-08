#!/usr/bin/env python
#coding=utf-8

import os
import logging
import pdb
import random

from collections import defaultdict

logger = logging.getLogger("info")
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.DEBUG)


def delete_invalid_data(src, dst):
    with open(src, "r") as fin, \
            open(dst, "w") as fout:
        for idx, line in enumerate(fin):
            line_split = line.strip().split("\t")

            labels = line_split[-1].split("|")
            status = []
            for lab in labels:
                if not lab: continue
                if lab.split(",")[-1] == "-1":
                    status.append(0)
                else:
                    status.append(1)
            if sum(status) == 0: continue
            fout.write(line)


def split_train_and_test(raw_data, save_dir="processed/train_test"):
    """  generate random train list
    list_id = set()
    with open(raw_data, "r") as fin:
        for idx, line in enumerate(fin):
            list_id.add(line.strip().split("\t")[-1].split("|")[0].split(",")[
                0])

    test = set(random.sample(list(list_id), 2))
    train = list_id
    with open(os.path.join(save_dir, "train_list.txt"), "w") as ftrain, \
            open(os.path.join(save_dir, "test_list.txt"), "w") as ftest:
        for item in train:
            ftrain.write("%s\n" % (item))
        for item in test:
            ftest.write("%s\n" % (item))
    """

    test_list = [
        int(i.strip())
        for i in open("processed/train_test/test_list.txt", "r").readlines()
    ]

    with open(raw_data, "r") as fin, \
            open(os.path.join(save_dir, "train.txt"), "w") as ftrain, \
            open(os.path.join(save_dir, "test.txt"), "w") as ftest:
        for line in fin:
            list_id = int(line.strip().split("\t")[-1].split("|")[0].split(",")
                          [0])
            if list_id in test_list:
                ftest.write(line)
            else:
                ftrain.write(line)


def load_fea_dict(dict_path):
    feat_dict = []
    with open(dict_path, "r") as fin:
        for idx, line in enumerate(fin):
            if idx > 18: break
            key, value = line.strip().split(",")
            if idx:
                feat_dict.append([key, int(value)])
            else:
                feat_dict.append([key, value])
    return feat_dict


def normalize_numerical_fea(col_idx, fea_info_save_path, samples):
    max_value = 0.0
    if fea_info_save_path is not None:
        for idx, sample in enumerate(samples):
            try:
                if sample[col_idx] != "NULL" and float(sample[
                        col_idx]) > max_value:
                    max_value = float(sample[col_idx])
            except:
                logger.info("error sample %d : %s" %
                            (idx, samples[idx][col_idx]))
        fout = open(fea_info_save_path, "w")
        fout.write("%f\n" % (max_value))
    else:
        max_value = float(
            open("processed/train_test/fea_%03d.txt" % (col_idx), "r")
            .readline().strip())

    for idx, sample in enumerate(samples):
        try:
            if sample[col_idx] == "NULL":
                sample[col_idx] = "-1"
            else:
                sample[col_idx] = str(
                    float(sample[col_idx]) / float(max_value))
        except:
            sample[col_idx] = "-1"


def normalize_categorical_fea(col_idx, fea_dict_save_path, samples):
    feat_dict = defaultdict(int)
    if fea_dict_save_path is not None:
        for idx, sample in enumerate(samples):
            feat_dict[sample[col_idx]] += 1
        sorted_dict = sorted(
            feat_dict.iteritems(), key=lambda x: x[1], reverse=True)
        with open(fea_dict_save_path, "w") as fdict:
            for key, value in sorted_dict:
                fdict.write("%s\t%d\n" % (key, value))
        feat_dict = {}
        for idx, item in enumerate(sorted_dict):
            feat_dict[item[0]] = idx
    else:
        with open("processed/train_test/fea_%03d.txt" % (col_idx), "r") as fin:
            for idx, line in enumerate(fin):
                feat_dict[line.strip().split("\t")[0]] = idx

    for sample in samples:
        sample[col_idx] = str(feat_dict[sample[col_idx]])


def normalize(data_path, feat_dict, save_dir, norm_on_self=True):
    feat_dict = load_fea_dict(feat_dict)
    samples = []
    with open(data_path, "r") as fin:
        for idx, line in enumerate(fin):
            line_split = line.strip().split("\t")
            if len(line_split) != 20: continue
            samples.append(line_split)

    for i in range(1, len(feat_dict)):
        logger.info("processing feature %d" % (i))
        if feat_dict[i][-1] == 1:  # numerical feature
            normalize_numerical_fea(i,
                                    (os.path.join(save_dir, "fea_%03d.txt" % i)
                                     if norm_on_self else None), samples)

        elif feat_dict[i][-1] == 2:  # categorical feature
            normalize_categorical_fea(i, (
                os.path.join(save_dir, "fea_%03d.txt" % i)
                if norm_on_self else None), samples)

    file_name = os.path.split(os.path.splitext(data_path)[0])[-1]
    with open(os.path.join(save_dir, file_name + "_normed.txt"), "w") as fout:
        for sample in samples:
            labels = sample[-1].rstrip("|").split("|")
            for lab in labels:
                fout.write("%s\t%s\n" % ("\t".join(sample[:-1]), lab))


def make_pairs(raw_data_path, pairs_save_path):
    samples = defaultdict(list)
    with open(raw_data_path, "r") as fin:

        for line in fin:
            line_split = line.strip().split("\t")
            list_id, rank = line_split[-1].split(",")
            rank = int(rank)
            if rank == -1: continue
            samples[list_id].append(line_split[:-1] + [str(rank)])

    for key in samples:
        samples[key].sort(key=lambda x: x[-1], reverse=True)

    with open(pairs_save_path, "w") as fout:
        for key in samples:
            inputs = samples[key]
            total_samples = len(inputs)
            for i in range(total_samples):
                for j in range(i + 1, total_samples):
                    fout.write("%s\t%s\n" %
                               ("@@@".join(inputs[i]), "@@@".join(inputs[j])))


if __name__ == "__main__":
    # delete_invalid_data("data/raw_data.txt", "processed/valid_inputs.txt")
    # split_train_and_test(
    #     "data/res.txt", save_dir="processed/train_test")

    # normalize("processed/train_test/train.txt", "data/feature.txt",
    #           "processed/train_test/")

    # normalize(
    #     "processed/train_test/test.txt",
    #     "data/feature.txt",
    #     "processed/train_test/",
    #     norm_on_self=False)

    # make_pairs(
    #     raw_data_path="processed/train_test/train_normed.txt",
    #     pairs_save_path="processed/train_test/train_pairs.txt")
