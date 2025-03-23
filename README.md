### **1. Bubble Sort**
```java
void bubbleSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++)
        for (int j = 0; j < n - i - 1; j++)
            if (arr[j] > arr[j + 1]) 
                swap(arr, j, j + 1);
}
```

---

### **2. Selection Sort**
```java
void selectionSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++)
            if (arr[j] < arr[minIdx]) minIdx = j;
        swap(arr, i, minIdx);
    }
}
```

---

### **3. Insertion Sort**
```java
void insertionSort(int[] arr) {
    int n = arr.length;
    for (int i = 1; i < n; i++) {
        int key = arr[i], j = i - 1;
        while (j >= 0 && arr[j] > key) arr[j + 1] = arr[j--];
        arr[j + 1] = key;
    }
}
```

---

### **4. Merge Sort**
```java
void mergeSort(int[] arr, int l, int r) {
    if (l < r) {
        int m = (l + r) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
```

---

### **5. Quick Sort**
```java
void quickSort(int[] arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
```

---

### **6. Heap Sort**
```java
void heapSort(int[] arr) {
    int n = arr.length;
    for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(arr, 0, i);
        heapify(arr, i, 0);
    }
}
```

---

### **7. Counting Sort**
```java
void countingSort(int[] arr) {
    int max = Arrays.stream(arr).max().getAsInt();
    int[] count = new int[max + 1], output = new int[arr.length];
    for (int num : arr) count[num]++;
    for (int i = 1; i <= max; i++) count[i] += count[i - 1];
    for (int i = arr.length - 1; i >= 0; i--) output[--count[arr[i]]] = arr[i];
    System.arraycopy(output, 0, arr, 0, arr.length);
}
```

---

### **8. Radix Sort**
```java
void radixSort(int[] arr) {
    int max = Arrays.stream(arr).max().getAsInt();
    for (int exp = 1; max / exp > 0; exp *= 10) countSort(arr, exp);
}
```

---

### **9. Shell Sort**
```java
void shellSort(int[] arr) {
    int n = arr.length;
    for (int gap = n / 2; gap > 0; gap /= 2)
        for (int i = gap; i < n; i++) {
            int temp = arr[i], j = i;
            while (j >= gap && arr[j - gap] > temp) arr[j] = arr[j - gap], j -= gap;
            arr[j] = temp;
        }
}
```

---

### **10. Bucket Sort**
```java
void bucketSort(float[] arr) {
    List<Float>[] buckets = new List[arr.length];
    for (int i = 0; i < arr.length; i++) buckets[i] = new ArrayList<>();
    for (float num : arr) buckets[(int) (num * arr.length)].add(num);
    for (List<Float> bucket : buckets) Collections.sort(bucket);
    int index = 0;
    for (List<Float> bucket : buckets) for (float num : bucket) arr[index++] = num;
}
```

---

### **Helper Function for Swapping**
```java
void swap(int[] arr, int i, int j) {
    int temp = arr[i]; arr[i] = arr[j]; arr[j] = temp;
}
```

## **Comparable and Comparator** 

---

### **1. Using `Comparable` (Default Sorting)**
```java
import java.util.*;

class Student implements Comparable<Student> {
    String name;
    int age;

    Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public int compareTo(Student s) { // Sort by age (default)
        return this.age - s.age;
    }

    public String toString() {
        return name + " (" + age + ")";
    }

    public static void main(String[] args) {
        List<Student> students = Arrays.asList(
            new Student("Alice", 22),
            new Student("Bob", 20),
            new Student("Charlie", 25)
        );

        Collections.sort(students); // Uses compareTo()
        System.out.println(students);
    }
}
```
**Output:**
```
[Bob (20), Alice (22), Charlie (25)]
```
---
### **2. Using `Comparator` (Custom Sorting)**
```java
import java.util.*;

class Student {
    String name;
    int age;

    Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String toString() {
        return name + " (" + age + ")";
    }

    public static void main(String[] args) {
        List<Student> students = Arrays.asList(
            new Student("Alice", 22),
            new Student("Bob", 20),
            new Student("Charlie", 25)
        );

        // Sort by name using Comparator
        students.sort(Comparator.comparing(s -> s.name));
        System.out.println(students);
    }
}
```
**Output:**
```
[Alice (22), Bob (20), Charlie (25)]
```

---



### **Key Differences:**
- `Comparable`: Used when the **class itself** defines the default sorting order (`compareTo` method).
- `Comparator`: Used when you **want multiple sorting criteria** (e.g., sort by name, age, etc.).

# Stack 

```java
import java.util.*;

public class StackExample {
    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();

        // Push elements
        stack.push(10);
        stack.push(20);
        stack.push(30);
        System.out.println("Stack after pushes: " + stack); // [10, 20, 30]

        // Peek top element
        System.out.println("Top element: " + stack.peek()); // 30

        // Pop elements
        System.out.println("Popped: " + stack.pop()); // 30
        System.out.println("Stack after pop: " + stack); // [10, 20]

        // Check if stack is empty
        System.out.println("Is stack empty? " + stack.isEmpty()); // false

        // Search for an element (returns position from top)
        System.out.println("Position of 10: " + stack.search(10)); // 2 (1-based index)
    }
}
```

### **Output:**
```
Stack after pushes: [10, 20, 30]
Top element: 30
Popped: 30
Stack after pop: [10, 20]
Is stack empty? false
Position of 10: 2
```

# **TreeSet Basics in Java** 🌳  

---

### ** Basic Operations with `TreeSet`**
```java
import java.util.*;

public class TreeSetExample {
    public static void main(String[] args) {
        TreeSet<Integer> set = new TreeSet<>();

        // Adding elements
        set.add(30);
        set.add(10);
        set.add(20);
        set.add(40);
        set.add(10); // Duplicate (ignored)

        System.out.println("TreeSet: " + set); // Output: [10, 20, 30, 40] (Sorted)

        // Checking elements
        System.out.println("Contains 20? " + set.contains(20)); // true

        // Removing an element
        set.remove(30);
        System.out.println("After removing 30: " + set); // [10, 20, 40]

        // Getting first and last element
        System.out.println("First: " + set.first()); // 10
        System.out.println("Last: " + set.last()); // 40

        // Getting subset (headSet, tailSet, subSet)
        System.out.println("Elements less than 30: " + set.headSet(30)); // [10, 20]
        System.out.println("Elements greater than/equal to 20: " + set.tailSet(20)); // [20, 40]
    }
}
```

### **Expected Output** of the Given Code:
```
TreeSet: [10, 20, 30, 40]
Contains 20? true
After removing 30: [10, 20, 40]
First: 10
Last: 40
Elements less than 30: [10, 20]
Elements greater than/equal to 20: [20, 40]
```

# **Java `Map` Basics** 🗺️  

A `Map` in Java is a **key-value pair** data structure where:  
✅ Keys are **unique**  
✅ Values can be **duplicate**  
✅ Provides **fast lookup (O(1) for HashMap, O(log n) for TreeMap)**  

---

## **Basic `Map` Operations**
```java
import java.util.*;

public class MapExample {
    public static void main(String[] args) {
        Map<Integer, String> map = new HashMap<>();

        // Adding key-value pairs
        map.put(1, "Apple");
        map.put(2, "Banana");
        map.put(3, "Cherry");

        // Retrieving a value
        System.out.println("Value for key 2: " + map.get(2)); // Banana

        // Checking if key or value exists
        System.out.println("Contains key 3? " + map.containsKey(3)); // true
        System.out.println("Contains value 'Apple'? " + map.containsValue("Apple")); // true

        // Removing a key
        map.remove(1);
        System.out.println("After removing key 1: " + map); // {2=Banana, 3=Cherry}

        // Iterating through keys and values
        for (Map.Entry<Integer, String> entry : map.entrySet()) {
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }
    }
}
```

### **Expected Output:**
```
Value for key 2: Banana
Contains key 3? true
Contains value 'Apple'? true
After removing key 1: {2=Banana, 3=Cherry}
Key: 2, Value: Banana
Key: 3, Value: Cherry
```
