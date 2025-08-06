def interval_operations(intervals, operation):
    """
    Args:
        intervals: List of intervals
        operation: 'merge', 'intersect', or 'gaps'
    
    Returns:
        - 'merge': Merged intervals
        - 'intersect': Common intersection of all intervals
        - 'gaps': Gaps between intervals
    """
    
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])

    if operation == 'merge':
        merged = [intervals[0]]
        for current in intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                last[1] = max(last[1], current[1])
            else:
                merged.append(current)
        return merged

    elif operation == 'intersect':
        start = max(interval[0] for interval in intervals)
        end = min(interval[1] for interval in intervals)
        if start <= end:
            return [[start, end]]
        else:
            return []

    elif operation == 'gaps':
        merged = [intervals[0]]
        for current in intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                last[1] = max(last[1], current[1])
            else:
                merged.append(current)
        
        gaps = []
        for i in range(1, len(merged)):
            prev_end = merged[i - 1][1]
            curr_start = merged[i][0]
            if prev_end < curr_start:
                gaps.append([prev_end, curr_start])
        return gaps

    else:
        raise ValueError("Invalid operation. Choose from 'merge', 'intersect', or 'gaps'.")


intervals = [[1,3],[6,9]]
print("Gaps:", interval_operations(intervals, 'gaps'))       
print("Merge:", interval_operations(intervals, 'merge'))    
print("Intersect:", interval_operations(intervals, 'intersect')) 
