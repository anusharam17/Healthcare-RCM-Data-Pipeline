
Task Scheduler Using Topological Sort (Python)

Problem Description

Design a function that takes in a list of tasks and their dependencies and returns a valid order in which the tasks can be executed. If no valid order exists (due to cycles), return `None`.


Approach

* This problem is solved using "Topological Sort" (Kahn's Algorithm), which works for Directed Acyclic Graphs (DAG).
* We build a graph using `defaultdict` and compute in-degrees for each task.
* Tasks with in-degree 0 are added to a queue.
* We remove them one by one and reduce the in-degrees of their neighbors.
* If we complete all tasks, we return the topologically sorted order. Otherwise, a cycle exists.
             

## Follow-up Questions

1. What is the time complexity of your solution?
A. O(N + E) where:

  * N is the number of tasks.
  * E is the number of dependencies.
  * Each node is processed once and each edge is checked once.

2. What is the space complexity?
A. O(N + E):

  * `graph` stores all edges → O(E)
  * `degree` dictionary and `queue` → O(N)

3. How would you handle the case where intervals can have negative numbers?

This problem doesn’t involve numeric intervals. However, if the task identifiers were numeric and included negative numbers (e.g., `[-1, 0, 2]`), the solution would still work as long as task identifiers are hashable and provided explicitly in the `tasks` list.

4. Can you solve this problem without sorting? What would be the trade-offs?

* No, if the goal is to maintain a valid execution order, topological "sorting is required".
* Without sorting:
  * We may not satisfy dependency requirements.
  * Trade-off: a faster but "invalid" task sequence.
* However, DFS-based topological sorting is an "alternative", but it still sorts in terms of execution order.


