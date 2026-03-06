import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import uvicorn

orders_db=[]

@strawberry.type
class Order:
    id:str
    customer:str
    total:float
    status:str
    priority:int

@strawberry.type
class Query:
    @strawberry.field
    def orders(self)->list[Order]:
        result=[]
        for item in orders_db:
            order=Order(id=item["id"],customer=item["customer"],total=item["total"],status=item["status"],priority=item["priority"])
            result.append(order)
        return result

    @strawberry.field
    def order(self,id:str)->Order|None:
        for item in orders_db:
            if item["id"]==id: return Order(id=item["id"],customer=item["customer"],total=item["total"],status=item["status"],priority=item["priority"])
        return None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def createOrder(self,customer:str,total:float,status:str,priority:int)->Order:
        max_id=0
        for order in orders_db:
            current_id=int(order["id"])
            if current_id>max_id:max_id=current_id
        new_id=str(max_id+1)
        new_order={"id":new_id,"customer":customer,"total":total,"status":status,"priority":priority}
        orders_db.append(new_order)
        return Order(id=new_order["id"],customer=new_order["customer"],total=new_order["total"],status=new_order["status"],priority=new_order["priority"])

schema=strawberry.Schema(query=Query,mutation=Mutation)
app=FastAPI()
app.include_router(GraphQLRouter(schema),prefix="/graphql")


@app.get("/")
async def main():return {"link":"http://localhost:8122/graphql"}

uvicorn.run(app, host="0.0.0.0", port=8122)