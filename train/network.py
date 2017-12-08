import paddle.v2 as paddle
from paddle.v2.layer import parse_network

__all__ = ["half_ranknet", "ranknet"]


def half_ranknet(name, input_dim, is_infer=False):
    data = paddle.layer.data(name, paddle.data_type.dense_vector(input_dim))
    # hd1 = paddle.layer.fc(input=data,
    #                       size=10,
    #                       act=paddle.activation.Tanh(),
    #                       param_attr=paddle.attr.Param(
    #                           initial_std=0.01, name="hidden_w1"))
    output = paddle.layer.fc(
        input=data,
        size=1,
        act=paddle.activation.Linear(),
        # act=paddle.activation.Sigmoid(),
        param_attr=paddle.attr.Param(initial_std=0.001, name="output"))
    return output


def ranknet(input_dim):
    output_left = half_ranknet("pos", input_dim)
    output_right = half_ranknet("neg", input_dim)
    label = paddle.layer.data("label", paddle.data_type.dense_vector(1))

    cost = paddle.layer.rank_cost(
        left=output_left, right=output_right, label=label)
    return cost


if __name__ == "__main__":
    print(parse_network(ranknet(18)))
