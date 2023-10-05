import sympy as sm
import fractions as fr
class Mat:
    def __init__(self, row, column, fill):
        self.row = row
        self.col = column
        self.element = [[fill] * self.col for i in range(self.row)]

    def __str__(self):
        m = len(self.element)
        mtx = ""
        for i in range(m):
            mtx += ('|' + ', '.join(map(lambda x: '{0:8.3f}'.format(x), self.element[i])) + '|\n')
        return mtx

    def __add__(self, other):
        c = Mat(self.row, self.col, fill = 0)
        if isinstance(other, Mat):
            for i in range(self.row):
                for j in range(self.col):
                    c.element[i][j] = self.element[i][j] + other.element[i][j]
        elif isinstance(other, (int, float)):
            for i in range(self.row):
                for j in range(self.col):
                    c.element[i][j] = self.element[i][j] + other
        return c

    def __radd__(self, other):  
        return self.__add__(other)

    def __sub__(self, other):
        other = other*-1
        return self.__add__(other)

    def __mul__(self, other): #pointwise multiplication
        C = Mat(self.row, self.col, fill = 0)
        if isinstance(other, Mat):

            for i in range(self.row):
                for j in range(self.col):
                    C.element[i][j] = self.element[i][j] * other.element[i][j]

        elif isinstance(other, (int, float)):

            for i in range(self.row):
                for j in range(self.col):
                    C.element[i][j] = self.element[i][j] * other
        return C 

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __matmul__(self, other): # use symbol @
        if (isinstance(other, Mat)) & (self.col == other.row):
            C = Mat(self.row, other.col, fill = 0)
            for i in range(self.row):
                for j in range(other.col):
                    acc = 0
                    for k in range(self.col):
                        acc += self.element[i][k] * other.element[k][j]
                    C.element[i][j] = acc
        return C
    
    def __truediv__(self, other):
        c = Mat(self.row, self.col, fill = 0)
        if isinstance(other, (int, float)):
            for i in range(self.row):
                for j in range(self.col):
                    c.element[i][j] = self.element[i][j] / other
        return c

    def __getitem__(self, key):
        if isinstance(key, tuple):
            i = key[0] - 1
            j = key[1] - 1
            return self.element[i][j]
        elif isinstance(key, int):
            i = key - 1
            return self.element[i]

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            i = key[0] - 1
            j = key[1] - 1
            self.element[i][j] = value 
        elif isinstance(key, int):
            i = key - 1
            for j in range(i):
                self.element[i][j] = value[j]

    def div_row(self, value):
        if isinstance(value, int):
            i = self.col - 1
            for j in range(i):
                self.element[i][j] =  self.element[i][j]/value

    def create(ls):
        try:
            row = len(ls)
            col = len(ls[0])
            B = Mat(row, col, 0)
            for i in range(row):
                for j in range(col):
                    B.element[i][j] = ls[i][j]
            return B
        except:
            print("not the correct data type")

def row_reducing(ls : list, j : int):
    temp = []
    for i in ls:
        temp.append(i/j)
    ls = temp
    return ls

def rref(mat):
    rows = len(mat)
    cols = len(mat[0])
    for x in range(rows):
        for y in range(cols):
            mat[x][y] = str(mat[x][y])
            val = mat[x][y]
            mat[x][y] = fr.Fraction(val)

    for i in range(rows):
        if i < cols:
            pivot = mat[i][i]
            if pivot != 0:
                mat[i] = row_reducing(mat[i], pivot)
                for j in range(rows):
                    if j != i:
                        sec_pivot = mat[j][i]
                        mult = []
                        for k in mat[i]:
                            mult.append(k*sec_pivot)
                        temp = []
                        for x, y in zip(mat[j], mult):
                            temp.append(x - y)
                        mat[j] = temp
                        
            else:
                continue
    return mat
z = 1
while z == 1:
    print("Enter the number for operation:")
    print("1. RREF\n2. Matrix Calculation\n3. Scalar Calculation\n4. RREF2(sympy)\n5. Determinant(sympy)\n6. Inverse(sympy)")
    print()
    value = int(input())
    print()
    if (value == 1):
        try:
            a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
            print()
            mat1 = Mat(a[0], a[1], 0)
            print("Enter the matrix sperated by space and each row on different line: ")
            print()
            for i in range(a[0]):
                b = list(map(int, input().split(" ")))
                mat1.element[i] = b
            print("Your matrix is: ")
            print(mat1)
            print("row reduced echlon form of the matrix is: ")
            mat2 = mat1.element
            mat3 = rref(mat2)
            for i in range(mat1.row):
                for j in range(mat1.col):
                    print(mat3[i][j], end=' ')
                print()
        except :
            print("Error! Try again")
            continue
        
    elif (value == 2):
        print("Enter the type of operation you want to perform: ")
        print("1. Matrix mutliply\n2. Matrix Addition\n3. Matrix Subtraction")
        print()
        val = int(input())
        if (val == 1):
            try :
                a = list(map(int, input("Enter the number of rows and columns for the first matrix: ").split(" ")))
                print()
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line: ")
                print()
                for i in range(a[0]):
                    b1 = list(map(int, input().split(" ")))
                    mat1.element[i] = b1
                b = list(map(int, input("Enter the number of rows and columns for the second matrix: ").split(" ")))
                mat2 = Mat(b[0], b[1], 0)
                while (a[1]!=b[0]):
                    print("Wrong size, Column of first matrix should match row of second, Try Again!")
                    print()
                    b = list(map(int, input("Enter the number of rows and columns for the second matrix: ").split(" ")))
                mat2 = Mat(b[0], b[1], 0)
                print("Enter the matrix sperated by space and each row on different line: ")
                print()
                for i in range(b[0]):
                    lb = list(map(int, input().split(" ")))
                    mat2.element[i] = lb
                print(mat1)
                print(mat2)
                print(mat1@mat2)
            except:
                print("Error! Try again")
                continue

        elif (val == 2):
            try:
                a = list(map(int, input("Enter the number of rows and columns for the first matrix: ").split(" ")))
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line: ")
                for i in range(a[0]):
                    b = list(map(int, input().split(" ")))
                    mat1.element[i] = b
                b = list(map(int, input("Enter the number of rows and columns for the second matrix: ").split(" ")))
                while (a[1]!=b[1]) & (a[0]!=b[0]):
                    print("Wrong size, both matrix should have same size, Try Again!")
                    b = list(map(int, input("Enter the number of rows and columns for the second matrix: ").split(" ")))
                mat2 = Mat(b[0], b[1], 0)
                print("Enter the matrix sperated by space and each row on different line: ")
                for i in range(b[0]):
                    lb = list(map(int, input().split(" ")))
                    mat2.element[i] = lb
                print(mat1)
                print(mat2)
                print(mat1+mat2)
            except:
                print("Error! Try again")
                continue
            
        elif (val == 3):
            try:
                a = list(map(int, input("Enter the number of rows and columns for the first matrix: ").split(" ")))
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line: ")
                for i in range(a[0]):
                    b = list(map(int, input().split(" ")))
                    mat1.element[i] = b
                b = list(map(int, input("Enter the number of rows and columns for the second matrix: ").split(" ")))
                while (a[1]!=b[1]) & (a[0]!=b[0]):
                    print("Wrong size, both matrix should have same size, Try Again!")
                    b = list(map(int, input("Enter the number of rows and columns for the second matrix: ").split(" ")))
                mat2 = Mat(b[0], b[1], 0)
                print("Enter the matrix sperated by space and each row on different line: ")
                for i in range(b[0]):
                    lb = list(map(int, input().split(" ")))
                    mat2.element[i] = lb
                print(mat1)
                print(mat2)
                print(mat1-mat2)
            except:
                print("Error! Try again")
                continue
        else:
            print("not valid!")
        
    elif (value == 3):
        print("1. Add\n2. Subtract\n3. Multiply\n4. Divide")
        print("Enter the type of operation: ")
        val = int(input())
        sca = int(input("Enter the scalar: "))
        if (val == 1):
            try:
                a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line:")
                for i in range(a[0]):
                    b = list(map(int, input().split(" ")))
                    mat1.element[i] = b
                print(mat1 + sca)
            except:
                print("Error! Try again")
                continue
        elif (val == 2):
            try:
                a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line:")
                for i in range(a[0]):
                    b = list(map(int, input().split(" ")))
                    mat1.element[i] = b
                print(mat1 - sca)
            except:
                print("Error! Try again")
                continue
        elif (val == 3):
            try:
                a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line:")
                for i in range(a[0]):
                    b = list(map(int, input().split(" ")))
                    mat1.element[i] = b
                print(mat1 * sca)
            except:
                print("Error! Try again")
                continue
        elif (val == 4):
            try:
                a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
                mat1 = Mat(a[0], a[1], 0)
                print("Enter the matrix sperated by space and each row on different line:")
                for i in range(a[0]):
                    b = list(map(int, input().split(" ")))
                    mat1.element[i] = b
                print(mat1/sca)
            except:
                print("Error! Try again")
                continue
        else:
            print("Not valid!")
            
    elif (value == 4):
        try:
            a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
            b = []
            print("Enter the matrix sperated by space and each row on different line: ")
            for i in range(a[0]):
                c = list(map(int, input().split(" ")))
                b.append(c)
            M = sm.Matrix(b)
            print("Your matrix is: ")
            print(M)
            print()
            print("row reduced echlon form of the matrix is: ")
            M2 = M.rref()
            print(M2)
            print()
        except:
            print("Error! Try again")
            continue
    elif (value == 5):
        try:
            a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
            b = []
            print("Enter the matrix sperated by space and each row on different line:")
            for i in range(a[0]):
                c = list(map(int, input().split(" ")))
                b.append(c)
            M = sm.Matrix(b)
            print("Your matrix is: ")
            print(M)
            print()
            print("Determinant of the matrix is: ")
            M2 = M.det()
            print(M2)
            print()
        except:
            print("Error! Try again")
            continue
    elif (value == 6):
        try:
            a = list(map(int, input("Enter the number of rows and columns: ").split(" ")))
            b = []
            print("Enter the matrix sperated by space and each row on different line: ")
            for i in range(a[0]):
                c = list(map(int, input().split(" ")))
                b.append(c)
            M = sm.Matrix(b)
            print("Your matix is: ")
            print(M)
            print()
            print("Inverse of the matrix is: ")
            M2 = M**-1
            print(M2)
            print()
        except:
            print("Error! Try again")
            continue
        
    else:
        print("Not valid!")
        print()
    
    print("Do you wanna do another calculation?\n1. yes\n2. no")
    z = int(input())

    
