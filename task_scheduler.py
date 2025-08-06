from collections import defaultdict, deque

def task_scheduler(tasks, dependencies):
    # Step 1: Build graph and in-degree dictionary
    graph = defaultdict(list)
    degree = {task: 0 for task in tasks}

    # Step 2: Populate the graph and in-degrees
    for task, prereq in dependencies:
        graph[prereq].append(task)
        degree[task] += 1

    # Step 3: Initialize queue with tasks having no prerequisites
    queue = deque([task for task in tasks if degree[task] == 0])
    order = []

    # Step 4: Perform topological sort (Kahn's Algorithm)
    while queue:
        current = queue.popleft()
        order.append(current)

        for i in graph[current]:
            degree[i] -= 1
            if degree[i] == 0:
                queue.append(i)

    # Step 5: Return order if all tasks are processed, else return None (cycle)
    return order if len(order) == len(tasks) else None

# ---------- Test Cases ----------

tasks1 = ["A", "B", "C", "D"]
dependencies1 = [("B", "A"), ("C", "B"), ("D", "A")]
print("Test Case 1:", task_scheduler(tasks1, dependencies1))  
# Output: A valid order like ['A', 'B', 'C', 'D'] or ['A', 'D', 'B', 'C']

tasks2 = ["X", "Y", "Z"]
dependencies2 = [("Y", "X"), ("Z", "Y"), ("X", "Z")]
print("Test Case 2:", task_scheduler(tasks2, dependencies2))  
# Output: None (Cycle)

tasks3 = ["P", "Q", "R"]
dependencies3 = []
print("Test Case 3:", task_scheduler(tasks3, dependencies3))  
# Output: Any order, e.g., ['P', 'Q', 'R']

tasks4 = ["compile", "test", "deploy", "build", "package"]
dependencies4 = [
    ("test", "compile"),
    ("deploy", "package"),
    ("package", "build"),
    ("build", "compile")
]
print("Test Case 4:", task_scheduler(tasks4, dependencies4))  
# Output: ['compile', 'test', 'build', 'package', 'deploy'] or another valid order
