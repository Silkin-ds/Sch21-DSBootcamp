def data_types():
    intt=2003
    strr='qwerty'
    floatt=20.03
    booll=True
    listt=[2,0,0,3]
    dictt={"car":"bmw"}
    tuplee= (2,0,0,3)
    sett={2,0,0,3}

    types=[type(intt).__name__, type(strr).__name__, type(floatt).__name__, type(booll).__name__, type(listt).__name__, type(dictt).__name__, type(tuplee).__name__, type(sett).__name__]
    print(f"[{', '.join(types)}]")

if __name__ == '__main__':
      data_types()
      
