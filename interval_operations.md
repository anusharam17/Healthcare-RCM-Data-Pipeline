

## Approach

1. Sorting:
   All operations start by sorting the intervals by the starting point. This helps simplify merging and identifying gaps.

2. Merge:
   - Combine intervals that overlap (`current[0] <= last[1]`).
   - Expand the last interval to the max of both ends.

3. Intersect:
   - The common intersection of all intervals is the overlap between the latest start and the earliest end.
   - If the `start <= end`, there's an overlap.

4. Gaps:
   - First, merge overlapping intervals.
   - Then, check the gap between the end of one and start of the next interval.



## Follow-up Questions & Answers

Q1: What is the time complexity of your solution?

* Merge and Gaps: O(n log n)
* Intersect: O(n)

Q2: What is the space complexity?
* Merge and Gaps: O(n)
* Intersect: O(1)

Q3: How would you handle the case where intervals have negative numbers?
A. Negative values are valid in Python lists and sorting works the same way.


Q4: Can you solve this without sorting? What are the trade-offs?
* Yes, but only for unsorted input with additional data structures like heap or segment trees.

* Trade-offs**:
  * More complex implementation.
  * Sorting simplifies the problem.
  * Without sorting, handling overlapping and finding correct intervals becomes messy.

