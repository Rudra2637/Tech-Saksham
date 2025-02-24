students={}
student_ids=[]

def add_record(std_id, std_name, std_age, std_grade):
    students[std_id]=(std_name, std_age, std_grade)
    student_ids.append(std_id)
    return 0

def view_records():
    print("Student Id\tName\tAge\tGrade")
    for i in range(len(student_ids)):
        view_id = student_ids[i]
        view_name, view_age, view_grade = students[view_id]
        print("{}\t\t{}\t{}\t{}".format(student_ids[i],view_name, view_age, view_grade))
    return 0

def search_record(std_id):
    search_result = students.get(std_id, None)
    search_name, search_age, search_grade = search_result if search_result else ('Not Found', '', '')
    print(f"Search Result - ID: {std_id}, Name: {search_name}, Age: {search_age}, Grade: {search_grade}")
    return 0

def update_record(std_id, std_name, std_age, std_grade):
    students[std_id]=(std_name, std_age, std_grade)
    return 0
    
def delete_record(std_id):
    del students[std_id]
    student_ids.remove(std_id)

while True:
    num = int(input("\n    1. Add Student Record\n    2. View All Students\n    3. Search Student\n    4. Update Student Information\n    5. Delete Student Record\n    6. Exit\n==> "))
    if num == 1:
        std_id = int(input("Enter the student's id: "))
        std_name = input("Enter the student's name: ")
        std_age = int(input("Enter the student's age: "))
        std_grade = input("Enter the student's grade: ")
        add_record(std_id, std_name, std_age, std_grade)
        print("Record Inserted Successfully!")
    if num == 2:
        view_records()
    if num == 3:
        std_id = int(input("Enter the id to be searched: "))
        search_record(std_id)
    if num == 4:
        std_id = int(input("Enter the student's id: "))
        std_name = input("Enter the student's name: ")
        std_age = int(input("Enter the student's age: "))
        std_grade = input("Enter the student's grade: ")
        update_record(std_id, std_name, std_age, std_grade)
        print("Record Updated Successfully!")
    if num ==  5:
        std_id = int(input("Enter the id to be deleted: "))
        delete_record(std_id)
        print("Record Deleted Successfully!")
    if num == 6:
        break