#Это имитация реального сервиса, вроде даже похоже....

def next_state(state: str, event: str) -> str:
    if state=="NEW":
        if event=="PAY_OK":return "PAID"
        elif event=="PAY_FAIL":return "CANCELLED"
    elif state=="PAID":
        if event=="complete":return "DONE"
        elif event=="cancel" or event=="fail":return "CANCELLED"
    elif state=="DONE":return "DONE"
    elif state=="CANCELLED":return "CANCELLED"
    return state

orders={}

def create_order(order_id, items):
    orders[order_id]={"status":"NEW","items": items}
    print(f"Заказ {order_id} создан и забронирован")

def process_pay(summa):
    if summa<666:return "PAY_FAIL"
    return "PAY_OK"

def cancel_reserv(order_id):
    print(f"Отмена брони заказа {order_id}")
    return True

def process_order(order_id,items,summa):
    create_order(order_id,items)
    pay_result=process_pay(summa)

    old_status=orders[order_id]["status"]
    new_status=next_state(old_status,pay_result)
    orders[order_id]["status"]=new_status

    if new_status=="PAID": print(f"Заказ {order_id} успешно оплачен")
    elif new_status=="CANCELLED":
        print(f"Платеж не прошел, отменям заказ {order_id}")
        while True:
            if cancel_reserv(order_id):break

#Для запуска и проверки нужно написать заказ так: process_order("номер заказа", [несколько, товаров,можно],цена)
#так как у меня по варианту что-то связанное с билетами, это я и привел в примере, но работать оно может с чем угодно

#пример process_order("666", ["Ряд 10 Место 7","Ряд 10 Место 8","Ряд 10 Место 9"],755)