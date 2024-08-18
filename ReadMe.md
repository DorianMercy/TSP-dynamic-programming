# Take Home Problem: Surveyor Travel

## Brief

A mobile surveyor is looking for a system to optimise the order that she
visits the many sites on her job list. She has a list of locations with
their coordinates. It is up to you to create a solution in Python (making
use of appropriate libraries) to take the list and create a new list with
the order of where she should go to minimise the total distance she has to
travel. As she is mobile, she is not worried about a start location, or
time constraints at this point. However, the script should complete within
one minute on a normal laptop with a reasonably good solution for the test
cases provided.

Document your code, explaining your approach, any assumptions made, and how
the solution is expected to perform with large inputs.

### Answer

This travelling salesperson problem assumes Euclidean distance used, all nodes interconnected, and symmetric cost on arc directions. Brute force algorithm takes $O(n!)$ time complexity. This algorithm, dynamic programming, memoizes the lowest-cost path to a place via some places, enabling it to know which the next place is to have lowest cost. The time complexity is $O(2^nn^2)$: the via_set is a subset of n places, there are $2^n$ subsets, and for each iteration, the via_set as part of the key gets combined with $O(n)$ to_nodes, and each combination searches through $O(n)$ items in the via_set, which will produce $O(2^nn^2)$ faster than $O(n!)$.

## Instructions

### Setup
Make sure you are setup with a fairly recent version of Python.

Install the required dependencies : `pip install -r requirements.txt`

### Run unit tests

`pytest`
