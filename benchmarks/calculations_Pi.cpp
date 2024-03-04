#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <math.h>
#include <time.h>
#define TOTAL_ITERATIONS  100000000

long double pi = 0.0;
CRITICAL_SECTION cs;
long num_threads = 32;

DWORD WINAPI calculate_pi(LPVOID param) {
    long thread_id = (long)param;

    long iterations_per_thread = TOTAL_ITERATIONS / num_threads;
    long start_iteration = thread_id * iterations_per_thread;
    long end_iteration = start_iteration + iterations_per_thread;

    long double thread_sum = 0.0;

    for (long i = start_iteration; i < end_iteration; ++i) {
        if (i % 2 == 0) {
            thread_sum += 1.0 / (2.0 * i + 1);
        }
        else {
            thread_sum -= 1.0 / (2.0 * i + 1);
        }
    }

    EnterCriticalSection(&cs);
    pi += thread_sum;
    LeaveCriticalSection(&cs);

    return 0;
}

int main(int argc, char* argv[]) {
    if (argc == 2) {
        num_threads = atol(argv[1]);
    }
    HANDLE* threads = (HANDLE*)malloc(num_threads * sizeof(HANDLE));

    if (threads == NULL) {
        fprintf(stderr, "Error allocating memory for threads\n");
        return 2;
    }

    InitializeCriticalSection(&cs);

    LARGE_INTEGER start_time, end_time, frequency;
    double execution_time;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start_time);

    for (long i = 0; i < num_threads; ++i) {
        threads[i] = CreateThread(NULL, 1024 * 1024, calculate_pi, (LPVOID)i, 0, NULL);
        if (threads[i] == NULL) {
            fprintf(stderr, "Error creating thread %ld\n", i);
            return 3;
        }
    }

    WaitForMultipleObjects(num_threads, threads, TRUE, INFINITE);

    for (long i = 0; i < num_threads; ++i) {
        CloseHandle(threads[i]);
    }

    QueryPerformanceCounter(&end_time);
    execution_time = (double)(end_time.QuadPart - start_time.QuadPart) / frequency.QuadPart;
    printf("%f", execution_time);

    free(threads);

    pi *= 4;

    //printf("Pi cu %ld iteratii si %ld thread-uri: %f\n", num_threads * TOTAL_ITERATIONS, num_threads, pi);
    //long double real_pi = 3.14159265358979323846;
    //long double difference = fabs(real_pi - pi);
    //printf("Eroare este: %.15Lf\n", difference);

    DeleteCriticalSection(&cs);

    return 0;
}
