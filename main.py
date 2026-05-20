# Upgraded Exam Seating Arrangement System


import mysql.connector
import random
import csv

# -----------------------------
# MySQL Connection
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="exam_seating"
)

cursor = conn.cursor()


class ExamSeatingSystem:

    def __init__(self):
        self.students = []
        self.seating = {}
        self.seat_lookup = {}
        self.blocks = {}
        self.total_students = 0
        self.seats_per_row = 0
        self.branch_statistics = {}

    # -----------------------------
    # Add Blocks and Rooms
    # -----------------------------
    def add_blocks_and_rooms(self):
        if self.blocks:
            print("Blocks and rooms already created")
            return
       
        cursor.execute("DELETE FROM seating")
        cursor.execute("DELETE FROM rooms")
        cursor.execute("DELETE FROM blocks")
        conn.commit()
        self.blocks = {}
        self.seating = {}
        self.seat_lookup = {}


        while True:
            try:
                total_blocks = int(input("Enter number of blocks: "))

                if total_blocks > 0:
                    break
                else:
                    print("Enter value greater than 0")

            except ValueError:
                print("Enter valid number")

        for i in range(total_blocks):

            block_name = chr(65 + i)

            print(f"\nGenerated Block: {block_name}")

            while True:
                try:
                    total_rooms = int(input(f"Enter number of rooms in {block_name}: "))

                    if total_rooms > 0:
                        break
                    else:
                        print("Enter value greater than 0")

                except ValueError:
                    print("Enter valid number")

            while True:
                try:
                    self.seats_per_row = int(input(f"Enter seats per row in {block_name}: "))

                    if self.seats_per_row > 0:
                        break
                    else:
                        print("Enter value greater than 0")

                except ValueError:
                    print("Enter valid number")

            while True:
                try:
                    capacity = int(input(f"Enter capacity for each room in {block_name}: "))

                    if capacity > 0:
                        break
                    else:
                        print("Capacity must be greater than 0")

                except ValueError:
                    print("Enter valid capacity")

            self.blocks[block_name] = {}
            query= "INSERT INTO blocks(block_name) VALUES(%s)"
            values= (block_name,)
            cursor.execute(query,values)
            conn.commit()
            print("Inserted into DB:",block_name)

            for j in range(total_rooms):

                block_letter = block_name[-1]
                room_name = f"{block_letter}{j+1}"

                self.blocks[block_name][room_name] = capacity

                query = """
                INSERT INTO rooms(room_name, capacity, block_name)
                VALUES (%s, %s, %s)
                """

                values = (room_name, capacity, block_name)

                cursor.execute(query, values)
                conn.commit()
            print(f"{total_rooms} rooms generated successfully for Block {block_name}")
        print("\nBlocks and rooms added successfully!")

    # -----------------------------
    # Generate Students
    # -----------------------------
    def generate_students(self, branch_students):

        students = []

        for branch in branch_students:
            total = branch_students[branch]

            for i in range(1, total + 1):

                if i < 10:
                    roll = branch + "000" + str(i)
                elif i < 100:
                    roll = branch + "00" + str(i)
                elif i < 1000:
                    roll = branch + "0" + str(i)
                else:
                    roll = branch + str(i)

                students.append(roll)
                query = """
                INSERT INTO students(roll_no, branch)
                VALUES (%s, %s)
                """

                values = (roll, branch)

                cursor.execute(query, values)
                conn.commit()

        random.shuffle(students)
        return students

    # -----------------------------
    # Generate Seating
    # -----------------------------
    def generate_seating(self):
        cursor.execute("DELETE FROM seating")
        conn.commit()
        cursor.execute("DELETE FROM students")
        conn.commit()

        if not self.blocks:
            print("Please add blocks and rooms first.")
            return

        # Branch count
        while True:
            try:
                num_branches = int(input("Enter number of branches: "))

                if num_branches > 0:
                    break
                else:
                    print("Enter value greater than 0")

            except ValueError:
                print("Enter valid number")

        branches = set()

        while len(branches) < num_branches:

            branch = input("Enter branch name: ").upper()

            if branch == "":
                print("Branch name cannot be empty")
            elif branch in branches:
                print("Branch already entered")
            else:
                branches.add(branch)

        branch_students = {}
        self.branch_statistics = {}

        for branch in branches:

            while True:
                try:
                    count = int(input(f"Enter number of students in {branch}: "))

                    if count > 0:
                        branch_students[branch] = count
                        self.branch_statistics[branch] = count
                        break
                    else:
                        print("Enter value greater than 0")

                except ValueError:
                    print("Enter valid number")

        

        # Generate student list
        self.students = self.generate_students(branch_students)
        self.total_students = len(self.students)

        # Calculate total capacity
        total_capacity = 0

        for block in self.blocks:
            for room in self.blocks[block]:
                total_capacity += self.blocks[block][room]

        if self.total_students > total_capacity:
            print("\nNot enough room capacity!")
            print(f"Total Capacity: {total_capacity}")
            print(f"Total Students: {self.total_students}")
            return

        # Seating Allocation
        index = 0
        self.seating = {}
        self.seat_lookup = {}

        for block in self.blocks:

            self.seating[block] = {}

            for room, capacity in self.blocks[block].items():

                self.seating[block][room] = []

                row = 1
                seat = 1

                for _ in range(capacity):

                    if index >= self.total_students:
                        break

                    student = self.students[index]

                    self.seating[block][room].append((student, row, seat))
                    query = """
                    INSERT INTO seating(student_roll, block_name, room_name, row_no, seat_no)
                    VALUES (%s, %s, %s, %s, %s)
                    """

                    values = (student, block, room, row, seat)

                    cursor.execute(query, values)
                    conn.commit()

                    self.seat_lookup[student] = (
                        block,
                        room,
                        row,
                        seat
                    )

                    seat += 1

                    if seat > self.seats_per_row:
                        seat = 1
                        row += 1

                    index += 1

        print("\nSeating generated successfully!")

    # -----------------------------
    # Display Seating
    # -----------------------------
    def display_seating(self):

        query = """
        SELECT seating.student_roll,
                seating.block_name,
                seating.room_name,
                seating.row_no,
                seating.seat_no,
                rooms.capacity
        FROM seating
        JOIN rooms
        ON seating.room_name = rooms.room_name
        """

        cursor.execute(query)

        records = cursor.fetchall()

        print("\nSEATING ARRANGEMENT\n")

        for row in records:

            student, block, room, row_no, seat_no, capacity = row

            print(
                f"Student: {student} | "
                f"Block: {block} | "
                f"Room: {room} | "
                f"Row: {row_no} | "
                f"Seat: {seat_no} | "
                f"Capacity: {capacity}")

    # -----------------------------
    # Search Student
    # -----------------------------
    def search_student(self):

        print("\n1. Search by Roll Number")
        print("2. Search by Room")
        print("3. Search by Block")
        print("4. Search by Branch")

        choice = input("Enter choice: ")

        if choice == "1":

            roll = input("Enter student roll number: ").upper()

            query = """
            SELECT * FROM seating
            WHERE student_roll = %s
            """

            values = (roll,)

        elif choice == "2":

            room = input("Enter room name: ").upper()

            query = """
            SELECT * FROM seating
            WHERE room_name = %s
            """

            values = (room,)

        elif choice == "3":

            block = input("Enter block name: ").upper()

            query = """
            SELECT * FROM seating
            WHERE block_name = %s
            """

            values = (block,)

        elif choice == "4":

            branch = input("Enter branch name: ").upper()

            query = """
            SELECT seating.*, students.branch
            FROM seating
            JOIN students
            ON seating.student_roll = students.roll_no
            WHERE students.branch = %s
            """

            values = (branch,)

        else:
            print("Invalid choice")
            return

        cursor.execute(query, values)

        records = cursor.fetchall()

        if records:

            print("\nSearch Results:\n")

            for row in records:
                print(row)

        else:
            print("No records found")

    # -----------------------------
    # Save to File
    # -----------------------------
    def save_to_file(self):

        query = "SELECT * FROM seating"

        cursor.execute(query)

        records = cursor.fetchall()

        if not records:
            print("No seating data found")
            return

        with open("seating_plan.txt", "w") as file:

            file.write("EXAM SEATING ARRANGEMENT\n\n")

            for row in records:
                file.write(str(row) + "\n")

        
        print("Seating saved to seating_plan.txt")
        with open("seating_plan.csv", "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Seat ID",
                "Student Roll",
                "Block",
                "Room",
                "Row",
                "Seat"
            ])

            query = "SELECT * FROM seating"

            cursor.execute(query)

            records = cursor.fetchall()

            for row in records:
                writer.writerow(row)

        print("CSV file saved successfully")
    # -----------------------------

    # -----------------------------
    # Statistics
    # -----------------------------
    def show_statistics(self):

        print("\n========== STATISTICS ==========")

        # Total students
        total_students = len(self.students)

        # Total rooms
        total_rooms = 0

        # Total capacity
        total_capacity = 0

        for block in self.blocks:

            total_rooms += len(self.blocks[block])

            for room in self.blocks[block]:
                total_capacity += self.blocks[block][room]

        occupied_seats = total_students

        empty_seats = total_capacity - occupied_seats

        # Occupancy %
        if total_capacity > 0:
            occupancy = (occupied_seats / total_capacity) * 100
        else:
            occupancy = 0

        print(f"\nTotal Students      : {total_students}")
        print(f"Total Rooms         : {total_rooms}")
        print(f"Total Capacity      : {total_capacity}")
        print(f"Occupied Seats      : {occupied_seats}")
        print(f"Empty Seats         : {empty_seats}")
        print(f"Occupancy Percentage: {occupancy:.2f}%")

        print("\nBranch-wise Student Count:\n")

        for branch in self.branch_statistics:
            print(f"{branch} : {self.branch_statistics[branch]}")

    # -----------------------------
    # Main Menu
    # -----------------------------
    def run(self):

        while True:

            print("\n1.Add Blocks and Rooms")
            print("2.Generate Seating")
            print("3.Display Seating")
            print("4.Search Student")
            print("5.Save to File")
            print("6.Show Statistics")
            print("7.Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.add_blocks_and_rooms()

            elif choice == "2":
                self.generate_seating()

            elif choice == "3":
                self.display_seating()

            elif choice == "4":
                self.search_student()

            elif choice == "5":
                self.save_to_file()

            elif choice == "6":
                self.show_statistics()

            elif choice == "7":
                
                cursor.close()
                conn.close()
                print("Exiting Program")
                break

            else:
                print("Choose between 1 to 7")


# -----------------------------
# Run Program
# -----------------------------
system = ExamSeatingSystem()
system.run()
