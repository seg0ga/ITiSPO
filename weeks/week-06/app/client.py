import requests

def build_payload(query: str, variables: dict) -> dict:
    """
    Формирует словарь для отправки GraphQL запроса.

    :param query: Текст запроса (query или mutation).
    :param variables: Словарь с переменными.
    :return: Словарь с ключами "query" и "variables".
    """
    return {"query":query,"variables":variables}


def execute_query(url:str,query:str,variables:dict=None):
    payload=build_payload(query,variables or {})
    try:
        response=requests.post(url,json=payload)
        result=response.json()
        if "errors" in result:print("Ошибки:",result["errors"])
        else:print("Данные:",result.get("data"))

    except Exception as error:print(f"Ошибка выполнения запроса: {error}")



url="http://localhost:8272/graphql"
#↓тут можно написать какой нибудь mutation (я взял из прошлого задания, что проверить клиент на работоспособность ↓
query_create="""
mutation _createOrder($customer:String!,$total:Float!) {
    createOrder(
        customer: $customer,
        total: $total,
        status: "Оплачено",
        priority: 1)
    {
        id
        customer
        total
        status
        priority
    }}
"""
#↓тут можно написать какой нибудь query (я взял из прошлого задания, что проверить клиент на работоспособность ↓
query_get="""
query{
    orders{
        id
        customer
        total
        status
        priority
}}
"""

variables1={"date":"22.06.2006"} #поле из варианта
variables2={"customer":"Демин Сергей","total":666,"date":"22.06.2006"}
variables3={"customer":"Иванов Иван","total":888,"date":"22.06.2006"}
variables4={"customer":"Петров Петр ","total":"777","date":"22.06.2006"}
print("Mutation1:")
execute_query(url,query_create,variables2)
print("Mutation2:")
execute_query(url,query_create,variables3)
print("Mutation3:")
execute_query(url,query_create,variables4)
print("Query:")
execute_query(url,query_get)



project_code="bookings-s05"