def auto_pading(data_numpy, size, random_pad=False):
    C, T, V, M = data_numpy.shape

    if T < size:
        begin = random.randint(0, size - T) if random_pad else 0
        data_numpy_paded = np.zeros((C, size, V, M))
        data_numpy_paded[:, begin: begin + T, :, :] = data_numpy
        return data_numpy_paded
    else:
        return data_numpy