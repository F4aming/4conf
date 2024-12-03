import csv
import struct
import sys

MEMORY_SIZE = 1024
memory = [0] * MEMORY_SIZE

def load_binary(filename):
    with open(filename, 'rb') as file:
        return file.read()

def execute(binary_data, mem_range, output_file):
    pc = 0
    while pc < len(binary_data):
        opcode = binary_data[pc]
        print(f"PC: {pc}, Opcode: {opcode}")  # Отладочное сообщение

        # Обработка команды LOAD_CONST (6 байт)
        if opcode == 201:  
            if len(binary_data) < pc + 6:
                print(f"Ошибка: недостаточно данных для команды LOAD_CONST по адресу {pc}")
                break
            try:
                addr, const = struct.unpack('<HI', binary_data[pc+1:pc+6])
                memory[addr] = const
                print(f"LOAD_CONST: memory[{addr}] = {const}")
            except struct.error as e:
                print(f"Ошибка распаковки для LOAD_CONST по адресу {pc}: {e}")
                break
            pc += 6

        # Обработка команды LOAD_MEM (5 байт)
        elif opcode == 57:  
            if len(binary_data) < pc + 5:
                print(f"Ошибка: недостаточно данных для команды LOAD_MEM по адресу {pc}")
                break
            try:
                addr1, addr2 = struct.unpack('<HH', binary_data[pc+1:pc+5])
                memory[addr1] = memory[memory[addr2]]
                print(f"LOAD_MEM: memory[{addr1}] = memory[memory[{addr2}]] -> {memory[addr1]}")
            except struct.error as e:
                print(f"Ошибка распаковки для LOAD_MEM по адресу {pc}: {e}")
                break
            pc += 5

        # Обработка команды STORE_MEM (5 байт)
        elif opcode == 27:  
            if len(binary_data) < pc + 5:
                print(f"Ошибка: недостаточно данных для команды STORE_MEM по адресу {pc}")
                break
            try:
                addr1, addr2 = struct.unpack('<HH', binary_data[pc+1:pc+5])
                memory[memory[addr1]] = memory[addr2]
                print(f"STORE_MEM: memory[memory[{addr1}]] = memory[{addr2}] -> {memory[memory[addr1]]}")
            except struct.error as e:
                print(f"Ошибка распаковки для STORE_MEM по адресу {pc}: {e}")
                break
            pc += 5

        # Обработка команды SHR (7 байт)
        elif opcode == 113:  
            if len(binary_data) < pc + 7:
                print(f"Ошибка: недостаточно данных для команды SHR по адресу {pc}")
                break
            try:
                addr1, addr2, addr3 = struct.unpack('<HHH', binary_data[pc+1:pc+7])
                if memory[addr3] != 0:
                    memory[addr1] = memory[addr2] >> memory[addr3]
                else:
                    memory[addr1] = 0  # Предотвращение деления на 0
                print(f"SHR: memory[{addr1}] = memory[{addr2}] >> memory[{addr3}] -> {memory[addr1]}")
            except struct.error as e:
                print(f"Ошибка распаковки для SHR по адресу {pc}: {e}")
                break
            pc += 7
        
        else:
            print(f"Неизвестная команда {opcode} по адресу {pc}")
            break
    
    # Запись диапазона памяти в CSV файл
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address', 'Value'])
        for i in range(mem_range[0], mem_range[1]):
            writer.writerow([i, memory[i]])

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Использование: python interpreter.py <input.bin> <output.csv> <mem_start> <mem_end>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mem_start = int(sys.argv[3])
    mem_end = int(sys.argv[4])
    
    binary_data = load_binary(input_file)
    print(f"Размер бинарного файла: {len(binary_data)} байт")  # Отладочное сообщение
    execute(binary_data, (mem_start, mem_end), output_file)
    print("Выполнение завершено. Проверьте файл:", output_file)
