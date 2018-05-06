#!/usr/bin/env python
#coding=utf-8
from __future__ import division
import os
import random
import pdb
import re
from collections import defaultdict

FEA = [
    "title",
    "writer",
    "signed",
    "type",
    "word_count",
    "click",
    "like",
]


def get_filename(data_path):
    return os.path.split(os.path.splitext(data_path)[0])[1]


def to_utf8(data_dir):
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        os.popen("iconv -f GBK -t UTF8 -c <" + filepath + " >res")
        os.rename("res", filepath)


def format_chuangshizhongwen(data_path, save_dir):
    save_path = os.path.join(save_dir, get_filename(data_path) + ".txt")
    with open(data_path, "r") as fin, open(save_path, "w") as fout:
        for idx, line in enumerate(fin):
            if not idx: continue
            line_split = line.strip().split("\t")

            signed = "否"
            if "".join(line_split[3].split()) == "签约作品":
                signed = "是"

            fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                "".join(line_split[0].split()),  # title
                "".join(line_split[1].split()),  # writer
                signed,  # signed or not
                line_split[4],  # type
                float(line_split[5]),  # word_count
                float(line_split[6]),  # click
                float(line_split[9]),  # like
            ))


def format_hongxiutianxiang(data_path, save_dir):
    save_path = os.path.join(save_dir, get_filename(data_path) + ".txt")
    with open(data_path, "r") as fin, open(save_path, "w") as fout:
        for idx, line in enumerate(fin):
            if not idx: continue

            line_split = line.strip().split("\t")

            signed = "否"
            if line_split[4] == "签约":
                signed = "是"

            if "万字" in line_split[5]:
                word_count = float(line_split[5].replace("万字", "")) * 10000
            elif "字" in line_split[5]:
                word_count = float(line_split[5].replace("字", ""))
            else:
                word_count = float(line_split[5])

            if "万总点击" in line_split[7]:
                click = float(line_split[7].replace("万总点击", "")) * 10000
            elif "总点击" in line_split[7]:
                click = float(line_split[7].replace("总点击", ""))
            else:
                click = float(line_split[7])

            if "万总收藏" in line_split[6]:
                like = float(line_split[6].replace("万总收藏", "")) * 10000
            elif "总收藏" in line_split[6]:
                like = float(line_split[6].replace("总收藏", ""))
            else:
                like = float(line_split[6])

            fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                "".join(line_split[0].split()),  # 0, title
                "".join(line_split[1].split()),  # 1, writer
                signed,  # 2, signed or not
                line_split[3],  # 3. type
                word_count,  # 4, word_count
                click,  # 5, click
                like,  # 6, like
            ))


def format_jinjiang(data_path, save_dir="processed/formated"):
    save_path = os.path.join(save_dir, get_filename(data_path) + ".txt")
    with open(data_path, "r") as fin, open(save_path, "w") as fout:
        for idx, line in enumerate(fin):
            if not idx: continue
            line_split = line.strip().split("\t")

            try:
                signed = "否"
                if "".join(line_split[9].split()) == "已签约":
                    signed = "是"

                fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                    "".join(line_split[0].split()),  # title
                    "".join(line_split[1].split()),  # writer
                    signed,  # signed or not
                    line_split[3].split("-")[-1],  # type
                    float(line_split[4]),  # word_count
                    float(line_split[10]),  # click
                    float(line_split[5]),  # like
                ))
            except:
                fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                    "".join(line_split[0].split()),  # title
                    "".join(line_split[1].split()),  # writer
                    signed,  # signed or not
                    line_split[3].split("-")[-1],  # type
                    float(line_split[4]),  # word_count
                    0.,  # click
                    float(line_split[5]),  # like
                ))


def format_qidian(data_path, save_dir="processed/formated"):
    save_path = os.path.join(save_dir, get_filename(data_path) + ".txt")
    with open(data_path, "r") as fin, open(save_path, "w") as fout:
        for idx, line in enumerate(fin):
            if not idx: continue
            line_split = line.strip().split("\t")

            try:
                signed = "否"
                if "".join(line_split[3].split()) == "签约":
                    signed = "是"

                fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                    "".join(line_split[0].split()),  # title
                    "".join(line_split[1].split()),  # writer
                    signed,  # signed or not
                    line_split[4],  # type
                    0.,  # word_count
                    0.,  # click
                    0.,  # like
                ))
            except:
                print line


def format_zhangyue(data_path, save_dir="processed/formated"):
    def _to_float(string):
        pat = re.compile(r"[\d]+")
        n = float(pat.findall(string)[0])
        return n * 10000 if "万" in string else n

    save_path = os.path.join(save_dir, get_filename(data_path) + ".txt")
    with open(data_path, "r") as fin, open(save_path, "w") as fout:
        for idx, line in enumerate(fin):
            if not idx: continue
            line_split = line.strip().split("\t")

            try:
                signed = "否"
                if "".join(line_split[5].split()) in ["签约作品", "签约上架"]:
                    signed = "是"

                fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                    "".join(line_split[0].split()),  # title
                    "".join(line_split[1].split()),  # writer
                    signed,  # signed or not
                    line_split[4],  # type
                    _to_float(line_split[6]),  # word_count
                    _to_float(line_split[7]),  # click
                    _to_float(line_split[8]),  # like
                ))
            except:
                print line.strip()


def format_zongheng(data_path, save_dir="processed/formated"):
    save_path = os.path.join(save_dir, get_filename(data_path) + ".txt")
    with open(data_path, "r") as fin, open(save_path, "w") as fout:
        for idx, line in enumerate(fin):
            if not idx: continue
            line_split = line.strip().split("\t")

            try:
                signed = "是" if line_split[8] == "签约" else "否"

                fout.write("%s\t%s\t%s\t%s\t%.2f\t%.2f\t%.2f\n" % (
                    "".join(line_split[1].split()),  # title
                    "".join(line_split[2].split()),  # writer
                    signed,  # signed or not
                    line_split[9],  # type
                    float(line_split[10]),  # word_count
                    float(line_split[4]),  # click
                    float(line_split[7]),  # like
                ))
            except:
                print line.strip()


def format_raw():
    format_chuangshizhongwen("raw_data/01_chuangshizhongwenwang.txt",
                             "processed/formated")
    format_hongxiutianxiang("raw_data/02_hongxiutianxiang.txt",
                            "processed/formated")
    format_jinjiang("raw_data/03_jinjiang.txt")
    format_qidian("raw_data/04_qidian.txt")

    format_zhangyue("raw_data/05_zhangyue_gril.txt")
    format_zhangyue("raw_data/05_zhangyue_man.txt")

    format_zongheng("raw_data/06_zongheng_heipiao.txt")
    format_zongheng("raw_data/06_zongheng_xinshu.txt")
    format_zongheng("raw_data/06_zongheng_yuepiao.txt")


def build_dict(input_dir="processed/formated", output_dir="processed/info"):
    def _build_str_dict(input_dir, output_dir, idx):
        fea_dict = defaultdict(int)
        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, "r") as fin:
                for line in fin:
                    line_split = line.strip().split("\t")
                    fea_dict[line_split[idx]] += 1

        sorted_dict = sorted(
            fea_dict.iteritems(), key=lambda x: x[1], reverse=True)
        with open(os.path.join(output_dir, "fea_%02d.txt" % (idx)),
                  "w") as fout:
            max_count = sorted_dict[0][-1]
            for k, v in sorted_dict:
                fout.write("%s\t%.4f\t%d\n" % (k, v / max_count, v))

    def _count_max(input_dir, output_dir, idx):
        max_fea = 0.
        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file_name)
            with open(file_path, "r") as fin:
                for line in fin:
                    fea = float(line.strip().split("\t")[idx])
                    max_fea = fea if fea > max_fea else max_fea

        with open(os.path.join(output_dir, "fea_%02d.txt" % (idx)),
                  "w") as fout:
            fout.write("%.4f" % (max_fea))

    for idx, fea_name in enumerate(FEA):
        if idx < 4:
            _build_str_dict(input_dir, output_dir, idx)
        else:
            _count_max(input_dir, output_dir, idx)


def load_dict(file_path):
    word_dict = {}
    with open(file_path, "r") as fin:
        for line in fin:
            line_split = line.strip().split("\t")
            word_dict[line_split[0]] = line_split[1]
    return word_dict


def prepare_train(in_dir, out_dir, dict_dir):
    fea_dict = []
    for idx, fea_name in enumerate(FEA):
        fea_dict_path = os.path.join(dict_dir, "fea_%02d.txt" % (idx))
        if idx < 4:
            fea_dict.append(load_dict(fea_dict_path))
        else:
            fea_dict.append(float(open(fea_dict_path).readline().strip()))

    for file_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, file_name)
        out_path = os.path.join(out_dir, file_name)

        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")

                sample = ""
                for idx, fea in enumerate(line_split):
                    if idx < 4:
                        sample += "%s\t" % (fea_dict[idx][fea])
                    else:
                        sample += ("%f\t" % (float(fea) / fea_dict[idx]))
                fout.write("%s\n" % (sample.rstrip("\t")))


def make_pairs(in_dir, save_path, sampling_thd=0.8):
    with open(save_path, "w") as fout:
        for file_name in os.listdir(in_dir):
            in_path = os.path.join(in_dir, file_name)

            if "hongxiutianxiang" in in_path:
                sampling_thd = 0.85
            else:
                sampling_thd = 0.

            print("processing : %s" % (in_path))
            data = open(in_path, "r").readlines()

            for i in range(len(data)):
                for j in range(i + 1, len(data)):
                    prob = random.uniform(0., 1.)
                    if prob > sampling_thd:
                        fout.write("%s\t%s\n" %
                                   ("##".join(data[i].strip().split("\t")),
                                    "##".join(data[j].strip().split("\t"))))


if __name__ == "__main__":
    # to_utf8("raw_data")
    # build_dict()

    # prepare_train(
    #     in_dir="processed/formated",
    #     out_dir="processed/final",
    #     dict_dir="processed/info")

    make_pairs(in_dir="processed/final", save_path="processed/train.txt")
