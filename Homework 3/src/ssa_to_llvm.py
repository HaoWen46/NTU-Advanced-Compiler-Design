from bril import Program, Const, ValueOperation, EffectOperation, Label

def bril_to_llvm(program: Program) -> str:
    """
    Translate a Bril program in SSA form to LLVM IR.

    Args:
        program (Program): The Bril program represented as a Program object.

    Returns:
        str: The generated LLVM IR code as a string.
    """
    llvm_ir_lines = []
    llvm_type = {None: 'void', 'bool': 'i1', 'int': 'i32'}

    # Join all lines into a single LLVM IR string
    llvm_ir_lines.append('declare i32 @printf(i8*, ...)')
    llvm_ir_lines.append('declare i32 @atoi(i8*)')
    llvm_ir_lines.append('@.str = private unnamed_addr constant [4 x i8] c"%d\n\00", align 1')
    llvm_ir_lines.append('@.trueStr = private unnamed_addr constant [6 x i8] c"true\n\00", align 1')
    llvm_ir_lines.append('@.falseStr = private unnamed_addr constant [7 x i8] c"false\n\00", align 1')

    for func in program.functions:
        if func.name == 'main':
            func.type = 'int'
            llvm_ir_lines.append('define i32 @main(i32 %argc, i8** %argv) {')
            for i, arg in enumerate(func.args, 1):
                llvm_ir_lines.append(f'%arg{i}_ptr = getelementptr inbounds i8*, i8** %argv, i32 {i}')
                llvm_ir_lines.append(f'%arg{i} = load i8*, i8** %arg{i}_ptr')
                llvm_ir_lines.append(f'%{arg["name"]} = call {llvm_type[arg["type"]]} @atoi(i8* %arg{i})')
                llvm_ir_lines.append('br label %__entry__')

        else:
            args = ', '.join([f'{llvm_type[arg["type"]]} %{arg["name"]}' for arg in func.args])
            llvm_ir_lines.append(f'define {llvm_type[func.type]} @{func.name}({args}) {{')
        
        vartype = dict()
        for instr in func.instrs:
            if hasattr(instr, 'dest'):
                vartype[instr.dest] = llvm_type[instr.type]
        
        for instr in func.instrs:
            datatype = llvm_type[instr.type] if hasattr(instr, 'type') else 'void'
            if instr.op == 'call':
                dest = f'%{instr.dest} = ' if hasattr(instr, 'dest') else ''
                args = ', '.join([f'{vartype[arg]} %{arg}' for arg in instr.args])
                llvm_ir_lines.append(f'{dest}call {datatype} @{instr.funcs[0]}({args})')
            elif instr.op == 'phi':
                args = ', '.join([f'[%{instr.args[i]}, %{instr.labels[i]}]' for i in range(len(instr.args))])
                llvm_ir_lines.append(f'%{instr.dest} = phi {datatype} {args}')
            elif instr.op == 'id':
                llvm_ir_lines.append(f'%{instr.dest} = add {datatype} %{instr.args[0]}, 0')
            elif instr.op == 'ret':
                if func.name == 'main':
                    llvm_ir_lines.append('ret i32 0')
                else:
                    llvm_ir_lines.append(f'ret {llvm_type[func.type]} %{instr.args[0]}' if func.type else 'ret void')
            elif instr.op == 'print':
                if vartype[instr.args[0]] == 'i32':
                    llvm_ir_lines.append(f'call i32 @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i32 0, i32 0), i32 %{instr.args[0]})')
                elif vartype[instr.args[0]] == 'i1':
                    llvm_ir_lines.append('%true_ptr = getelementptr inbounds [6 x i8], [6 x i8]* @.trueStr, i32 0, i32 0')
                    llvm_ir_lines.append('%false_ptr = getelementptr inbounds [7 x i8], [7 x i8]* @.falseStr, i32 0, i32 0')
                    llvm_ir_lines.append(f'%str_ptr = select i1 %{instr.args[0]}, i8* %true_ptr, i8* %false_ptr')
                    llvm_ir_lines.append('call i32 @printf(i8* %str_ptr)')
            elif isinstance(instr, Label):
                llvm_ir_lines.append(f'{instr.label}:')
            elif isinstance(instr, Const):
                llvm_ir_lines.append(f'%{instr.dest} = add {datatype} {int(instr.value)}, 0')
            elif isinstance(instr, ValueOperation):
                op = instr.op if instr.op != 'div' else 'udiv'
                if op in ['lt', 'gt', 'le', 'ge']:
                    op = 'icmp u' + op
                if op in ['eq', 'ne']:
                    op = 'icmp ' + op
                args = ', '.join([f'%{arg}' for arg in instr.args])
                llvm_ir_lines.append(f'%{instr.dest} = {op} i32 {args}')
            elif isinstance(instr, EffectOperation):
                labels = f'{vartype[instr.args[0]]} %{instr.args[0]}, ' if instr.args else ''
                labels += ', '.join([f'label %{label}' for label in instr.labels])
                llvm_ir_lines.append(f'br {labels}')

        llvm_ir_lines.append('}\n')
    
    #llvm_ir_lines.append('declare i32 @printf(i8*, ...)')

    llvm_ir = '\n'.join(llvm_ir_lines)
    return llvm_ir
