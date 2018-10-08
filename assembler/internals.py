from data import REGISTERS, Opcodes

def str_to_int(s):
    if len(s) == 3 and s.startswith("'") and s.endswith("'"):
        return ord(s[1])
    elif s.startswith("0x"):
        return int(s, 16)
    else:
        return int(s, 10)

def register_from_name(s):
    s = s.lower()
    if s not in REGISTERS:
        raise ValueError("Invalid register '{}'".format(s))
    return REGISTERS[s]

def singleop(bytecode, params, opcode):
    if params:
        raise ValueError("Operation '{}' expects 0 arguments, got {}".format(opcode, len(params)))
    bytecode.append(opcode)

def unop(bytecode, params, opcode):
    if len(params) != 1:
        raise ValueError("Operation '{}' expects 1 argument, got {}".format(opcode, len(params)))
    reg = register_from_name(params[0])
    bytecode.append(opcode)
    bytecode.append(reg)

def unop_c(bytecode, params, opcode, nbytes):
    if len(params) != 1:
        raise ValueError("Operation '{}' expects 1 argument, got {}".format(opcode, len(params)))
    val = str_to_int(params[0])
    bytecode.append(opcode)
    bytecode.extend(val.to_bytes(nbytes, 'little', signed=True))

def binop(bytecode, params, opcode):
    if len(params) != 2:
        raise ValueError("Operation '{}' expects 2 arguments, got {}".format(opcode, len(params)))
    reg1 = register_from_name(params[0])
    reg2 = register_from_name(params[1])
    bytecode.append(opcode)
    bytecode.append(reg1)
    bytecode.append(reg2)

def binop_rc(bytecode, params, opcode, nbytes):
    if len(params) != 2:
        raise ValueError("Operation '{}' expects 2 arguments, got {}".format(opcode, len(params)))
    reg = register_from_name(params[0])
    val = str_to_int(params[1])
    bytecode.append(opcode)
    bytecode.append(reg)
    bytecode.extend(val.to_bytes(nbytes, 'little', signed=True))

def binop_cr(bytecode, params, opcode, nbytes):
    if len(params) != 2:
        raise ValueError("Operation '{}' expects 2 arguments, got {}".format(opcode, len(params)))
    val = str_to_int(params[0])
    reg = register_from_name(params[1])
    bytecode.append(opcode)
    bytecode.extend(val.to_bytes(nbytes, 'little', signed=True))
    bytecode.append(reg)

def binop_cc(bytecode, params, opcode, nbytes1, nbytes2):
    if len(params) != 2:
        raise ValueError("Operation '{}' expects 2 arguments, got {}".format(opcode, len(params)))
    val1 = str_to_int(params[0])
    val2 = str_to_int(params[1])
    bytecode.append(opcode)
    bytecode.extend(val1.to_bytes(nbytes1, 'little', signed=True))
    bytecode.extend(val2.to_bytes(nbytes2, 'little', signed=True))

def ternop_ccc(bytecode, params, opcode, nbytes1, nbytes2, nbytes3):
    if len(params) != 3:
        raise ValueError("Operation '{}' expects 3 arguments, got {}".format(opcode, len(params)))
    val1 = str_to_int(params[0])
    val2 = str_to_int(params[1])
    val3 = str_to_int(params[3])
    bytecode.append(opcode)
    bytecode.extend(val1.to_bytes(nbytes1, 'little', signed=True))
    bytecode.extend(val2.to_bytes(nbytes2, 'little', signed=True))
    bytecode.extend(val3.to_bytes(nbytes3, 'little', signed=True))

def process_instruction(bytecode, line):
    opcode, sep, params = line.partition(" ")
    opcode = opcode.lower()

    if sep == " ":
        params = [p.lstrip().rstrip() for p in params.split(",")]
    else:
        params = []

    if opcode == "nop" and params == []:
        singleop(bytecode, params, Opcodes.NOP)
    elif opcode == "lcons":
        binop_rc(bytecode, params, Opcodes.LCONS, 4)
    elif opcode == "lconsw":
        binop_rc(bytecode, params, Opcodes.LCONSW, 2)
    elif opcode == "lconsb":
        binop_rc(bytecode, params, Opcodes.LCONSB, 1)
    elif opcode == "mov":
        binop(bytecode, params, Opcodes.MOV)
    elif opcode == "push":
        unop(bytecode, params, Opcodes.PUSH)
    elif opcode == "pop":
        unop(bytecode, params, Opcodes.POP)
    elif opcode == "pop2":
        binop(bytecode, params, Opcodes.POP2)
    elif opcode == "dup":
        singleop(bytecode, params, Opcodes.DUP)
    elif opcode == "stor":
        binop_cr(bytecode, params, Opcodes.STOR, 2)
    elif opcode == "storw":
        binop_cr(bytecode, params, Opcodes.STORW, 2)
    elif opcode == "storb":
        binop_cr(bytecode, params, Opcodes.STORB, 2)
    elif opcode == "load":
        binop_rc(bytecode, params, Opcodes.LOAD, 2)
    elif opcode == "loadw":
        binop_rc(bytecode, params, Opcodes.LOADW, 2)
    elif opcode == "loadb":
        binop_rc(bytecode, params, Opcodes.LOADB, 2)
    elif opcode == "memcpy":
        ternop_ccc(bytecode, params, Opcodes.MEMCPY, 2, 2, 2)
    elif opcode == "incr":
        unop(bytecode, params, Opcodes.INCR)
    elif opcode == "incrf":
        unop(bytecode, params, Opcodes.INCRF)
    elif opcode == "decr":
        unop(bytecode, params, Opcodes.DECR)
    elif opcode == "decrf":
        unop(bytecode, params, Opcodes.DECRF)
    elif opcode == "add":
        binop(bytecode, params, Opcodes.ADD)
    elif opcode == "addf":
        binop(bytecode, params, Opcodes.ADDF)
    elif opcode == "sub":
        binop(bytecode, params, Opcodes.SUB)
    elif opcode == "subf":
        binop(bytecode, params, Opcodes.SUBF)
    elif opcode == "mult":
        binop(bytecode, params, Opcodes.MULT)
    elif opcode == "multf":
        binop(bytecode, params, Opcodes.MULTF)
    elif opcode == "div":
        binop(bytecode, params, Opcodes.DIV)
    elif opcode == "divf":
        binop(bytecode, params, Opcodes.DIVF)
    elif opcode == "mod":
        binop(bytecode, params, Opcodes.MOD)
    elif opcode == "and":
        binop(bytecode, params, Opcodes.AND)
    elif opcode == "or":
        binop(bytecode, params, Opcodes.OR)
    elif opcode == "xor":
        binop(bytecode, params, Opcodes.XOR)
    elif opcode == "not":
        unop(bytecode, params, Opcodes.NOT)
    elif opcode == "i2f":
        unop(bytecode, params, Opcodes.I2F)
    elif opcode == "f2i":
        unop(bytecode, params, Opcodes.F2I)
    elif opcode == "jmp":
        unop_c(bytecode, params, Opcodes.JMP, 2)
    elif opcode == "jr":
        unop(bytecode, params, Opcodes.JR)
    elif opcode == "jz":
        binop_rc(bytecode, params, Opcodes.JZ, 2)
    elif opcode == "jnz":
        binop_rc(bytecode, params, Opcodes.JNZ, 2)
    elif opcode == "jgz":
        binop_rc(bytecode, params, Opcodes.JGZ, 2)
    elif opcode == "jlz":
        binop_rc(bytecode, params, Opcodes.JLZ, 2)
    elif opcode == "je":
        binop_rc(bytecode, params, Opcodes.JE, 2)
    elif opcode == "jne":
        binop_rc(bytecode, params, Opcodes.JNE, 2)
    elif opcode == "jg":
        binop_rc(bytecode, params, Opcodes.JG, 2)
    elif opcode == "jge":
        binop_rc(bytecode, params, Opcodes.JGE, 2)
    elif opcode == "jl":
        binop_rc(bytecode, params, Opcodes.JL, 2)
    elif opcode == "jle":
        binop_rc(bytecode, params, Opcodes.JLE, 2)
    elif opcode == "print":
        unop(bytecode, params, Opcodes.PRINT)
    elif opcode == "printi":
        unop(bytecode, params, Opcodes.PRINTI)
    elif opcode == "printf":
        unop(bytecode, params, Opcodes.PRINTF)
    elif opcode == "println":
        singleop(bytecode, params, Opcodes.PRINTLN)
    elif opcode == "i2s":
        binop_cr(bytecode, params, Opcodes.I2S, 2)
    elif opcode == "s2i":
        binop_rc(bytecode, params, Opcodes.S2I, 2)
    elif opcode == "a_dr":
        binop_rc(bytecode, params, Opcodes.A_DR, 1)
    elif opcode == "a_ar":
        binop_rc(bytecode, params, Opcodes.A_AR, 1)
    elif opcode == "a_dw":
        binop_cc(bytecode, params, Opcodes.A_DW, 1, 1)
    elif opcode == "a_aw":
        binop_cc(bytecode, params, Opcodes.A_AW, 1, 2)
    elif opcode == "a_dwr":
        binop_cr(bytecode, params, Opcodes.A_DWR, 1)
    elif opcode == "a_awr":
        binop_cr(bytecode, params, Opcodes.A_AWR, 1)
    elif opcode == "a_pm":
        binop_cc(bytecode, params, Opcodes.A_PM, 1, 1)
    elif opcode == "halt" and params == []:
        singleop(bytecode, params, Opcodes.HALT)
    else:
        raise ValueError("Unknown opcode")

    return bytecode
