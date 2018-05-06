#coding=utf-8
import sys
import os
import pdb
from collections import defaultdict


def proc_11_28(in_dir, out_dir):
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        out_path = os.path.join(out_dir, f_name)
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")
                if len(line_split) < 12: continue
                fout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    line_split[0],  # book title
                    line_split[1],  # the writer
                    line_split[3],  # click number
                    line_split[4],  # comment number
                    line_split[5].replace("\"", "").replace(",", ""),  # score
                    line_split[8],  # whether sign the contract
                    line_split[10],  # type
                    line_split[11],  # word count
                ))


def proc_11_14(in_dir, out_dir):
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        out_path = os.path.join(out_dir, f_name)
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")
                if len(line_split) < 9: continue

                click = str(int(float(line_split[3]) * 1000))
                comment = str(int(float(line_split[4]) * 1000))
                score = str(int(float(line_split[5]) * 1000))
                word_num = str(
                    int(
                        float(line_split[8].replace("\"", "").replace(
                            "\xc2\xa0", "")) * 1000))

                fout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    line_split[0],  # book title
                    line_split[1],  # the writer
                    click,  # click number
                    comment,  # comment number
                    score,  # score
                    line_split[6],  # whether sign the contract
                    line_split[7],  # type
                    word_num,  # word count
                ))


def proc_12_26(in_dir, out_dir):
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        out_path = os.path.join(out_dir, f_name)
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")
                if len(line_split) < 10: continue

                fout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    line_split[0],  # book title
                    line_split[1],  # the writer
                    line_split[3],  # click number
                    line_split[4],  # comment number
                    line_split[5],
                    # str(line_split[5] + line_split[6]),  # score
                    line_split[7],  # whether sign the contract
                    line_split[8],  # type
                    line_split[9],  # word count
                ))


def proc_01_13(in_dir, out_dir):
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        out_path = os.path.join(out_dir, f_name)
        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")

                if line_split[5] == "签约上架":
                    signed = "签约"
                else:
                    signed = "未签约"

                fout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    line_split[0],  # 标题
                    line_split[1],  # 作者
                    line_split[7],  # 点击
                    line_split[10],  # 评论
                    str(int(line_split[8]) + int(line_split[9])),  # 鲜花数
                    signed,  # 是否签约
                    line_split[4],  # 类型
                    line_split[7]  # 字数
                ))


def format_hongxiutianxiang(in_path, out_path):
    with open(in_path, "r") as fin, open(out_path, "w") as fout:
        for line in fin:
            line_split = line.strip().split("\t")

            # if line_split[5] == "签约上架":
            #     signed = "签约"
            # else:
            #     signed = "未签约"

            if "万" in line_split[7]:
                click = line_split[7].replace("万总点击", "")
                click = str(int(float(click) * 1000))
            else:
                click = line_split[7].replace("总点击", "")
                click = str(int(float(click)))

            if "万" in line_split[6]:
                shoucang = line_split[6].replace("万总收藏", "")
                shoucang = str(int(float(click) * 1000))
            else:
                shoucang = line_split[6].replace("总收藏", "")
                shoucang = str(int(float(click)))

            if "万" in line_split[5]:
                word = line_split[5].replace("万", "")
                word = str(int(float(click) * 1000))
            else:
                word = str(int(float(click)))

            score = "0"
            comment = "0"
            fout.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                "".join(line_split[0].split()),  # 标题
                "".join(line_split[1].split()),  # 作者
                click,  # 点击
                comment,  # 评论 = 月票
                score,
                line_split[4],  # 是否签约
                line_split[3],  # 类型
                word  # 字数
            ))


def format_raw():
    # proc_11_28("11_28", "all_data_12_26")
    # proc_11_28("12_07", "all_data_12_26")
    # proc_11_28("human_ranked", "all_data_12_26")
    # proc_11_14("12_14", "all_data_12_26")
    # proc_11_14("12_24", "all_data_12_26")

    # proc_12_26("12_26", "../12_26/formated")
    # proc_01_13("01_13", "../01_13/formated")
    format_hongxiutianxiang("15_hongxiutianxiang.txt",
                            "15_hongxiutianxiang_clean.txt")


def writer_info(in_dir, col_num, out_file):
    dicts = defaultdict(set)
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        with open(in_path, "r") as fin:
            for line in fin:
                line_split = line.strip().split("\t")
                key = "".join(line_split[col_num].lower().split())
                dicts[key].add(line_split[0])

    sorted_dict = sorted(
        dicts.iteritems(), key=lambda x: len(x[1]), reverse=True)
    max_val = 0
    for v in dicts.values():
        if len(v) > max_val: max_val = len(v)

    with open(out_file, "w") as fout:
        for item in sorted_dict:
            fout.write("%s\t%.6f\t%d\n" % (item[0], float(len(item[1])) /
                                           max_val, len(item[1])))


def build_dict(in_dir, col_num, out_file):
    dicts = defaultdict(int)
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        with open(in_path, "r") as fin:
            for line in fin:
                line_split = line.strip().split("\t")
                key = "".join(line_split[col_num].lower().split())
                dicts[key] += 1

    sorted_dict = sorted(dicts.iteritems(), key=lambda x: x[1], reverse=True)
    max_val = max(dicts.values())
    with open(out_file, "w") as fout:
        for item in sorted_dict:
            fout.write("%s\t%.6f\t%d\n" % (item[0], float(item[1]) / max_val,
                                           item[1]))


def find_max(in_dir, col, out_path):
    max_val = -1
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        with open(in_path, "r") as fin:
            for line in fin:
                line_split = line.strip().split("\t")
                val = int(line_split[col].replace("\xc2\xa0", ""))
                if val > max_val:
                    max_val = val
    open(out_path, "w").write("%d" % max_val)


def clean_col5(in_dir, out_dir):
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        with open(in_path, "r") as fin, open(
                os.path.join(out_dir, f_name), "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")
                if line_split[5] in ["签约", "是", "已签约"]:
                    line_split[5] = "签约"
                else:
                    line_split[5] = "未签约"
                fout.write("%s\n" % ("\t".join(line_split)))


def load_dict(in_path):
    word_dict = {}
    with open(in_path, "r") as fin:
        for line in fin:
            line_split = line.strip().split("\t")
            word_dict[line_split[0]] = float(line_split[1])
    return word_dict


def norm_input(info_dir, in_dir, out_dir):
    writer = load_dict(os.path.join(info_dir, "01_all_writers.txt"))
    click_max = float(
        open(os.path.join(info_dir, "02_click_max.txt"), "r").readline().strip(
        ))
    comment_max = float(
        open(os.path.join(info_dir, "03_comment_max.txt"), "r").readline()
        .strip())
    score_max = float(
        open(os.path.join(info_dir, "04_score_max.txt"), "r").readline().strip(
        ))
    signed = load_dict(os.path.join(info_dir, "05_signed.txt"))
    types = load_dict(os.path.join(info_dir, "06_types.txt"))
    word_count_max = float(
        open(os.path.join(info_dir, "07_word_count_max.txt"), "r").readline()
        .strip())

    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        out_path = os.path.join(out_dir, f_name)

        with open(in_path, "r") as fin, open(out_path, "w") as fout:
            for line in fin:
                line_split = line.strip().split("\t")

                writer_name = "".join(line_split[1].lower().split())
                if not writer_name: continue

                fout.write("%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (
                    "".join(line_split[0].split()),  #  书名
                    writer[writer_name],  #  作者
                    float(line_split[2]) / click_max,  # 点击
                    float(line_split[3].replace("\xc2\xa0", "")) /
                    comment_max,  #  评论
                    float(line_split[4]) / score_max,  #  积分
                    signed[line_split[5]],  # 是否签约
                    types["".join(line_split[6].lower().split())],  # 类型
                    float(line_split[7]) / word_count_max,  #  字数
                ))


def mkdir_pairs(in_dir, out_path):
    fout = open(out_path, "w")
    for f_name in os.listdir(in_dir):
        in_path = os.path.join(in_dir, f_name)
        print in_path

        samples = []
        with open(in_path, "r") as fin:
            for line in fin:
                a_sample = line.strip().split("\t")
                samples.append(a_sample)

            for i in range(len(samples)):
                for j in range(i, len(samples)):
                    fout.write("%s\t%s\n" % (" ".join(samples[i]),
                                             " ".join(samples[j])))


def proc_12_24():
    build_dict("all_data", 1, out_file="info/01_all_writers.txt")
    find_max("all_data", 2, "info/02_click_max.txt")
    find_max("all_data", 3, "info/03_comment_max.txt")
    find_max("all_data", 4, "info/04_score_max.txt")
    build_dict("all_data", 5, out_file="info/05_signed.txt")
    build_dict("all_data", 6, out_file="info/06_types.txt")
    find_max("all_data", 7, "info/07_word_count_max.txt")


def data_info_01_13():
    writer_info("all_data_01_13", 1, out_file="info_01_13/01_all_writers.txt")
    find_max("all_data_01_13", 2, "info_01_13/02_click_max.txt")
    find_max("all_data_01_13", 3, "info_01_13/03_comment_max.txt")
    find_max("all_data_01_13", 4, "info_01_13/04_score_max.txt")
    build_dict("all_data_01_13", 5, out_file="info_01_13/05_signed.txt")
    build_dict("all_data_01_13", 6, out_file="info_01_13/06_types.txt")
    find_max("all_data_01_13", 7, "info_01_13/07_word_count_max.txt")


def data_info_01_13():
    writer_info("all_data_01_13", 1, out_file="info_01_13/01_all_writers.txt")
    find_max("all_data_01_13", 2, "info_01_13/02_click_max.txt")
    find_max("all_data_01_13", 3, "info_01_13/03_comment_max.txt")
    find_max("all_data_01_13", 4, "info_01_13/04_score_max.txt")
    build_dict("all_data_01_13", 5, out_file="info_01_13/05_signed.txt")
    build_dict("all_data_01_13", 6, out_file="info_01_13/06_types.txt")
    find_max("all_data_01_13", 7, "info_01_13/07_word_count_max.txt")


if __name__ == "__main__":
    # format_raw()
    # clean_col5("all_data_12_26", "./clean")
    # data_info_12_26()
    # data_info_01_13()

    # norm_input("info_12_26", "all_data_12_26", "normed_for_train_12_26")
    # norm_input("info_01_13", "all_data_01_13", "normed_for_train_01_13")

    # mkdir_pairs("normed_for_train_12_26", "train_pairs_12_26.txt")

    mkdir_pairs("normed_for_train_01_13", "train_pairs_01_13.txt")

    # norm_input("../12_24/formated", "normed_for_test")
