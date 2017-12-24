#coding=utf8

import os
import sys
from collections import defaultdict
import pdb


def load_data_info(dict_file):
    info = []
    with open(dict_file, "r") as fdict:
        for line in fdict:
            if not "".join(line.split()): continue
            line_split = line.strip().split(",")
            info.append(
                [line_split[0],
                 int(line_split[1]),
                 int(line_split[2])])
    return info


def load_data(data_file, data_info):
    samples = []
    with open(data_file, "r") as fdata:
        for idx, line in enumerate(fdata):
            line_split = line.strip().split("\t")
            if len(line_split) != len(data_info):
                print("error line %d" % (idx + 1))

            # useful_info = [line_split[0]]
            useful_info = [line_split[0]]
            for i, ls in enumerate(line_split[1:]):
                if data_info[i + 1][1]:
                    if (data_info[i + 1][2] == 1
                        ) or data_info[i + 1][2] == 0:  # str
                        useful_info.append(ls)
                    elif data_info[i + 1][2] == 2:
                        if ls.decode("utf8") == "无".decode("utf8"):
                            useful_info.append(0)
                        else:
                            useful_info.append(
                                int(
                                    ls.replace(',',
                                               '').rstrip("\"").lstrip("\"")
                                    .replace("\xc2\xa0", "")))
            samples.append(useful_info)
            useful_info = []
    return samples


def norm_categorical_feature(samples, i, for_test):
    print("fea %d" % i)
    word_dict = {}
    if not for_test:
        feature_dict = defaultdict(int)
        for sample in samples:
            key = "".join(sample[i].split())
            if not key: continue
            feature_dict[key] += 1

        if i == 1 or i == 7:
            feature_dict["<unk>"] = 99999
        sorted_dict = sorted(
            feature_dict.iteritems(), key=lambda x: x[1], reverse=True)

        with open("processed/fea_%02d.txt" % (i), "w") as fdict:
            for idx, item in enumerate(sorted_dict):
                word_dict[item[0]] = idx
                fdict.write("%s\t%d\n" % (item[0], item[1]))
    else:
        with open("processed/fea_%02d.txt" % (i), "r") as fdict:
            for idx, line in enumerate(fdict):
                word_dict[line.strip().strip().split("\t")[0]] = idx

    for sample in samples:
        if sample[i] in word_dict:
            sample[i] = str(word_dict[sample[i]])
        else:
            if "<unk>" in word_dict:
                sample[i] = str(word_dict["<unk>"])
            else:
                print("Error")


def norm_numerical_feature(samples, i, for_test):
    max_value = -1.
    if for_test:
        max_value = int(
            open("processed/fea_%02d.txt" % (i), "r").readline().strip())
    else:
        for sample in samples:
            if sample[i] > max_value:
                max_value = sample[i]

        with open("processed/fea_%02d.txt" % (i), "w") as fdict:
            fdict.write("%d" % (max_value))

    for sample in samples:
        sample[i] = str(float(sample[i]) / max_value)


def norm_feature(samples, for_test):
    feature_num = len(samples[0])

    for i in range(1, feature_num):
        if isinstance(samples[0][i], str):
            norm_categorical_feature(samples, i, for_test)
        else:
            norm_numerical_feature(samples, i, for_test)
    return samples


def process_dir(src, for_test=False):
    for file_name in os.listdir(src):
        process_file(os.path.join(src, file_name), for_test)


def process_file(in_name, for_test):
    name = os.path.splitext(os.path.split(in_name)[1])[0]

    data_info = load_data_info("train_info.txt")
    samples = load_data(in_name, data_info)

    normalized = norm_feature(samples, for_test)

    with open("%s_normalized_dev.txt" % (name), "w") as fout:
        for sample in samples:
            fout.write("%s\n" % ("\t".join(sample)))


def make_pairs(data_file, save_name):
    samples = []
    with open(data_file, "r") as fin:
        for line in fin:
            samples.append("###".join(line.strip().split("\t")))

    with open(save_name, "w") as fout:
        for i in range(len(samples)):
            for j in range(i + 1, len(samples)):
                fout.write("%s\t%s\n" % (samples[i], samples[j]))


if __name__ == "__main__":
    process_file("exported/top_400.txt", for_test=True)
    process_file("exported/19000data.txt", for_test=True)

    # make_pairs("1_normalized_dev.txt", "pairs_train.txt")

    # process_file("2.txt", for_test=True)
    # make_pairs("2_normalized_dev.txt", "pairs_eval.txt")
    # process_dir("raw")

    # process_dir("raw", for_test=True)
