class Book:
    def __init__(self, book_id, score):
        self.id = book_id
        self.score = score
        self.scanned = False

    def __str__(self):
        return str(self.id)

class Library:
    def __init__(self, library_id, signup_time, ship_per_day):
        self.id = library_id
        self.signup_time = signup_time
        self.ship_per_day = ship_per_day

        self.books = []
        self.scanned_books = []

        self.signing_up = False
        self.signed_up = False

        self.sign_up_start = None

        self.borked = False
        
    def add_book(self, book):
        self.books.append(book)
        self.books.sort(key=lambda x: x.score)

    def get_potential_score(self):
        return sum([x.score for x in self.books])

    def get_time(self):
        time = self.signup_time
        scanned = 0
        for book in self.books:

            if book in self.scanned_books:
                continue

            if scanned == 0:
                time += 1
            
            scanned = (scanned + 1) % self.ship_per_day
        return time

    def get_heuristic_score(self):
        return (1 / self.get_time()) * self.get_potential_score()
        #return self.get_potential_score()
        #return 1 / self.get_time()
        #return self.ship_per_day + 1 / self.get_time()
        #return (1 / self.get_time()) * (self.get_potential_score() + self.ship_per_day)
        #return len(self.books)
    def has_scannable_books(self):
        if self.borked:
            return True
        for book in self.books:
            if not book.scanned:
                self.borked = True
                return True
        return False

    def scan(self):
        # beep
        added = 0
        for book in self.books:
            if not book.scanned:
                added += 1
                book.scanned = True
                self.scanned_books.append(book)
                if added >= self.ship_per_day:
                    return added
        return added

    def __str__(self):
        return f"{self.id} {len(self.scanned_books)}\n" + " ".join([str(x) for x in self.scanned_books])

def solve(file):

    file = open(file, "r")
    content = file.read()
    file.close()

    lines = content.split("\n")
    total_books, total_libraries, days_scanning = [int(x) for x in lines[0].split()]

    books = []
    libraries = []

    i = 0
    for book_score in lines[1].split():
        books.append(Book(i, int(book_score)))
        i += 1

    library_lines = lines[2:]

    for i in range(0, len(library_lines), 2):

        if (library_lines[i] == ""):
            break

        #print([int(x) for x in library_lines[i].split()])
        num_books, signup_time, ship_per_day = [int(x) for x in library_lines[i].split()]
        book_ids = [int(x) for x in library_lines[i + 1].split()]
        
        library = Library(i // 2, signup_time, ship_per_day)

        for book_id in book_ids:
            library.add_book(books[book_id])

        libraries.append(library)
        
    # solve this, yeah!

    sorted_libraries = sorted(libraries, key=lambda x: x.get_heuristic_score())[::-1]
    
    signed_up_libraries = []

    signing_up = False
    total_signed_up = 0

    time = 0

    while time <= days_scanning:

        #print(f"THE TIME IS {time}")
        
        for library in sorted_libraries:

            #print(f"library {library.id}")

            if library.signing_up:

                #print("is signing up")

                if time - library.sign_up_start >= library.signup_time:

                    #print("...but has actually finished signing up!")

                    signed_up_libraries.append(library)

                    library.signing_up = False
                    library.signed_up = True
                    signing_up = False
                    total_signed_up += 1
                    
                continue

            if not library.has_scannable_books():
                continue
            
            if not signing_up and not library.signed_up:

                #print("is starting to sign up")
                
                signing_up = True
                library.signing_up = True
                library.sign_up_start = time

            if not library.signed_up:

                #print("has not signed up and so is being ignored! fuck off!")
                
                continue

            #print("is scanning books")

            library.scan()
            
        time += 1

    amount = 0

    for lib in signed_up_libraries[:]:
        if len(lib.scanned_books) == 0:
            amount += 1
            signed_up_libraries.remove(lib)

    if amount > 0:
        print(f"You moron! You let {amount} libraries be signed up, but they couldn't scan any books! What a muppet.")

    return f"{len(signed_up_libraries)}\n" + "\n".join([str(x) for x in signed_up_libraries])

for file in ["a_example", "b_read_on", "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]:
    result = solve(f"{file}.txt")
    result_file = open(f"{file}_output.txt", "w")
    result_file.write(result)
    result_file.close()
    print(f"We did it! We did {file}!")
input()
