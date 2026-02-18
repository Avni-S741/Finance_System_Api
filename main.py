
from fastapi import FastAPI,HTTPException 
from schemas import (ExpenseCreate,ExpenseResponse,UpdateExpenseModel)
from db import init_db
from typing import List
from expense_logic import (
    add_expenses,
    update_expense,
    soft_delete_expense,
    restore_expense,
    get_expense_by_id,
    get_all_expenses,
    get_summary
)


app = FastAPI()#object of FastAPI class to access its functions easily.... 
init_db()#load stored expense when the server starts....

@app.get("/")
def root():
    return {"status": "Finance system running"}


@app.post("/expenses",response_model=ExpenseResponse,status_code=201)
def create_expenses(expense:ExpenseCreate):
    try:
        return add_expenses(
            amount=expense.amount,
            item=expense.item,
            paid_on=expense.paid_on,
            category=expense.category
            )
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@app.patch("/expenses/{expense_id}")
def update_expense_api(expense_id:str , updated_data: UpdateExpenseModel):
    try:
        update_expense(expense_id,
                       updated_data.dict(exclude_unset=True)
                       )
        return {"message": "message updated successfully!!"}
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
    

@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense_api(expense_id:str):
    try:
        soft_delete_expense(expense_id)
    except ValueError as e:
         raise HTTPException(status_code=404,detail=str(e))

@app.post("/expenses/{expense_id}/restore")
def restore(expense_id:str):
    try:
        restore_expense(expense_id)
        return {"message": "Expense resotred"}
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    

@app.get("/expenses", response_model=List[ExpenseResponse])
def read_expenses():
    return get_all_expenses()

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def read_expenses(expense_id:str):
    expense=get_expense_by_id(expense_id)

    if not expense:
        raise HTTPException(status_code=404,detail="Expense not found")
    return expense

@app.get("/summary")
def summary():
    return get_summary()
