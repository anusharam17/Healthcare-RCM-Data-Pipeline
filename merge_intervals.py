def merge_intervals(intervals):
    if not intervals:
        return []

    # Step 1: Sort the intervals based on the start time
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]  # Initialize merged list with the first interval

    for current in intervals[1:]:
        prev = merged[-1]  # Get the last interval from the merged list

        # Step 2: Check if the current interval overlaps with the previous one
        if current[0] <= prev[1]:
            # Merge the intervals by extending the end of the previous interval
            prev[1] = max(prev[1], current[1])
        else:
            # No overlap, so add the current interval to the merged list
            merged.append(current)

    return merged


print("\nMerge Intervals Test Cases:")

test1 = [[1,3],[2,6],[8,10],[15,18]]
print("Test 1:", merge_intervals(test1)) 

test2 = [[1,4],[4,5]]
print("Test 2:", merge_intervals(test2))  

test3 = [[1,4],[2,3]]
print("Test 3:", merge_intervals(test3)) 

test4 = [[1,2],[3,4],[5,6]]
print("Test 4:", merge_intervals(test4))  

test5 = [[1,4],[2,5],[3,6]]
print("Test 5:", merge_intervals(test5)) 

test6 = [[6,7],[2,4],[5,9]]
print("Test 6:", merge_intervals(test6)) 

test7 = [[1,4]]
print("Test 7:", merge_intervals(test7))  

test8 = [[2,3],[4,5],[6,7],[8,9],[1,10]]
print("Test 8:", merge_intervals(test8)) 
