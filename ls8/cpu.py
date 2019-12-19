"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8 
        self.sp = 7

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        # program = []

        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                n = line.split('#')
                n2 = n[0].strip()
                
                if n2 == '':
                    continue

                val = int(n2,2)
                self.ram[address] = val
                address +=1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            command = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]
            
            # Ldi
            if command == 0b10000010:
                self.reg[reg_a] = reg_b
                self.pc += 3

            # mul
            if command == 0b10100010:
                self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
                self.pc += 3

            # prn
            if command == 0b01000111:
                print(self.reg[reg_a])
                self.pc += 2

            # push
            if command == 0b01000101:
                self.reg[self.sp] -= 1

                reg_a = self.ram[self.pc + 1]
                value = self.reg[reg_a]
                self.ram[self.reg[self.sp]] = value

                self.pc += 2

            # pop
            if command == 0b01000110:
                reg_a = self.ram[self.pc + 1]
                value = self.ram[self.reg[self.sp]]
                self.reg[reg_a] = value

                self.reg[self.sp] += 1

                self.pc += 2

            # call
            if command == 0b01010000:
                return_address = self.pc + 2
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_address

                reg_num = self.ram[self.pc + 1]
                sub_address = self.reg[reg_num]
                self.pc = sub_address

            # ret
            if command == 0b00010001:
                return_address = self.ram[self.reg[self.sp]]
                self.reg[self.sp] +=1

                self.pc = return_address

            # add
            if command == 0b10100000:
                self.reg[reg_a] += self.reg[reg_b]
                self.pc +=3

            # hlt
            if command == 0b00000001:
                running = False

            else:
                print(f'error at{self.pc}')