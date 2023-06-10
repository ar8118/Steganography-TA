import numpy as np
import random


def data_embedding_algorithm(cover_image, secret_data):

    stego_image = np.copy(cover_image)

    key = random.randint(0, 255)

    secret_data = np.bitwise_not(secret_data)

    for i in range(secret_data.shape[0]):
        for j in range(secret_data.shape[1]):
            k1 = (cover_image[i, j] >> 1) & 1
            k2 = (cover_image[i, j] >> 2) & 1
            m1 = cover_image[i, j] & 1

            if k1 == 0 and k2 == 0:
                count_unchanged = 'countNc00'
                count_changed = 'countN00'
            elif k1 == 1 and k2 == 0:
                count_unchanged = 'countNc10'
                count_changed = 'countN10'
            elif k1 == 0 and k2 == 1:
                count_unchanged = 'countNc01'
                count_changed = 'countN01'
            else:
                count_unchanged = 'countNc11'
                count_changed = 'countN11'

            if m1 == secret_data[i, j]:
                locals()[count_unchanged] += 1
            else:

                stego_image[i, j] = secret_data[i, j]

                locals()[count_changed] += 1

    if locals()['countNc00'] > locals()['countN00']:

        stego_image[((stego_image >> 1) & 1) == 0 &
                    ((stego_image >> 2) & 1) == 0] ^= 1
    elif locals()['countNc10'] > locals()['countN10']:

        stego_image[((stego_image >> 1) & 1) == 1 &
                    ((stego_image >> 2) & 1) == 0] ^= 1
    elif locals()['countNc01'] > locals()['countN01']:

        stego_image[((stego_image >> 1) & 1) == 0 &
                    ((stego_image >> 2) & 1) == 1] ^= 1
    elif locals()['countNc11'] > locals()['countN11']:

        stego_image[((stego_image >> 1) & 1) == 1 &
                    ((stego_image >> 2) & 1) == 1] ^= 1

    return stego_image, key


def data_extraction_algorithm(stego_image, key_matrix):

    np.random.seed(key_matrix)
    N = stego_image.shape[0]
    p = np.random.randint(0, 16)

    if p & 0b0001:

        stego_image[((stego_image >> 1) & 1) == 0 &
                    ((stego_image >> 2) & 1) == 0] ^= 1
    elif p & 0b0010:

        stego_image[((stego_image >> 1) & 1) == 1 &
                    ((stego_image >> 2) & 1) == 0] ^= 1
    elif p & 0b0100:

        stego_image[((stego_image >> 1) & 1) == 0 &
                    ((stego_image >> 2) & 1) == 1] ^= 1
    elif p & 0b1000:

        stego_image[((stego_image >> 1) & 1) == 1 &
                    ((stego_image >> 2) & 1) == 1] ^= 1

    secret_data = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            if stego_image[i, j] % 2 == 0:
                secret_data[i, j] = 1

    return secret_data


def main():
    cover_image = input("Enter cover image bits")
    secret_data = input("Enter secret data")
    output = data_embedding_algorithm(cover_image, secret_data)
    hidden_message = data_extraction_algorithm(output[0], output[1])
    print(hidden_message)


if __name__ == '__main__':
    main()
