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
        #self.SP = 0
        self.register[-1] = 0xF4

        self.instruction_set = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b01000110: self.POP,
            0b01000101: self.PUSH
        }

        self.alu_instructions = {
            0b10100010: "MUL"
        }

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        try:
            with open('examples/' + filename) as f:
                for line in f:
                    x = line.split("#")[0]
                    instruction = x.strip()

                    if instruction != "":
                        self.ram[address] = int(instruction, 2)
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
        while not self.halted:

            current_instruction = self.ram_read(self.counter)
            #print(self.instruction_set[current_instruction], self.counter)

            if current_instruction in self.instruction_set:
                self.instruction_set[current_instruction]()
            elif current_instruction in self.alu_instructions:
                self.alu(self.alu_instructions[current_instruction], self.ram_read(
                    self.counter + 1), self.ram_read(self.counter + 2))
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
        self.register[address] = value
        self.counter += 3

    def PRN(self):
        address = self.ram_read(self.counter + 1)
        value = self.register[address]
        print(value)
        self.counter += 2

    def POP(self):
        self.register[self.ram[self.counter + 1]] = self.ram[self.register[-1]]
        self.register[-1] += 1
        self.counter += 2

    def PUSH(self):
        self.register[-1] -= 1
        self.ram[self.register[-1]] = self.register[self.ram[self.counter + 1]]
        self.counter += 2
