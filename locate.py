import numpy as np

han = np.hanning(20124)
print(han)
# firstHalf = np.where(han > 0.4)
# firstHalfIndex = firstHalf[0][0]
# secondHalfIndex = firstHalf[0][-1]
length = len(han)
arr1 = han[:round(length/4)]
arr2 = han[round(length/4):round(3*length/4)]
arr3 = han[round(3*length/4):]
print(arr1)
print(arr2)
print(arr3)
