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




