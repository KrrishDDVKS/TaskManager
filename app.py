import streamlit as st
import mysql.connector

# Establish a connection to MySQL Server

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    database="taskmanager",
    password='KrrishDDVK$7'
)
mycursor=mydb.cursor()
print("Connection Established")

# Create Streamlit App

def main():
    st.title("Task Tracker System");

    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Select an Operation",("Create","Update","Delete","Status"))
    # Perform Selected CRUD Operations
    if option=="Create":
        st.subheader("Create a Task")
        name=st.text_input("Task Name")
        descr=st.text_input("Description")
        dd = st.date_input("DueDate")
        stat=st.selectbox("Status",("Pending","Inprogress","Completed"))
        pri=st.selectbox("Priority",("High","Medium","Low"))
        pro=st.selectbox("Projectname",("ADAS","ASUX"))
        if pro=="ADAS":    
            a=st.selectbox("Assigned to",("hanu","ram","laksh"))
        else:
            a=st.selectbox("Assigned to",("Krishna","Arjun","B.Ram"))
    

        if st.button("Create"):
            sql="select project_id from projects where project_name= %s"
            val=(pro,)
            mycursor.execute(sql,val)
            pro = mycursor.fetchall()

                
            sql="select status_id from Task_Statuses where status_name= %s"
            val=(stat,)
            mycursor.execute(sql,val)
            stat = mycursor.fetchall()
            
            
            sql="select priority_id from Task_Priorities where priority_name= %s"
            val=(pri,)
            mycursor.execute(sql,val)
            pri = mycursor.fetchall()
            print(pri)

            sql= "insert into Tasks(task_name,description,deadline,status_id,priority_id,project_id) values(%s,%s,%s,%s,%s,%s)"
            val= (name,descr,dd,stat[0][0],pri[0][0],pro[0][0])
            mycursor.execute(sql,val)
            mydb.commit()
            

            sql="select user_id from Users where name= %s"
            val=(a,)
            mycursor.execute(sql,val)
            a = mycursor.fetchall()
            print(a)

            sql="select CURDATE()"
            mycursor.execute(sql)
            d = mycursor.fetchall()
            print(d)

            sql="select task_id from Tasks ORDER BY task_id DESC LIMIT 1;"
            mycursor.execute(sql)
            i = mycursor.fetchall()
            print(i)

            sql="insert into Task_Assignees(task_id,user_id,assignment_date) values(%s,%s,%s)"
            val= (i[0][0],a[0][0],d[0][0])
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Task Created Successfully!!!")

    elif option=="Status":
        st.subheader("Task Status")
        sql='select t.task_id, t.task_name, t.description, t.deadline, ts.status_name, tp.priority_name, p.project_name,tea.team_name, u.name, u.email from Tasks t join Task_Statuses ts on t.status_id=ts.status_id join Task_Priority tp on t.priority_id=tp.priority_id join Projects p on t.project_id=p.project_id join Team_Projects tep on t.project_id=tep.project_id join Teams tea on tep.team_id=tea.team_id join Task_Assignees ta on t.task_id=ta.task_id join Users u on ta.user_id=u.user_id;'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for row in result:
            st.subheader(row)



    elif option=="Update":
        st.subheader("Update a Task")
        id=st.text_input("ID")
        name=st.text_input("Task new Name")
        descr=st.text_input("new Description")
        dd = st.date_input("new DueDate")
        stat=st.selectbox("new Status",("Pending","Inprogress","Completed"))
        pri=st.selectbox("new Priority",("High","Medium","Low"))
        pro=st.selectbox("new Projectname",("ADAS","ASUX"))
        sql="select project_id from projects where project_name= %s"
        val=(pro,)
        mycursor.execute(sql,val)
        pro = mycursor.fetchall()
        sql="select status_id from Task_Statuses where status_name= %s"
        val=(stat,)
        mycursor.execute(sql,val)
        stat = mycursor.fetchall()
        sql="select priority_id from Task_Priorities where priority_name= %s"
        val=(pri,)
        mycursor.execute(sql,val)
        pri = mycursor.fetchall()

        if st.button("Update"):
            sql="update Tasks set task_name=%s,description=%s,deadline=%s,status_id=%s,priority_id=%s,project_id=%s where task_id =%s"
            val= (name,descr,dd,stat[0][0],pri[0][0],pro[0][0],id)
            print(val)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Task Updated Successfully!!!")




    elif option=="Delete":
        st.subheader("Delete a Task")
        id=st.number_input("Task ID",min_value=1)
        if st.button("Delete"):
            sql="delete from Task_Assignees where task_id =%s"
            val=(id,)
            mycursor.execute(sql,val)
            mydb.commit()
           
            sql="delete from Tasks where task_id =%s"
            val=(id,)
            mycursor.execute(sql,val)
            mydb.commit()
            
            st.success("Task Deleted Successfully!!!")


if __name__ == "__main__":
    main()
