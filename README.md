# Hashcode 2020 solution (Qualification round)
Our solution for the 2020 [Google Hashcode](https://codingcompetitions.withgoogle.com/hashcode) qualification round problem with libraries and books.

<p align="center">
<img src="/images/hashcode.jpg" alt="Hashcode Logo" width="500"/>
</p>


## Results

| File  | Score |
| ------------- | ------------- |
| a_example ([input](inputs/a_example.txt) \| [output](outputs/a_example.out)) | 21 |
| b_read_on ([input](inputs/b_read_on.txt) \| [output](outputs/b_read_on.out)) | 5,822,900 |
| c_incunabula ([input](inputs/c_incunabula.txt) \| [output](outputs/c_incunabula.out)) | 5,645,747 |
| d_tough_choices ([input](inputs/d_tough_choices.txt) \| [output](outputs/d_tough_choices.out)) | 4,812,730 |
| e_so_many_books ([input](inputs/e_so_many_books.txt) \| [output](outputs/e_so_many_books.out)) | 5,019,670 |
| f_libraries_of_the_world ([input](inputs/f_libraries_of_the_world.txt) \| [output](outputs/f_libraries_of_the_world.out)) | 5,240,161 |
| **Total** | **26,541,229** |


## The problem

You can find the pdf with the problem [here](hashcode_2020_online_qualification_round.pdf).

<img src="/images/hashcode_2020_problem.png" alt="Hashcode 2020 problem" width="500"/>


## Our solution

The code for the solution is in [main.py](main.py). Our approach was a greedy algorithm.

The solution follows these steps:

1. Read the input
2. Calculate a heuristic score for each library with this formula:

   
   <p align="center">
   <img src="https://latex.codecogs.com/svg.latex?\Large&space;library\_score=\frac{library\_books\_score}{library\_signup\_days}" title="library_score = library_books_score / library_signup_days" />
   </p>  

   where library_books_score is calculated like this:

   1. Calculate available days for this library:

   <p align="center">
   <img src="https://latex.codecogs.com/svg.latex?\Large&space;library\_available\_days=all\_days-library\_signup\_days" title="library_available_days = all_days - library_signup_days" />
   </p>

   2. Count how many books can be scanned in these days:

   <p align="center">
   <img src="https://latex.codecogs.com/svg.latex?\Large&space;k=library\_available\_days&space;\times&space;library\_maximum\_books\_scanned\_per\_day" title="k = library_available_days * library_maximum_books_scanned_per_day" />
   </p>

   3. Get the top k books according to their score and sum their scores. This is the *library_books_score*.

3. Sort libraries according to their score
4. For every library in sorted order:
   1. Count how many books from this library (k) can be scanned, like in steps 2i and 2ii, but now take into account the number of signup days from the previous libraries. So if the previous libraries have taken *d* total days for the signup, then the formula from the step 2i becomes:
   <p align="center">
   <img src="https://latex.codecogs.com/svg.latex?\Large&space;library\_available\_days=all\_days-library\_signup\_days-d" title="library_available_days = all_days - library_signup_days - d" />
   </p>
   
   2. From the books of this library, except the books that have already been scanned from the previous libraries, get the top k books according to their score and scan them.

5. Create the output



