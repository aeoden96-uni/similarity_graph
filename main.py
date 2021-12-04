import numpy as np
import pandas as pd


# B = np.array([[0,1,1,0,0],
#                  [0,0,1,0,1],
#                  [0,0,0,1,1],
#                  [0,1,0,0,0],
#                  [0,0,0,0,0]])
#
# A = np.array([[0,1,0],
#                  [0,0,1],
#                  [0,0,0]])
A = np.array([[0,1,1,0],
                 [1,0,1,0],
                 [0,1,0,0],
                 [1,0,1,0]])

B = np.array([[0,0,1,1,0,0],
            [0,0,0,1,0,1],
            [1,0,0,0,1,1],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [1, 0, 1, 1, 0,0]
              ])

sizeB= B.shape[0]
sizeA= A.shape[0]

def inter(limit,X = np.ones((sizeB,sizeA))):
    if (limit < 1): raise ValueError
    # X = np.ones((5, 3))
    for i in range(limit):
        i = B.dot(X).dot(A.transpose())
        j = B.transpose().dot(X).dot(A)
        X = i+j
        norm = np.linalg.norm(X, 'fro')
        X = X / norm
    return X

def main():
    p = inter(16)


    print(p)
    print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(p))))
    # print("Nova matrica\n", nova)
    # print("Norma", norm)
    # print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(nova))))

    # p = np.array([[1,0],[0,1]])
    # norm = np.linalg.norm(p,'fro')
    # nova = p/norm
    # print(p)
    # print(nova)
    # print(np.sum(nova))



if __name__ == '__main__':
    main()
