"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.counter = 0
        self.halted = False
        self.pc = 0

        self.instruction_set = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
        }

        self.alu_instructions = {
            0b10100010: self.alu
        }

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        # print(self.pc)
        try:
            with open('examples/' + filename) as f:
                for line in f:
                    x = line.split("#")[0]
                    instruction = x.strip()

                    if instruction != "":
                        # self.ram[address] = '0b' + instruction # CAN'T USE STRINGS
                        # self.ram[address] = bin(int(instruction, 2))  # MANGLES
                        # INTS BUT RUINS PRINT VALUE
                        self.ram[address] = int(instruction, 2)
                        # print(bin(self.ram[address]))
                        address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found!")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
            self.counter += 3
            # print(f'MUL')
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.counter,
            # self.fl,
            # self.ie,
            self.ram_read(self.counter),
            self.ram_read(self.counter + 1),
            self.ram_read(self.counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # print(self.ram)
        # self.counter = 0
        # print(self.counter)
        while not self.halted:

            current_instruction = self.ram_read(self.counter)

            if current_instruction in self.instruction_set:
                # print(bin(current_instruction))
                self.instruction_set[current_instruction]()
                # print(f'instruction')
            elif current_instruction in self.alu_instructions:
                self.alu_instructions[current_instruction]("MUL", self.ram_read(self.counter + 1), self.ram_read(self.counter + 2))
                # print(f'alu')
            else:
                print(f"No {current_instruction} at {self.counter}")
                sys.exit(1)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def HLT(self):
        self.halted = True

    def LDI(self):
        address = self.ram_read(self.counter + 1)
        value = self.ram_read(self.counter + 2)
        # print(value)
        self.register[address] = value
        self.counter += 3

    def PRN(self):
        address = self.ram_read(self.counter + 1)
        value = self.register[address]
        # print(f'printing {value}')
        # print(self.ram)
        print(value)
        self.counter += 2
