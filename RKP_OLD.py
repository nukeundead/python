import copy
from datetime import *

append = False

today = datetime.date(datetime.today())
current_year = today.year
current_month = today.month
current_day = today.day

area = 44.8
months=['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
services = ['В/О', 'ГАЗ', 'ГВС', 'ДМФН', 'КАПР', 'ОТОП', 'РФ', 'Э/Э', 'СИРЖП', 'ХВС', 'ЦВ']
permanent_index = [1, 3, 4, 5, 6, 8, 10]
varios_index = [2, 7, 9]
print_consum_index = [0, 2, 5, 7, 9, 11]
print_indications_index = [2, 7, 9, 11]

def prev_month(date):
    m = date.month - 1
    y = date.year
    if m<=0:
        m = 12 + m
        y = date.year - 1
    return m,y

def deltadays(date1, date2):
    date1=datetime.toordinal(date1)
    date2=datetime.toordinal(date2)
    delta=max(date1, date2)-min(date1, date2)
    return delta

def numtoword_month(a):
    return months[a - 1]

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def lines_count(file_name):
    i = 0
    with open(file_name,'r') as file:
        for line in file:
            i+=1
    file.close()
    return(i)

def read_last_line_as_list(file_name):
    table = []
    with open(file_name,'r') as file:
        lines_counter = 0
        lastline = lines_count(file_name)
        for line in file:
            lines_counter+=1
            if lines_counter==lastline:
                s = line.split('\t')
                for i in range(len(s)):
                    if isfloat(s[i]) and float(s[i])%1==0:
                        table.append(int(float(s[i])))
                    elif isfloat(s[i]) and float(s[i])%1>0:
                        table.append(float(s[i]))
                    else:
                        table.append(s[i])
    file.close()
    return (table)

def append_to_file(file_name, list_name):
    with open(file_name, 'a') as file:
        file.write('\n')
        for i in range(len(list_name)):
            if i==0:
                file.write(str(list_name[i]))
            else:
                file.write('\t' + str(list_name[i]))
    file.close()

def checking_input(msg, last_indication, limit):
    Error=True
    while Error==True:
        try:
            indication=int(input(msg))
            Error=False
            if indication >= last_indication and indication < (last_indication + limit):
                Error=False
            else:
                int(msg)
            return indication
        except ValueError:
            print('Показание должно быть целым числом не меньше предыдущего')
            Error=True

def input_indications(last_indications):
    water_limit=20
    energy_limit=300
    new_indications = [0, 1, 'gvs', 1, area, 0.6048, area, 'e/e', area, 'hvs', area, 'date']
    #new_indications = copy.deepcopy(last_indications)
    #new_indications[2] = int(input('Введите показание ГВС '))
    print('Прошлые показания:')
    print('ГВС: ', last_indications[2], " куб. м")
    print('ХВС: ', last_indications[9], " куб. м")
    print('Э/Э: ', last_indications[7], " кВт")
    new_indications[2] = checking_input('Введите показание ГВС ', last_indications[2], water_limit)
    #new_indications[9] = int(input('Введите показание ХВС '))
    new_indications[9] = checking_input('Введите показание ХВС ', last_indications[9], water_limit)
    #new_indications[7] = int(input('Введите показание Э/Э '))
    new_indications[7] = checking_input('Введите показание Э/Э ', last_indications[7], energy_limit)
    #print(last_indications)
    #print(new_indications)
    new_indications[11] = today
    return new_indications

def consumption(last_indications, new_indications):
    consumption = [0, 1, 0, 1, area, 0.6048, area, 0, area, 0, area]
    for i in varios_index:
        consumption[i] = new_indications[i] - last_indications[i]
    consumption[0] = consumption[2] + consumption[9]#VO
    print()
    print('{: <31}{: >8.0f}{: <}'.format('Потребление ГВС в этом месяце:', consumption[2], ' куб. м'))
    print('{: <31}{: >8.0f}{: <}'.format('Потребление ХВС в этом месяце:', consumption[9], ' куб. м'))
    print('{: <31}{: >8.0f}{: <}'.format('Водоотведение в этом месяце:', consumption[0], ' куб. м'))
    print('{: <31}{: >8.0f}{: <}'.format('Потребление Э/Э в этом месяце:', consumption[7], ' кВт'))
    consumption.append(today)
    #print('Потребление:',consumption)
    return consumption

def ifint(a):
    if a%1==0:
        return round(a, 0)#int(a)
    else:
        return round(a, 2)

def cost(consumption, current_tariffs, preferences):
    rate = []
    economy = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(consumption) - 1):
        if i==4:
            rate.append(consumption[i] * current_tariffs[i] - preferences[i])
            economy[4] = preferences[4]
        else:
            rate.append(consumption[i] * current_tariffs[i] * preferences[i])
            economy[i] = consumption[i] * current_tariffs[i] * (1 - preferences[i])
    total_cost = sum(rate)
    rate.append(total_cost)#rate[11]
    
    water_cost = rate[0] + rate[2] + rate[9]
    water_part = water_cost / total_cost
    rate.append(water_cost)#rate[12]

    light_part = rate[7] / total_cost
    rate.append(rate[7])#rate[13]
    
    tsg_cost = rate[6] + rate[8] + rate[10]
    tsg_part = tsg_cost / total_cost
    rate.append(tsg_cost)#rate[14]
    
    else_cost = rate[1] + rate[3] + rate[4] + rate[5]
    else_part = else_cost / total_cost
    else_cost = ifint(else_cost)
    rate.append(else_cost)#rate[15]
    total_economy = sum(economy)
    economy_part = total_economy / (total_economy + total_cost)
    rate.append(total_economy)#rate[16]
    print(rate[len(rate) - 1])

    for i in range(len(rate)):
        #rate[i] = round(rate[i],2)#round(,2)
        rate[i] = ifint(rate[i])
        print(rate[i])
        
    #print(rate)
    print()
    print('{: <31}{: >8.2f}{: <}'.format('Сумма к оплате:', total_cost, ' р.'))
    print()
    print('В том числе:')
    print('{: <31}{: >8.2f}{: <}{: >7.2%}'.format('Вода:', water_cost, ' р.', water_part))
    print('{: <31}{: >8.2f}{: <}{: >7.2%}'.format('Свет:', rate[7], ' р.', light_part))
    print('{: <31}{: >8.2f}{: <}{: >7.2%}'.format('ТСЖ:', tsg_cost, ' р.', tsg_part))
    print('{: <31}{: >8.2f}{: <}{: >7.2%}'.format('Прочее:', else_cost, ' р.', else_part))
    print()
    print('{: <31}{: >8.2f}{: <}{: >7.2%}'.format('Сэкономлено:', total_economy, ' р.', economy_part))
    rate.append(today)#rate[17]
    #print(rate)
    return rate
    
def calc():
    current_tariffs = read_last_line_as_list('tariffs.txt')
    #print('Актуальные тарифы:', current_tariffs)
    prev_indications = read_last_line_as_list('indications.txt')
    last_indications = [0, 1, prev_indications[0], 1, area, 0.6048, area, prev_indications[1], area, prev_indications[2], area, prev_indications[3]]
    prev_date_string=prev_indications[3]
    #print(prev_date_string)
    prev_date=datetime.strptime(prev_date_string,'%Y-%m-%d')
    prev_date=datetime.date(prev_date)
    #print(prev_date)
    delta_days=deltadays(today, prev_date)
    #print('delta_days',delta_days)
    #print('Последние показания:',last_indications)
    preferences = read_last_line_as_list('preferences.txt')
    #print('Актуальные льготы:', preferences)
    new_indications = input_indications(last_indications)
    consum = consumption(last_indications, new_indications)
    rate = cost(consum, current_tariffs, preferences)
    print_indications = []
    for i in print_indications_index:
        print_indications.append(new_indications[i])
    if append==True: append_to_file('indications.txt', print_indications)
    print_consum = []
    for i in print_consum_index:
        print_consum.append(consum[i])
    if append==True: append_to_file('consumption.txt', print_consum)
    if append==True: append_to_file('cost.txt', rate)
    rez = []
    print()
    rez.append('Показания квартирных счётчиков воды')
    rez.append('За период с 20 {:} {:} г. по 20 {:} {:} г.'.format(numtoword_month(previos_period_month), previos_period_year, numtoword_month(current_month), current_year))
    rez.append('ЖСК "Информатор"')
    rez.append('Ф.И.О.: Ивенский Никита Андреевич, тел. 8 (915) 094-93-50')
    rez.append('Адрес: Москва, ул. 2-я Пугачевская, д. 3, к. 1, кв. 85')
    rez.append('Дата заполнения: 20 {:} {:} г.'.format(numtoword_month(current_month), current_year))
    rez.append('{: <32} {: <31}'.format('Показания счётчика холодной воды', 'Показания счётчика горячей воды'))
    rez.append('{: <32} {: <31}'.format('Заводской №', 'Заводской №'))
    rez.append('{: <28}{: >4} {: <27}{: >4}'.format('Текущее, м3', new_indications[9], 'Текущее, м3', new_indications[2]))
    rez.append('{: <28}{: >4} {: <27}{: >4}'.format('Предыдущее, м3', prev_indications[2], 'Предыдущее, м3', prev_indications[0]))
    rez.append('{: <28}{: >4} {: <27}{: >4}'.format('Расход, м3', print_consum[4], 'Расход, м3', print_consum[1]))
    rez.append('')
    rez.append('Плательщик __________')
    #name='Nikita'
    #rez.append(F'Плательщик, {name}')#f-строка
    
    with open('rez.txt','a') as file:
        for i in range(len(rez)):
            print(rez[i])
            file.write(str(rez[i]) + '\n')
        file.write('----------------------------------------------------------------\n')
    file.close()

previos_period_month, previos_period_year=prev_month(today)    
calc()
input('Нажмите любую клавишу...')
print('Готово!')
