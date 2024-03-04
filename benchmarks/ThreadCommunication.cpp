#include <stdio.h>
#include <windows.h>
#include <time.h>

#define BUFFER_SIZE 10
#define THREADS_SIZE 1024

int buffer[BUFFER_SIZE];
int count = 0;
CRITICAL_SECTION cs;
CONDITION_VARIABLE cond_producer, cond_consumer;

DWORD WINAPI producer(LPVOID param) {
    int num_items = (int)param;
    for (int i = 0; i < num_items; ++i) {
        EnterCriticalSection(&cs);

        while (count == BUFFER_SIZE) {
            SleepConditionVariableCS(&cond_producer, &cs, INFINITE);
        }
        buffer[count++] = i;
        // printf("Producator: %d\n", i);
        WakeConditionVariable(&cond_consumer);
        LeaveCriticalSection(&cs);
    }
    return 0;
}

DWORD WINAPI consumer(LPVOID param) {
    int num_items = (int)param;
    for (int i = 0; i < num_items; ++i) {
        EnterCriticalSection(&cs);
        while (count == 0) {
            SleepConditionVariableCS(&cond_consumer, &cs, INFINITE);
        }
        int item = buffer[--count];
        // printf("Consumator: %d\n", item);
        WakeConditionVariable(&cond_producer);
        LeaveCriticalSection(&cs);
    }
    return 0;
}
int main(int argc, char* argv[]) {
    int nr_threads = 64;
    int num_producers = nr_threads / 2;
    int num_consumers = nr_threads / 2;
    int num_items = 100000;
    if (argc == 4) {
        num_producers = atoi(argv[1]);
        num_consumers = atoi(argv[2]);
        num_items = atoi(argv[3]);
    }

    InitializeCriticalSection(&cs);
    InitializeConditionVariable(&cond_producer);
    InitializeConditionVariable(&cond_consumer);

    HANDLE producer_threads[THREADS_SIZE];
    HANDLE consumer_threads[THREADS_SIZE];

    LARGE_INTEGER start_time, end_time, frequency;
    double execution_time;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start_time);

    for (int i = 0; i < num_producers; ++i) {
        producer_threads[i] = CreateThread(NULL, 0, producer, (LPVOID)num_items, 0, NULL);
    }

    for (int i = 0; i < num_consumers; ++i) {
        consumer_threads[i] = CreateThread(NULL, 0, consumer, (LPVOID)num_items, 0, NULL);
    }

    WaitForMultipleObjects(num_producers, producer_threads, TRUE, INFINITE);
    WaitForMultipleObjects(num_consumers, consumer_threads, TRUE, INFINITE);

    QueryPerformanceCounter(&end_time);
    execution_time = (double)(end_time.QuadPart - start_time.QuadPart) / frequency.QuadPart;
    printf("%f", execution_time);

    DeleteCriticalSection(&cs);

    return 0;
}
