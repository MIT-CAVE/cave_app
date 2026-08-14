# Space Complexity Analysis

Space complexity measures the *extra memory* an algorithm needs beyond the input array:

$\text{Total Space} = \text{Input Space} + \text{Auxiliary Space}$

## Implementation Examples

```python
def sort_with_extra_space(arr):
    # O(n) auxiliary space
    temp = [0] * len(arr)    # Creates new array
    # ...sorting logic...
    return temp

def sort_in_place(arr):
    # O(1) auxiliary space
    left, right = 0, len(arr) - 1
    while left < right:      # Only uses a few variables
        arr[left], arr[right] = arr[right], arr[left]
```

## Memory Usage Types

1. **Auxiliary Space** ($S_a$): Extra working memory
   - Temporary arrays: $O(n)$
   - Helper variables: $O(1)$

2. **Recursive Stack** ($S_r$): Call stack memory
   ```python
   def recursive_sort(arr, start, end):
       if end - start <= 1: return
       mid = (start + end) // 2
       # Stack frames: O(log n) for balanced recursion
       recursive_sort(arr, start, mid)
       recursive_sort(arr, mid, end)
   ```

## Space Complexity Classes

| Complexity | Description | Memory Growth |
|------------|-------------|---------------|
| $O(1)$ | Constant | Fixed size |
| $O(\log n)$ | Logarithmic | $S_r \propto \log n$ |
| $O(n)$ | Linear | $S_a \propto n$ |

Can you identify which algorithm achieves $O(1)$ auxiliary space while maintaining $O(n \log n)$ time complexity?

*Hint: Look for an algorithm that:*
- Modifies array in-place: $S_a = O(1)$
- Uses minimal stack space
- Has efficient runtime: $T(n) = O(n \log n)$