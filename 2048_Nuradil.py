#keep calm it's my first game (Nuradıl)
import random
print('Вас приветствует бот игры "2^11=2048"')
table_hw=int(input('Введите сторону квадратной доски: '))
bc=int(input('Введите максимальное число шагов назад: '))
print('***************************************')
print('Советы:')
print('Используйте клавиши WASD')
print('Наберите exit в консоль для выхода из бесконечного цикла! :)')
print('Наберите back x для шага назад(х число меньшее или равное'+str(bc)+')')
print('Чтобы начать новую игру наберите new game')
print("OK! LET'S GO!")
print('***************************************')
#основная функция программы {hw - длинна и ширина доски, bc - максимальное число шагов назад}
def main(hw,bc):
    #основной вложенный список как бы игровая доска
    cell=[]
    #заполнение основного списка нулями
    for i in range(hw):
        cell.append([0]*hw)
    #список пустых ячейек
    empty=[]
    #буфер для хранения предыдущих шагов
    bufer=[]
    #обновление списка пустых ячейек
    mx =updater(empty,cell,hw)
    #добавление новой плитки
    auto_insert(empty,cell,hw)
    # и еще раз то же самое
    mx = updater(empty,cell,hw)
    auto_insert(empty,cell,hw)
    #вывод получившигося списка с помощью специальной функции
    printer(cell,mx)
    n=True
    #sc это score то есть общий счет
    sc=0
    #максимально возможный счет в идеальном случае
    mx_sc=2**(hw*hw+1)
    print('SCORE:'+str(sc)+'  [maximal score:'+str(mx_sc)+']')
    print('        ')
    while n:
        #инпут команд пользователя из консоли
        key=input()
        #если пользователь ввел w - плитки ползут вверх, a - влево, s - вниз, d - вправо
        if key=='w' or key=='W':
            #запись главного списка для шагов назад
            zip(cell,bufer,hw,bc)
            #функция движения плиток которая возвращает новый счет
            sc,mx=up(empty,cell,hw,sc)
        #как бы то же самое только влево, вправо и вниз
        elif key=='s' or key=='S':
            zip(cell,bufer,hw,bc)
            sc,mx=down(empty,cell,hw,sc)
        elif key=='d' or key=='D':
            zip(cell,bufer,hw,bc)
            sc,mx=right(empty,cell,hw,sc)
        elif key=='a' or key=='A':
            zip(cell,bufer,hw,bc)
            sc,mx=left(empty,cell,hw,sc)
        #при наборе new game начнется новая игра после проходов всех if else
        elif key=='new game':
            ng=input('Вы уверенны? :) y/n')
            if ng=='y':
                ng=input('Выбрать новую доску? y/n')
                if ng=='y':
                    table_hw=int(input('Введите сторону квадратной доски: '))
                    bc=int(input('Введите максимальное число шагов назад: '))
                    #вызов основной функции для начатия новой игры
                    main(table_hw,bc)
                elif ng=='n':
                    print('Новая игра! :)')
                    print('          ')
                    main(hw,bc)
            elif ng=='n':
                print('Ну ладно! Продолжайте')
                print('       ')
        #при написании exit в консоль переменная n станет False и основной цикл закончиться
        elif key=='exit':
            ex=input('Вы уверенны? :( y/n')
            if ex=='y':
                n=False
            elif ex=='n':
                print('Вот шутник! :) ')
        else:
            #при написании back x {x это число шагов назад} игра возвращается назад
            if len(key)>=6 and key[0:4]=='back':
                #инпут был например back 5 при сплит через пробел a будет back, а b будет 5
                a,b=key.split(' ')
                #split возвращает string а нам нужен integer
                b=int(b)
                #функция шага назад
                back(bufer,cell,b,hw,bc)
        #вывод основного списка
        printer(cell,mx)
        #вывод очков
        print('SCORE:'+str(sc))
        #функция over проверяет есть ли еще возможные ходы и возвращает true или false
        f=over(empty,cell,hw)
        #соответственно если f true то игра окончена и цикл должен завершится
        if f==True:
            n=False
        print('          ')
    #после завершения цикла работает else
    else:
        print('TOTAL SCORE:'+str(sc))
    print('Game Over')

#функция упаковки каждого хода игрока в буферный список
def zip(cell,bufer,hw,bc):
    
    #так как простое копирование не работает из за того что в буфере остается просто ссылка на скопированный список
    #приходиться превращать его в текст и только потом записывать в буфер
    a=''
    for i in range(hw):
        for j in range(hw):
            a+=(str(cell[i][j])+' ')
    bufer.append(a)
    #если буфер стал больше максимального количества шагов назад то первый элемент буфера удаляется
    if len(bufer)>bc:
        bufer.pop(0)

#функция отмены хода
def back(bufer,cell,steps,hw,bc):    
    ln=len(bufer)
    #если введенное число меньше или равно длинне буфера
    if steps<=ln:
        a=bufer[-steps]
        x=1
        u=''
        #распаковка буфера
        for i in a:
            if i!=' ':
                u+=i
            else:
                if x<=hw*hw:
                    k,j=de_indexer(x,hw)
                    cell[k][j]=u
                    u=''
                    x+=1
        #замена основного списка на только что распакованный
        for i in range(hw):
            for j in range(hw):
                cell[i][j]=int(cell[i][j])
    #если длинна меньше мы сообщаем об этом пользователю
    else:
        if steps>bc:
            print('Но вы указали максимально только '+str(bc)+' шагов! :|')
        else:
            print('Вы еще не сделали '+str(steps)+' ходов')

#функция проверки возможности хода
def over(m,l,hw):
    updater(m,l,hw)
    #проходимся по всем плиткам и проверяем есть ли рядом такая же или пустая
    #если пустых ячеек нет возвращается true если есть false
    if len(m)==0:
        for i in range(hw):
            for j in range(hw):
                if i==0:
                    if j==0:
                        if l[i][j]==l[i+1][j] or l[i][j]==l[i][j+1]:
                            return False
                    else:
                        if j!=hw-1:
                            if l[i][j]==l[i+1][j] or l[i][j]==l[i][j+1] or l[i][j]==l[i][j-1]:
                                return False
                        else:
                            if l[i][j]==l[i+1][j] or l[i][j]==l[i][j-1]:
                                return False
                else:
                    if i!=hw-1:
                        if j==0:
                            if l[i][j]==l[i+1][j] or l[i][j]==l[i-1][j] or l[i][j]==l[i][j+1]:
                                return False
                        else:
                            if j!=hw-1:
                                if l[i][j]==l[i+1][j] or l[i][j]==l[i-1][j] or l[i][j]==l[i][j+1] or l[i][j]==l[i][j-1]:
                                    return False
                            else:
                                if l[i][j]==l[i+1][j] or l[i][j]==l[i-1][j] or l[i][j]==l[i][j-1]:
                                    return False
                    else:
                        if j==0:
                            if l[i][j]==l[i-1][j] or l[i][j]==l[i][j+1]:
                                    return False
                        else:
                            if j!=hw-1:
                                if l[i][j]==l[i-1][j] or l[i][j]==l[i][j+1] or l[i][j]==l[i][j-1]:
                                    return False
                            else:
                                if l[i][j]==l[i-1][j] or l[i][j]==l[i][j-1]:
                                    return False
        else:
            return True
    else:
        return False

#функция движения плиток вверх
def up(m,l,hw,sc):
    for i in range(hw):
        for j in range(1,hw):
            n=1
            k=1
            while n==1 and j-k>=0:
                if l[j-k][i]==0:
                    l[j-k][i],l[j-k+1][i]=l[j-k+1][i],l[j-k][i]
                    k+=1
                elif l[j-k][i]==l[j-k+1][i]:
                    if l[j-k][i]%2!=1:
                        l[j-k][i]+=(l[j-k+1][i]+1)
                        l[j-k+1][i]=0                        
                        sc+=(l[j-k][i]-1)
                        k+=1
                    else:
                        n=-1
                else:
                    n=-1
    #обновления списка пустых ячеек
    mx = updater(m,l,hw)
    #добавление новой ячейки
    auto_insert(m,l,hw)
    return sc,mx

#функция движения плиток вниз
def down(m,l,hw,sc):
    for i in range(hw):
        for j in range(hw-2,-1,-1):
            n=1
            k=1
            while n==1 and j+k<=hw-1:
                if l[j+k][i]==0:
                    l[j+k][i],l[j+k-1][i]=l[j+k-1][i],l[j+k][i]
                    k+=1
                elif l[j+k][i]==l[j+k-1][i]:
                    if l[j+k][i]%2!=1:
                        l[j+k][i]+=(l[j+k-1][i]+1)
                        l[j+k-1][i]=0
                        sc+=(l[j+k][i]-1)
                        k+=1                        
                    else:
                        n=-1
                else:
                    n=-1
    mx = updater(m,l,hw)
    auto_insert(m,l,hw)
    return sc,mx 

#функция движения плиток в права
def right(m,l,hw,sc):
    for i in range(hw):
        for j in range(hw-2,-1,-1):
            n=1
            k=1
            while n==1 and j+k<=hw-1:
                if l[i][j+k]==0:
                    l[i][j+k],l[i][j+k-1]=l[i][j+k-1],l[i][j+k]
                    k+=1
                elif l[i][j+k]==l[i][j+k-1]:
                    if l[i][j+k]%2!=1:
                        l[i][j+k]+=(l[i][j+k-1]+1)
                        l[i][j+k-1]=0
                        sc+=(l[i][j+k]-1)
                        k+=1                        
                    else:
                        n=-1
                else:
                    n=-1
    mx = updater(m,l,hw)
    auto_insert(m,l,hw)
    return sc,mx
    
#функция движения плиток влево
def left(m,l,hw,sc):
    for i in range(hw):
        for j in range(1,hw):
            n=1
            k=1
            while n==1 and j-k>=0:
                if l[i][j-k]==0:
                    l[i][j-k],l[i][j-k+1]=l[i][j-k+1],l[i][j-k]
                    k+=1
                elif l[i][j-k]==l[i][j-k+1]:
                    if l[i][j-k]%2!=1:
                        l[i][j-k]+=(l[i][j-k+1]+1)
                        l[i][j-k+1]=0
                        sc+=(l[i][j-k]-1)
                        k+=1                        
                    else:
                        n=-1
                else:
                    n=-1
    mx = updater(m,l,hw)
    auto_insert(m,l,hw)
    return sc,mx

#функция добавления новой плитки
def auto_insert(m,l,hw):
    #смотрим есть ли свободные ячейки
    a=len(m)
    if a!=0:
        #выбор одной из пустых ячеек
        b=random.randint(0,a-1)
        #запись в список пустых производится индексированными числами а эта функция деиндексирует это число
        c,d=de_indexer(m[b],hw)
        #n число от 0 до 1
        n=random.random()
        #с вероятностью 10% будет 4 и 90% будет 2
        if n>=0.9:
            l[c][d]=1024
        else:
            l[c][d]=512

#функция обновления списка пустых ячеек
def updater(m,l,hw):
    #очищаем список
    m.clear()
    #проходимся по всем ячейкам главного списка и если ячейка пустая индексируем ее и добавляем индекс в список пустых ячеек
    mx = 0
    for i in range(hw):
        for j in range(hw):
            if len(str(l[i][j]))>mx:
                mx = len(str(l[i][j]))
            if l[i][j]%2==1:
                l[i][j]-=1
            if l[i][j]==0:
                a=indexer(i,j,hw)
                m.append(a)
    return mx

#вывод вложенного списка
def printer(l,mx):
    for i in l:
        #распаковка списка
        s = []
        for j in i:
            s.append(str(j).rjust(mx,' '))
        print(*s)

#индексация
def indexer(a,b,hw):
    return(a*hw+b+1)

#деиндексация
def de_indexer(a,hw):
    a-=1
    return(a//hw,a%hw)

#вызов основной функции
main(table_hw,bc)