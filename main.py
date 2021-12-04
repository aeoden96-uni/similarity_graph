import numpy as np
import pandas as pd


def ucitaj(ime_dat):
    with open(ime_dat) as f:
        dim = int(f.readline())
        matrix = np.zeros((dim,dim))
        # print(dim)
        lines = f.readlines()

        for line in lines:
            # print(line)
            i,j = line.split()
            i = int(i)-1
            j =  int(j)-1
            # print(i,j)
            matrix[i][j] = 1
        return matrix


def find_unique(ime_dat,rijec_id):
    with open(ime_dat) as f:
        dim = int(f.readline())
        uniq = set()

        uniq.add(rijec_id)

        lines = f.readlines()

        for line in lines:
            try:
                i, j = line.split()
            except:
                continue
            i = int(i)
            j = int(j)

            if rijec_id == i:
                uniq.add(j)
            if rijec_id == j:
                uniq.add(i)
        # print(uniq)
        return len(uniq)

def ucitaj_large(ime_dat,rijec_id):
    with open(ime_dat) as f:
        dim = int(f.readline())
        uniq = set()
        # uniq.set(rijec_id)
        parovi= []

        lines = f.readlines()


        for line in lines:
            try:
                i, j = line.split()
            except:
                continue
            i = int(i)
            j = int(j)

            if rijec_id == i:
                uniq.add(j)

            if rijec_id == j:
                uniq.add(i)

            # if rijec_id == i or rijec_id == j:
            #     parovi.append((i, j))
            #     # w.write(f'{i} {j}\n')


        for line in lines:
            try:
                i, j = line.split()
            except:
                continue
            i = int(i)
            j = int(j)

            if i in uniq and j in uniq:
                parovi.append((i,j))


        print(uniq)
        # print(parovi)



        mapiranje= []

        for u in uniq:
            mapiranje.append(u)
        novi_parovi = []
        for i,j in parovi:
            novi_parovi.append((mapiranje.index(i)+1,mapiranje.index(j)+1))


    with open("novi" + str(rijec_id) + ".txt", "w+") as w:
        for i, j in novi_parovi:
            w.write(f'{i} {j}\n')

    with open("novi" + str(rijec_id) + "rijeci.txt", "w+") as w, open("examples/e00/index.txt",encoding="ISO-8859-1") as f:
        lines = f.readlines()
        print("mapiranje len: " ,len(mapiranje))
        novi_index = [""] * 50
        for i,line in enumerate(lines):
            ind = i + 1

            if ind in mapiranje:

                novi_index[mapiranje.index(ind)] = line

        for i in novi_index:
            w.write(i)



    # print(mapiranje)
    return len(uniq)





def inter(limit,A,B):
    X = np.ones((B.shape[0], A.shape[0]))
    if (limit < 1): raise ValueError
    # X = np.ones((5, 3))
    for i in range(limit):
        i = B.dot(X).dot(A.transpose())
        j = B.transpose().dot(X).dot(A)
        X = i+j
        norm = np.linalg.norm(X, 'fro')
        X = X / norm

    return np.around(X,4)

def main():
    example = input("Koji primjer:(npr e01) ")


    # if example == "e00":
    #     # id = int(input("Id rijeci: "))
    #     id = 27893
    #     A = ucitaj_large("examples/" + example + "/dico.txt",id)
    #     # print(A)
    #     # B = ucitaj("examples/" + example + "/dico.txt")
    #     print(A)
    #     # p = inter(2, A, B)
    #
    #
    #
    # else:
    #     itt = int(input("Broj iteracija: "))
    #
    #     A = ucitaj("examples/" + example + "/A.txt")
    #     # print(A)
    #     B = ucitaj("examples/" + example + "/B.txt")
    #
    #     p = inter(itt,A,B)
    id = 27893
    B = ucitaj("novi27893.txt")
    A = ucitaj("B.txt")
    p = inter(30, A, B)


    print(p)
    print("Korijen sume kvadrata elemenata", np.sqrt(np.sum(np.square(p))))

    # najveci = []
    #
    # for i,k in enumerate(p[1]):
    #     najveci.append((i,k))
    #
    # najveci.sort(key=lambda x: x[1])
    #
    #
    # print("Max: " , np.max(p[1]))
    # print(najveci)




if __name__ == '__main__':
    main()
