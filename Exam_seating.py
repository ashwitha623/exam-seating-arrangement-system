import random


class ExamSeatingSystem:

    def __init__(self):
        self.seating = None
        self.seat_lookup = None
        self.blocks = None
        self.seats_per_row = 0
        self.total_students = 0

    # -----------------------------
    # Generate Students Branch-wise
    # -----------------------------
    def generate_students(self, branch_students):
        students = []

        for branch in branch_students:
            total = branch_students[branch]
            for i in range(1, total + 1):
                if i< 10:
                    roll= branch+ "000" +str(i)
                elif i< 100:
                    roll =branch + "00" +str(i)
                elif i< 1000:
                    roll= branch+ "0" + str(i)
                else:
                    roll= branch +str(i)
                students.append(roll)

        # Shuffle for proper branch mixing
        random.shuffle(students)
        return students

    # -----------------------------
    # Divide into Blocks
    # -----------------------------
    def divide_into_blocks(self, students, block_capacity):
        blocks = {}
        block_letter = 'A'

        for i in range(0, len(students), block_capacity):
            block_name = f"Block-{block_letter}"
            blocks[block_name] = students[i:i + block_capacity]
            block_letter = chr(ord(block_letter) + 1)

        return blocks

    # -----------------------------
    # Assign Seats
    # -----------------------------
    def assign_seats(self, blocks, seats_per_row):
        seating = {}
        seat_lookup = {}

        for block, students in blocks.items():
            seating[block] = []
            row = 1
            seat = 1

            for student in students:
                seating[block].append((student, row, seat))
                seat_lookup[student] = (block, row, seat)

                seat += 1
                if seat > seats_per_row:
                    seat = 1
                    row += 1

        return seating, seat_lookup

    # -----------------------------
    # Display Seating
    # -----------------------------
    def display_seating(self):
        if not self.seating:
            print("Generate seating first.")
            return

        for block, data in self.seating.items():
            print("\n" + block)
            print("-" * 30)

            current_row = 1
            row_students = []

            for student, row, seat in data:
                if row != current_row:
                    print(*row_students)
                    row_students = []
                    current_row = row

                row_students.append(student)

            if row_students:
                print(*row_students)

    # -----------------------------
    # Search Student
    # -----------------------------
    def search_student(self):
        if not self.seat_lookup:
            print("Generate seating first.")
            return

        roll = input("Enter Roll Number(e.g : cse0054): ").upper()

        if roll in self.seat_lookup:
            block, row, seat = self.seat_lookup[roll]
            print(f"{roll} is in {block} | Row {row} | Seat {seat}")
        else:
            print("Student not found.")

    # -----------------------------
    # Save to File
    # -----------------------------
    def save_to_file(self):
        if not self.seating:
            print("Generate seating first.")
            return

        with open("seating_plan.txt", "w") as file:
            for block, data in self.seating.items():
                file.write("\n" + block + "\n")
                file.write("-" * 30 + "\n")

                for student, row, seat in data:
                    file.write(f"{student} -> Row {row} Seat {seat}\n")

        print("Seating saved successfully to seating_plan.txt")

    # -----------------------------
    # Show Statistics
    # -----------------------------
    def show_statistics(self):
        if not self.blocks:
            print("Generate seating first.")
            return

        total_blocks = len(self.blocks)
        total_rows = 0

        for students in self.blocks.values():
            rows = len(students) // self.seats_per_row
            if len(students) % self.seats_per_row != 0:
                rows += 1
            total_rows += rows

        print("\n--- Seating Statistics ---")
        print("Total Students :", self.total_students)
        print("Total Blocks   :", total_blocks)
        print("Total Rows Used:", total_rows)

    # -----------------------------
    # Generate Seating (Full Validation)
    # -----------------------------
    def generate_seating(self):

        if self.seating:
            confirm = input("Seating already exists. Regenerate? (Y/N): ").upper()
            if confirm != 'Y':
                return

        # Number of branches
        while True:
            try:
                num_branches = int(input("Enter number of branches (1-25): "))
                if 1 <= num_branches <= 25:
                    break
                else:
                    print("Please enter between 1 and 25.")
            except ValueError:
                print("Enter a valid number.")

        # Branch names
        branches = set()
        while len(branches) < num_branches:
            branch = input("Enter branch name (CSE/ECE/MECH): ").upper()

            if branch in branches:
                print("Branch already entered.")
            elif branch == "":
                print("Branch name cannot be empty.")
            else:
                branches.add(branch)

        # Students per branch
        branch_students = {}

        for branch in branches:
            while True:
                try:
                    count = int(input(f"Enter number of students in {branch}: "))
                    if count > 0:
                        branch_students[branch] = count
                        break
                    else:
                        print("Must be greater than 0.")
                except ValueError:
                    print("Enter a valid number.")

        # Block capacity
        while True:
            try:
                block_capacity = int(input("Enter block capacity: "))
                if block_capacity > 0:
                    break
                else:
                    print("Must be greater than 0.")
            except ValueError:
                print("Enter a valid number.")

        # Seats per row
        while True:
            try:
                seats_per_row = int(input("Enter seats per row: "))
                if seats_per_row > 0:
                    break
                else:
                    print("Must be greater than 0.")
            except ValueError:
                print("Enter a valid number.")

        # Generate seating
        students = self.generate_students(branch_students)
        self.total_students = len(students)

        self.blocks = self.divide_into_blocks(students, block_capacity)
        self.seats_per_row = seats_per_row

        self.seating, self.seat_lookup = self.assign_seats(
            self.blocks, seats_per_row
        )

        print("Seating generated successfully!")

    # -----------------------------
    # Main Menu
    # -----------------------------
    def run(self):
        while True:
            print("\n1.Generate Seating")
            print("2.Display Seating")
            print("3.Search Student")
            print("4.Save to File")
            print("5.Show Statistics")
            print("6.Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.generate_seating()
            elif choice == "2":
                self.display_seating()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.save_to_file()
            elif choice == "5":
                self.show_statistics()
            elif choice == "6":
                print("Exiting program.")
                break
            else:
                print("Choose between 1 to 6.")


# Run Program
system = ExamSeatingSystem()
system.run()