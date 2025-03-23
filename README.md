
---

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
