import tkinter as tk
from tkinter import Toplevel, scrolledtext
import subprocess
import statistics
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def run_benchmark(command, num_iterations=10):
    results = []

    for _ in range(num_iterations):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, _ = process.communicate()
        if process.returncode == 0:
            try:
                result = float(output)
                results.append(result)
            except ValueError:
                return -1
        else:
            return -1

    if results:
        average_result = statistics.mean(results)
        return average_result
    else:
        return -1


def check_results(command, arg):
    result = run_benchmark([command] + arg)
    if result == -1:
        return "Eroare la rularea benchmark-ului"
    else:
        return result


def message_result(text, command, threads, arg):
    message = f"{text}\n"
    message += f"Timp de executie cu {threads} threaduri este {check_results(command, arg)}\n"
    message += "\n\n"
    return message


def validate_input():
    command = entry_threads.get()
    if command == "graphic":
        validate_input_grafic()
    elif command == "teste_multiple":
        validate_input_numbers()
    else:
        validate_input_number()


def validate_input_numbers():
    selected_benchmarks = [var1.get(), var2.get(), var3.get(), var4.get()]
    threads = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    message = ""
    if any(selected_benchmarks):
        if selected_benchmarks[0]:
            message += "Calcul cu Virgulă Flotantă pentru Cifrele lui Pi\n"
            for t in threads:
                message += message_result("", "./PI", t,
                                          [entry_threads.get()])
                print("Pi ", t)
            message += "\n\n"
        if selected_benchmarks[1]:
            message += "Calculul Numerelor Prime\n"
            for t in threads:
                message += message_result("", "./prime", t, ["100000", entry_threads.get()])
                print("Prim ", t)
            message += "\n\n"
        if selected_benchmarks[2]:
            message += "MergeSort\n"
            for t in threads:
                message += message_result("", "./MergeSort", 2, [entry_threads.get(), "100000"])
                print("MergeSort ", t)
            message += "\n\n"
        if selected_benchmarks[3]:
            message += "Comunicarea între Thread-uri folosind Producer-Consumer\n"
            for t in threads:
                message += message_result("",
                                          "./ProducerConsumer", t,
                                          [str(t / 2), str(t / 2), "10000"])
                print("Comunicare ", t)
            message += "\n\n"
        show_result(message)
    else:
        show_result("Alege cel puțin un benchmark!")


def validate_input_number():
    try:
        num_threads = int(entry_threads.get())
        if num_threads <= 0:
            show_result("Număr de thread-uri invalid!")
        else:
            selected_benchmarks = [var1.get(), var2.get(), var3.get(), var4.get()]
            message = ""
            if any(selected_benchmarks):
                if selected_benchmarks[0]:
                    message += message_result("Calcul cu Virgulă Flotantă pentru Cifrele lui Pi", "./PI", num_threads,
                                              [entry_threads.get()])
                if selected_benchmarks[1]:
                    message += message_result("Calculul Numerelor Prime", "./prime", num_threads,
                                              ["100000", entry_threads.get()])
                if selected_benchmarks[2]:
                    message += message_result("MergeSort", "./MergeSort", num_threads, [entry_threads.get(), "100000"])
                if selected_benchmarks[3]:
                    message += message_result("Comunicarea între Thread-uri folosind Producer-Consumer",
                                              "./ProducerConsumer", num_threads,
                                              [str(num_threads / 2), str(num_threads / 2), "10000"])
                show_result(message)
            else:
                show_result("Alege cel puțin un benchmark!")
    except ValueError:
        show_result("Număr de thread-uri invalid!")


def show_result(message):
    result_window = Toplevel(root)
    result_window.title("Result")
    result_window.configure(bg='#1E1E1E')  # Stil dark theme

    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=50, height=20, bg='#1E1E1E', fg='white')
    result_text.insert(tk.END, message)
    result_text.config(state=tk.DISABLED)
    result_text.pack(expand=True, fill="both")

    ok_button = tk.Button(result_window, text="OK", command=result_window.destroy, bg='#333', fg='white')
    ok_button.pack(pady=10)

    result_window.update()
    result_window_width = result_window.winfo_width() + 20  # Adăugăm o margine pentru aspect estetic
    result_window_height = result_window.winfo_height() + 50
    result_window.geometry(
        f"{result_window_width}x{result_window_height}+{int((root.winfo_screenwidth() - result_window_width) / 2)}+{int((root.winfo_screenheight() - result_window_height) / 2)}")


def validate_input_grafic():
    selected_benchmarks = [var1.get(), var2.get(), var3.get(), var4.get()]
    threads = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    if any(selected_benchmarks):
        if selected_benchmarks[0]:
            result = [(t, check_results("./PI", [str(t)])) for t in threads]
            open_result_window("Calcul cu Virgulă Flotantă pentru Cifrele lui Pi", result)
        if selected_benchmarks[1]:
            result = [(t, check_results("./prime", ["100000", str(t)])) for t in threads]
            open_result_window("Calculul Numerelor Prime", result)
        if selected_benchmarks[2]:
            result = [(t, check_results("./MergeSort", [str(t), "100000"])) for t in threads]
            open_result_window("MergeSort", result)
        if selected_benchmarks[3]:
            result = [(t, check_results("./ProducerConsumer", [str(t)])) for t in [2, 4, 8, 16, 32, 64, 128]]
            open_result_window("Comunicarea între Thread-uri folosind Producer-Consumer", result)
    else:
        show_result("Alege cel puțin un benchmark!")


def open_result_window(benchmark_name, thread_time_list):
    result_window = tk.Toplevel()
    result_window.title(benchmark_name)
    result_window.geometry("600x400")
    result_window.configure(bg='#1E1E1E')

    label = tk.Label(result_window, text=f"Rezultate pentru {benchmark_name}", pady=10, bg='#1E1E1E', fg='white')
    label.pack()

    threads, times = zip(*thread_time_list)

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.plot(threads, times, marker='o', linestyle='-')
    ax.set_xlabel('Number of Threads')
    ax.set_ylabel('Execution Time (s)')
    ax.set_title('Execution Time vs Number of Threads')

    # Embedding the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    ok_button = tk.Button(result_window, text="OK", command=result_window.destroy, bg='#333', fg='white')
    ok_button.pack(pady=10)


root = tk.Tk()
root.title("Program pentru masurarea performantei multi-core")
root.configure(bg='#1E1E1E')

main_window_width = int(root.winfo_screenwidth() / 4)
main_window_height = int(root.winfo_screenheight() / 2)
root.geometry(
    f"{main_window_width}x{main_window_height}+{int((root.winfo_screenwidth() - main_window_width) / 2)}+{int((root.winfo_screenheight() - main_window_height) / 2)}")

var1 = tk.BooleanVar()
var2 = tk.BooleanVar()
var3 = tk.BooleanVar()
var4 = tk.BooleanVar()

default_num_threads = "4"

check_box1 = tk.Checkbutton(root, text="Calcul cu Virgulă Flotantă pentru Cifrele lui Pi", variable=var1, bg='#1E1E1E',
                            fg='white', selectcolor='#1E1E1E')
check_box1.grid(row=0, column=0, pady=10, padx=10, sticky="w")

check_box2 = tk.Checkbutton(root, text="Calculul Numerelor Prime", variable=var2, bg='#1E1E1E', fg='white',
                            selectcolor='#1E1E1E')
check_box2.grid(row=1, column=0, pady=10, padx=10, sticky="w")

check_box3 = tk.Checkbutton(root, text="MergeSort", variable=var3, bg='#1E1E1E', fg='white', selectcolor='#1E1E1E')
check_box3.grid(row=2, column=0, pady=10, padx=10, sticky="w")

check_box4 = tk.Checkbutton(root, text="Comunicarea între Thread-uri folosind Producer-Consumer", variable=var4,
                            bg='#1E1E1E', fg='white', selectcolor='#1E1E1E')
check_box4.grid(row=3, column=0, pady=10, padx=10, sticky="w")

entry_threads = tk.Entry(root, bg='#333', fg='white')
entry_threads.grid(row=4, column=0, pady=10, padx=10, sticky="w")
entry_threads.insert(0, default_num_threads)  # Setare valoare implicită

validate_button = tk.Button(root, text="Ruleaza", command=validate_input, bg='#333', fg='white')
validate_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")

root.mainloop()
