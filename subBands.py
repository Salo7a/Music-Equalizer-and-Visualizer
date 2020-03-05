import numpy as np



def subBands(arr, subs):
    subSize = int(len(arr)//subs)
    arrSubs = []
    for index in range(subs):
        sub = []
        if index == 0:
            sub = arr[:subSize]
        elif index == range(subs)[-1]:
            sub = arr[subSize*index:]
        else:
            sub = arr[subSize*index:(subSize*(index+1))]

        arrSubs.append(sub)

    return arrSubs


def FWHM(arr, length):
    before = arr[:round(length/4)]
    middle = arr[round(length/4):round(length/4)+length//2]
    after = arr[round(3*length/4)+1:]
    while len(middle) > length:
        middle = middle[:-1]
    while len(middle) < length:
        middle = np.append(middle, [0.5])
    while len(before) < length:
        before = np.append([1], before)
    while len(before) > length:
        before = before[:-1]
    while len(after) < length:
        after = np.append(after, [1])
    while len(before) > length:
        after = after[:-1]

    return before, middle, after





