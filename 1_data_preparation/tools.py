import numpy as np
import random

def auto_pading(data_numpy, size, random_pad=False):
    C, T, V, M = data_numpy.shape

    if T < size:
        begin = random.randint(0, size - T) if random_pad else 0
        data_numpy_paded = np.zeros((C, size, V, M))
        data_numpy_paded[:, begin: begin + T, :, :] = data_numpy
        return data_numpy_paded
    else:
        return data_numpy

def random_choose(data_numpy, size, auto_pad=True):
    C, T, V, M = data_numpy.shape
    if T == size:
        return data_numpy
    
    elif T < size:
        if auto_pad:
            return auto_pading(data_numpy, size, random_pad=False)
        else:
            return data_numpy
    else:
        begin = random.randint(0, T - size)
        return data_numpy[:, begin:begin + size, :, :]

def random_move(data_numpy, 
                angle_candinate=[-10., -5., 0., 5., 10.],
                scale_candinate=[0.9, 1.0, 1.1],
                transform_candinate=[-0.2, -0.1, 0.0, 0.1, 0.2],
                move_time_candinate=[1]
            ):
    
    C, T, V, M = data_numpy.shape

    move_time = random.choice(move_time_candinate)
    node = np.arange(0, T, T * 1.0 / move_time).round().astype(int)
    node = np.append(node, T)
    num_node = len(node)

    A = np.random.choice(angle_candinate, num_node)
    S = np.random.choice(scale_candinate, num_node)
    T_x = np.random.choice(transform_candinate, num_node)
    T_y = np.random.choice(transform_candinate, num_node)

    a = np.zeros(T)
    s = np.zeros(T)
    t_x = np.zeros(T)
    t_y = np.zeros(T) 


    for i in range(num_node - 1):
        a[node[i]:node[i + 1]] = np.linspace(
            A[i], A[i + 1], node[i + 1] - node[i]) * np.pi / 180
        s[node[i]:node[i + 1]] = np.linspace(S[i], S[i + 1],
                                             node[i + 1] - node[i])
        t_x[node[i]:node[i + 1]] = np.linspace(T_x[i], T_x[i + 1],
                                               node[i + 1] - node[i])
        t_y[node[i]:node[i + 1]] = np.linspace(T_y[i], T_y[i + 1],
                                               node[i + 1] - node[i])
    
    theta = np.array([[np.cos(a) * s, -np.sin(a) * s],
                      [np.sin(a) * s, np.cos(a) * s]])

    for i_frame in range(T):
        xy = data_numpy[0:2, i_frame, :, :]
        new_xy = np.dot(theta[:, :, i_frame], xy.reshape(2, -1))
        new_xy[0] += t_x[i_frame]
        new_xy[1] += t_y[i_frame]
        data_numpy[0:2, i_frame, :, :] = new_xy.reshape(2, V, M)

    return data_numpy

def random_shift(data_numpy):
    # input: C,T,V,M
    C, T, V, M = data_numpy.shape
    data_shift = np.zeros(data_numpy.shape)
    valid_frame = (data_numpy != 0).sum(axis=3).sum(axis=2).sum(axis=0) > 0
    begin = valid_frame.argmax()
    end = len(valid_frame) - valid_frame[::-1].argmax()

    size = end - begin
    bias = random.randint(0, T - size)
    data_shift[:, bias:bias + size, :, :] = data_numpy[:, begin:end, :, :]

    return data_shift

def openpose_match(data_numpy):
    C, T, V, M = data_numpy.shape
    assert(C == 3)
    score = data_numpy[2, :, :, :].sum(axis=1)
    rank = (-score[0:T - 1]).argsort(axis=1).reshape(T - 1, M)
    xy1 = data_numpy[0:2, 0:T - 1, :, :].reshape(2, T - 1, V, M, 1)
    xy2 = data_numpy[0:2, 1:T, :, :].reshape(2, T - 1, V, 1, M)
    
    distance = ((xy2 - xy1)**2).sum(axis=2).sum(axis=0)
    forward_map = np.zeros((T, M), dtype=int) - 1
    forward_map[0] = range(M)

    for m in range(M):
        choose = (rank == m)
        # ...and
