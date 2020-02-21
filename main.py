import numpy as np
import operator
import sys


def parallel_sort(array_1, array_2, ascending=False):
    if not ascending:
        return zip(*sorted(zip(array_1, array_2), key=operator.itemgetter(0))[::-1])
    return zip(*sorted(zip(array_1, array_2), key=operator.itemgetter(0)))


class Library:

    def __init__(self, id, book_ids, signup_days, max_books_scanned_per_day):
        self.id = id
        self.book_ids = book_ids
        self.signup_days = signup_days
        self.max_books_scanned_per_day = max_books_scanned_per_day

    def get_best_book_ids(self, start_day=0):
        global book_scores, libraries_signup_days, libraries_max_books_scanned_per_day, D, final_books
        available_days = D - self.signup_days - start_day

        available_books = list(set(self.book_ids) - set(final_books))
        current_book_scores = np.take(book_scores, available_books)

        max_num_books = max(min(int(available_days * self.max_books_scanned_per_day), len(available_books)), 0)

        if max_num_books == 0:
            return []

        # get top k books (k=max_num_books)
        ind = np.argpartition(current_book_scores, -max_num_books)[-max_num_books:]

        return np.take(available_books, ind)

    def get_best_books_score(self, start_day=0):

        global book_scores, libraries_signup_days, libraries_max_books_scanned_per_day, D
        available_days = D - self.signup_days - start_day
        max_num_books = max(min(int(available_days * self.max_books_scanned_per_day), len(self.book_ids)), 0)

        current_book_scores = np.take(book_scores, self.book_ids)

        # get top k books (k=max_num_books)
        ind = np.argpartition(current_book_scores, -max_num_books)[-max_num_books:]
        best_books_scores = np.take(current_book_scores, ind)

        return np.sum(best_books_scores)

    def __repr__(self):
        return self.id.__str__()


def sum_book_scores(book_ids):
    global book_scores
    return np.sum(np.take(book_scores, list(book_ids)))


files = ["a_example", "b_read_on", "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]

total_score = 0

for file in files:

    with open("inputs/" + file + ".txt", "r") as f:
        content = f.read().splitlines()
    print(file)

    B, L, D = list(map(int, content[0].split(' ')))

    book_scores = list(map(int, content[1].split(' ')))
    pos = 1
    libraries_num_books = np.zeros(L)
    libraries_signup_days = np.zeros(L)
    libraries_max_books_scanned_per_day = np.zeros(L)
    libraries = np.empty(L, dtype=Library)
    for i in range(L):
        pos += 1
        n, t, m = list(map(int, content[pos].split(' ')))
        libraries_num_books[i] = n
        libraries_signup_days[i] = t
        libraries_max_books_scanned_per_day[i] = m

        pos += 1
        book_ids = np.asarray(list(map(int, content[pos].split(' '))))
        libraries[i] = Library(i, book_ids, t, m)

    sys.stdout.write("\rSolving...")

    library_book_score_counter = np.vectorize(lambda library: library.get_best_books_score())
    libraries_scores = library_book_score_counter(libraries)

    heuristic_score = np.vectorize(lambda book_score, signup_days: book_score / signup_days)
    signup_scores = heuristic_score(libraries_scores, libraries_signup_days)

    signup_scores, libraries_sorted = parallel_sort(signup_scores, libraries)

    final_books = set()
    with open("outputs/" + file + ".out", 'w+') as f:

        f.write(str(L) + "\n")

        start_day = 0
        for i in range(L):

            current_library = libraries_sorted[i]
            chosen_book_ids = current_library.get_best_book_ids(start_day)
            final_books.update(chosen_book_ids)
            start_day += current_library.signup_days

            if len(chosen_book_ids) > 0:
                f.write(str(current_library.id) + " " + str(len(chosen_book_ids)) + "\n")
                f.write(str(' '.join(map(str, chosen_book_ids))) + "\n")
            else:
                f.write(str(current_library.id) + " 1\n")
                f.write(str(current_library.book_ids[0])+"\n")

            progress = 100 * i / (2 * L)
            sys.stdout.write("\rCreating output... (" + str(int(progress)) + " %)")

        score = sum_book_scores(final_books)
        total_score += score

        print("\r- Score:", score)

print("")
print("Total score:", total_score)
