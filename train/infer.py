#coding=utf8
import os
import sys
import gzip
import pdb
import math
import numpy as np
from openpyxl import Workbook

import paddle.v2 as paddle
import reader
from network import half_ranknet


def norm_score(x):
    return int(1. / (1 + math.exp(-x)) * 1000)


def get_file_name(file_path):
    return os.path.splitext(os.path.split(file_path)[1])[0]


def gen_report(predictions, raw_file, data_info):
    fn = get_file_name(raw_file)

    raw_sample = {}
    with open(raw_file, "r") as fin:
        for line in fin:
            line_split = line.strip().split("\t")
            raw_sample[line_split[0]] = line.strip()

    res_file = Workbook()
    res_sheet = res_file.create_sheet(0)
    res_sheet.title = u"模型打分"

    idx = 1
    res_sheet["A%d" % idx] = u"分值"
    res_sheet["B%d" % idx] = u"来源"

    titles = open(data_info, "r").readlines()
    for i, title in enumerate(titles):
        res_sheet["%s%d" % (chr(ord("C") + i), idx)] = title.split(",")[0]

    idx += 1
    for p in predictions:
        res_sheet["A%d" % (idx)] = "%f" % (p[0][0])
        res_sheet["B%d" % (idx)] = u"起点"

        for i, context in enumerate(raw_sample[p[1]].split("\t")):
            res_sheet["%s%d" % (chr(ord("C") + i), idx)] = context
        idx += 1

    res_file.save(fn + "_scores.xlsx")


def infer(model_path, test_data, batch_size):
    assert os.path.exists(model_path), "The trained model does not exist."
    # feature_dim = 18
    feature_dim = 7

    parameters = paddle.parameters.Parameters.from_tar(gzip.open(model_path))
    inferer = paddle.inference.Inference(
        output_layer=half_ranknet("infer", feature_dim), parameters=parameters)

    test_batch = []
    info = []
    scores = []
    for idx, item in enumerate(reader.test_reader(test_data)()):
        test_batch.append([item[0]])
        info.append(item[1])

        if len(test_batch) == batch_size:
            scores += inferer.infer(input=test_batch, field=["value"]).tolist()
            test_batch = []

    if len(test_batch):
        scores += inferer.infer(input=test_batch, field=["value"]).tolist()
        test_batch = []
    return zip(scores, info)


if __name__ == '__main__':
    paddle.init(use_gpu=False, trainer_count=1)
    # infer("models/ranknet_params_25.tar.gz",
    #       "../preprocess/processed/train_test/test_normed.txt", 16)

    # raw_file = "../preprocess/data/12_07/exported/all_data.txt"
    # proc_file = "../preprocess/data/12_07/all_data.txt"
    # data_info = "../preprocess/data/12_07/train_info.txt"

    # proc_file = ("../preprocess/data/12_14/"
    #             "qidian_add_missing_fea_normalized_dev.txt")
    # raw_file = ("../preprocess/data/12_14/raw/qidian_add_missing_fea.txt")
    # data_info = "../preprocess/data/12_14/train_info.txt"

    # proc_file = ("/Users/ying/Documents/codes/rank_ip/preprocess/data/12_07/"
    #              "top_400_normalized_dev.txt")
    # raw_file = ("/Users/ying/Documents/codes/rank_ip/preprocess/"
    #             "data/12_07/exported/top_400.txt")

    # proc_file = ("/Users/ying/Documents/codes/rank_ip/preprocess/data/12_07/"
    #              "19000data_normalized_dev.txt")
    # raw_file = ("/Users/ying/Documents/codes/rank_ip/preprocess/"
    #             "data/12_07/exported/19000data.txt")

    # predictions = infer(
    #     "trained_models/11_28/models/ranknet_params_3800.tar.gz", proc_file, 1)
    # predictions = infer(
    #     "trained_models/11_28/models/ranknet_params_7200.tar.gz", proc_file, 1)
    # gen_report(predictions, raw_file, data_info)
