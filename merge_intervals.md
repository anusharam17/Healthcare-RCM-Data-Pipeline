Problem Description:
You need to merge overlapping intervals and return a list of merged intervals. Two intervals overlap if one starts before the other ends.

Approach :

1. Sort the intervals by start time.
2. Initialize a merged list with the first interval.
3. For each interval:
       If it overlaps with the last merged interval, merge them.
       Else, append the new interval to the result.
4. Return the merged list.


Follow-up Questions

Q1: What is the time complexity of your solution?
A: O(n log n) due to sorting.

Q2: What is the space complexity?
A: O(n) – for storing the merged intervals.

Q3: How would you handle the case where intervals can have negative numbers?
A: No change needed. The logic works for negative numbers as long as each interval is a valid range [start, end] with start <= end.

Q4: Can you solve this problem without sorting? What would be the trade-offs?
A: Without sorting, merging overlapping intervals becomes much harder and may require checking every pair, increasing time complexity to O(n^2). Sorting provides a deterministic left-to-right traversal, simplifying the merging logic.

