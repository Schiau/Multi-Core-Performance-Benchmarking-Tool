#include <iostream>
#include <windows.h>
#include <cstdlib>

using namespace std;

int* a;
int num_threads = 32;
int part = 0;
int arr_size = 100000;

void merge(int low, int mid, int high) {
    int n1 = mid - low + 1;
    int n2 = high - mid;

    int* left = (int*)malloc(n1 * sizeof(int));
    int* right = (int*)malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++)
        left[i] = a[i + low];

    for (int j = 0; j < n2; j++)
        right[j] = a[j + mid + 1];

    int i = 0, j = 0, k = low;

    while (i < n1 && j < n2) {
        if (left[i] <= right[j])
            a[k++] = left[i++];
        else
            a[k++] = right[j++];
    }

    while (i < n1)
        a[k++] = left[i++];

    while (j < n2)
        a[k++] = right[j++];

    free(left);
    free(right);
}

void merge_sort(int low, int high) {
    if (low < high) {
        int mid = low + (high - low) / 2;

        merge_sort(low, mid);
        merge_sort(mid + 1, high);
        merge(low, mid, high);
    }
}

DWORD WINAPI merge_sort_thread(LPVOID arg) {
    int thread_part = part++;
    int low = thread_part * (arr_size / num_threads);
    int high = (thread_part + 1) * (arr_size / num_threads) - 1;
    int mid = low + (high - low) / 2;

    if (low < high) {
        merge_sort(low, mid);
        merge_sort(mid + 1, high);
        merge(low, mid, high);
    }

    return 0;
}

int generateRandomValue(int index) {
    return static_cast<int>(50 + 50 * sin(index));
}

int main(int argc, char* argv[]) {
    if (argc == 3) {
        num_threads = atoi(argv[1]);
        arr_size = atoi(argv[2]);
    }

    a = (int*)malloc(arr_size * sizeof(int));

    for (int i = 0; i < arr_size; i++)
        a[i] = generateRandomValue(i);

    HANDLE* threads = (HANDLE*)malloc(num_threads * sizeof(HANDLE));

    LARGE_INTEGER start_time, end_time, frequency;
    double execution_time;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start_time);

    for (int i = 0; i < num_threads; i++)
        threads[i] = CreateThread(NULL, 0, merge_sort_thread, NULL, 0, NULL);

    WaitForMultipleObjects(num_threads, threads, TRUE, INFINITE);

    for (int i = 0; i < num_threads; i++)
        CloseHandle(threads[i]);

    for (int i = 1; i < num_threads; i += 2)
        merge(0, i * (arr_size / num_threads) - 1, (i + 1) * (arr_size / num_threads) - 1);

    for (int i = 2; i < num_threads; i += 2)
        merge(0, (i + 1) * (arr_size / num_threads) - 1, (i + 2) * (arr_size / num_threads) - 1);

    merge(0, (num_threads - 1) * (arr_size / num_threads), arr_size - 1);

    QueryPerformanceCounter(&end_time);
    execution_time = (double)(end_time.QuadPart - start_time.QuadPart) / frequency.QuadPart;
    printf("%f", execution_time);

    //for (int i = 0; i < arr_size; i++)
    //    cout << a[i] << " ";

    free(threads);
    free(a);

    return 0;
}
