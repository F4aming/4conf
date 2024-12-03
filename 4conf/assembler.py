import csv
import struct
import sys

def assemble(input_file, output_file, log_file):
    instructions = {
        'LOAD_CONST': 201,
        'LOAD_MEM': 57,
        'STORE_MEM': 27,
        'SHR': 113
    }
    
    binary_output = bytearray()
    log_data = []

    try:
        # Чтение исходного ассемблерного файла
        with open(input_file, 'r') as infile:
            for line_number, line in enumerate(infile, start=1):
                parts = line.strip().split()
                
                # Пропускаем пустые строки и комментарии
                if not parts or parts[0].startswith('#'):
                    continue  

                command = parts[0]

                # Обработка различных команд
                if command == 'LOAD_CONST':
                    if len(parts) != 3:
                        print(f"Ошибка в строке {line_number}: неправильное количество аргументов")
                        continue
                    opcode = instructions[command]
                    addr = int(parts[1])
                    const = int(parts[2])
                    binary_output += struct.pack('<BHI', opcode, addr, const)
                    log_data.append([command, addr, const, ''])

                elif command == 'LOAD_MEM':
                    if len(parts) != 3:
                        print(f"Ошибка в строке {line_number}: неправильное количество аргументов")
                        continue
                    opcode = instructions[command]
                    addr1 = int(parts[1])
                    addr2 = int(parts[2])
                    binary_output += struct.pack('<BHH', opcode, addr1, addr2)
                    log_data.append([command, addr1, addr2, ''])
                
                elif command == 'STORE_MEM':
                    if len(parts) != 3:
                        print(f"Ошибка в строке {line_number}: неправильное количество аргументов")
                        continue
                    opcode = instructions[command]
                    addr1 = int(parts[1])
                    addr2 = int(parts[2])
                    binary_output += struct.pack('<BHH', opcode, addr1, addr2)
                    log_data.append([command, addr1, addr2, ''])
                
                elif command == 'SHR':
                    if len(parts) != 4:
                        print(f"Ошибка в строке {line_number}: неправильное количество аргументов")
                        continue
                    opcode = instructions[command]
                    addr1 = int(parts[1])
                    addr2 = int(parts[2])
                    addr3 = int(parts[3])
                    binary_output += struct.pack('<BHHH', opcode, addr1, addr2, addr3)
                    log_data.append([command, addr1, addr2, addr3])
                
                else:
                    print(f"Ошибка в строке {line_number}: неизвестная команда '{command}'")
        
        # Сохранение бинарного файла
        with open(output_file, 'wb') as outfile:
            outfile.write(binary_output)
        
        # Сохранение лога в CSV
        with open(log_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Instruction', 'Param1', 'Param2', 'Param3'])
            writer.writerows(log_data)
        
        print("Ассемблирование завершено. Лог сохранен в", log_file)
    
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Использование: python assembler.py <input.asm> <output.bin> <log.csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    
    assemble(input_file, output_file, log_file)
