from datetime import datetime, timezone
import uuid
from db import make_connection
from collections import defaultdict


def normalize_string(value: str) -> str: # a function that accepts a string to strip its whitespace from beginning and end and return it as string....
    return value.strip()


def normalize_category(value: str) -> str: #a function that accepts a string to strip as well as convert uppercase to lowercase and return it as string....
    return value.strip().lower()

def get_expense_by_id(expense_id:str):
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM expensestore 
    WHERE id=?''',(expense_id,)
    )
    row=cursor.fetchone() # get the first result from the query....
    conn.close() # closes the connection

    if not row: 
        return None
    
    return dict(row) #converts row into python dict....

def add_expenses(amount:float, item:str, paid_on:str, category:str):
    # validation....
    if amount<=0:
        raise ValueError("Invalid amount!!")
    if not item:
        raise ValueError("Item required!!")
    if not paid_on:
        raise ValueError("Date is required!!")
    if not category:
        raise ValueError("Category is required!!")
    # normalization....
    item= normalize_string(item)
    paid_on = paid_on.isoformat()
    category=normalize_category(category)

    # uuid generates random and unique ids.... 
    expense_id=str(uuid.uuid4())
    now=datetime.now(timezone.utc)
    iso_now=now.isoformat()
    created_at=iso_now
    updated_at=iso_now
    deleted_at=None
    deleted=0
    
    conn=make_connection()
    cursor=conn.cursor()

    cursor.execute('''
    INSERT INTO expensestore(id,amount,item,paid_on,category,deleted,created_at,updated_at,deleted_at)
    VALUES(?,?,?,?,?,?,?,?,?)
    ''', (expense_id,amount,
          item,paid_on,
          category,deleted,
          created_at,updated_at,
          deleted_at)
          )
    conn.commit()
    conn.close()
    return get_expense_by_id(expense_id)

def update_expense(expense_id: str , updated_data: dict):
    # Fetch + validate....
    expense = get_expense_by_id(expense_id)
    if not expense:
        raise ValueError("Expense not found")
    
    if expense["deleted"]:
        raise ValueError("Cannot update a deleted expense")
    
    if not updated_data:
        raise ValueError("No data sent to update")
    
    # Build SET parts....
    set_clauses=[]
    values=[]
    ALLOWED_FIELDS = {"amount", "item", "paid_on", "category"}

    for field,value in updated_data.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError("Invalid field")
        # normalization...
        if field== "item":
            value=normalize_string
        elif field=="paid_on":
            value=value.isoformat()
        elif field=="category":
            value=normalize_category


        set_clauses.append(f"{field}=?")
        values.append(value) 
        
    # Updating updated_at data....
    now=datetime.now(timezone.utc).isoformat()
    set_clauses.append("updated_at = ?")
    values.append(now)

    # Actual sql.....
    set_sql=",".join(set_clauses)
    sql=f"""UPDATE expensestore 
    SET {set_sql} WHERE id=? 
    AND deleted = 0
    """

    # Binding id....
    values.append(expense_id)

    # Execution....
    conn=make_connection()
    cursor=conn.cursor()
    cursor.execute(sql,tuple(values))
    conn.commit()
    conn.close()

    # Returning updated data....
    return get_expense_by_id(expense_id) 

def soft_delete_expense(expense_id:str):

    # Fetch and validate....
    expense= get_expense_by_id(expense_id)

    if not expense:
            raise ValueError("Expense not found")
    if expense["deleted"]:
            raise ValueError("Expense already deleted")
    
    # Updating deleted_at and updated_at....
    now=datetime.now(timezone.utc).isoformat()

    deleted_at=now
    updated_at=now

    # Execution....
    conn=make_connection()
    cursor=conn.cursor()
    cursor.execute('''
    UPDATE expensestore 
    SET deleted=1,
        deleted_at=?,
        updated_at=?
        WHERE id =? AND deleted = 0
    ''',(deleted_at,updated_at,expense_id))
    conn.commit()
    conn.close()

    # Returning updated data....
    return None
    
def restore_expense(expense_id:str):
    
    # Fetch + validate....
    expense = get_expense_by_id(expense_id) 
    if not expense:
        raise ValueError("Expense not found")
    if not expense["deleted"]:
        raise ValueError("Expense is not deleted")
    
    # Updating updated_at data....
    now=datetime.now(timezone.utc).isoformat()
    updated_at=now

    # Execution....
    conn=make_connection()
    cursor=conn.cursor()
    cursor.execute('''
    UPDATE expensestore 
    SET deleted = 0,
        deleted_at= NULL,
        updated_at=?
    WHERE id=? AND deleted=1
    ''',(updated_at,expense_id))

    conn.commit()
    conn.close()

    # Returning Updated data....
    return get_expense_by_id(expense_id)

      
def get_all_expenses():
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM expensestore 
    WHERE deleted = 0'''
    )
    data=cursor.fetchall() #fetch all rows that match the query condition....
    conn.close()

    return [dict(row) for row in data] 

def get_summary():
    conn=make_connection()
    cursor=conn.cursor()

    cursor.execute('''
    SELECT category, SUM(amount) as total 
    FROM expensestore
    WHERE deleted=0 GROUP BY category''')

    data= cursor.fetchall()
    conn.close()
    category_totals=dict(data)
    total_spent=sum(category_totals.values())

    return {
    "by_category": category_totals,
    "total_spent": total_spent
    }

