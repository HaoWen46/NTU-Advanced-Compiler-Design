from typing import Dict, List, Set
from bril import Function, Instruction, ValueOperation, Label, Const
from cfg import CFG, BasicBlock
from dominance import DominatorTree

def construct_ssa(function: Function):
    """
    Transforms the function into SSA form.
    """
    cfg = CFG(function)
    dom_tree = DominatorTree(cfg)

    # Step 1: Variable Definition Analysis
    def_blocks = collect_definitions(cfg)

    # Step 2: Insert φ-Functions
    insert_phi_functions(cfg, dom_tree, def_blocks)

    # Step 3: Rename Variables
    rename_variables(cfg, dom_tree)

    # After transformation, update the function's instructions
    function.instrs = reconstruct_instructions(cfg)

def collect_definitions(cfg: CFG) -> Dict[str, Set[BasicBlock]]:
    """
    Collects the set of basic blocks in which each variable is defined.
    """
    # TODO: Implement variable definition collection
    def_blocks: Dict[str, Set[BasicBlock]] = dict()
    blocks = [cfg.entry_block] + list(cfg.blocks.values())
    for block in blocks:
        for instr in block.instructions:
            if hasattr(instr, 'dest'):
                if instr.dest not in def_blocks:
                    def_blocks[instr.dest] = set()
                def_blocks[instr.dest] |= {block}

    return def_blocks

def insert_phi_functions(cfg: CFG, dom_tree: DominatorTree, def_blocks: Dict[str, Set[BasicBlock]]):
    """
    Inserts φ-functions into the basic blocks.
    """
    # TODO: Implement φ-function insertion using dominance frontiers
    datatype = dict()
    global_names = set()
    blocks = [cfg.entry_block] + list(cfg.blocks.values())
    #func_args = {arg['name'] for arg in cfg.function.args}

    for block in blocks:
        varkill = set()
        for instr in block.instructions:
            if hasattr(instr, 'args'):
                for src in instr.args:
                    if src not in varkill:
                        global_names |= {src}
            if hasattr(instr, 'dest'):
                datatype[instr.dest] = instr.type
                varkill |= {instr.dest}

    phi: Dict[str, Set[str]] = {block.label: set() for block in blocks}
    for name in global_names:
        if name not in def_blocks:
            continue

        worklist = def_blocks[name]
        while worklist:
            for block in worklist.copy():
                worklist -= {block}
                for df in dom_tree.dom_frontiers[block]:
                    if name not in phi[df.label]:
                        phi[df.label] |= {name}
                        worklist |= {df}
    
    for label, names in phi.items():
        phi_functions = []
        for name in names:
            instr = {'op': 'phi', 'dest': name, 'type': datatype[name], 'arg': []}
            phi_functions.append(ValueOperation(instr))

        if label not in cfg.blocks:
            cfg.entry_block.instructions[:0] = phi_functions
        else:
            cfg.blocks[label].instructions[:0] = phi_functions
    
    initialize = []
    for arg in cfg.function.args:
        global_names -= {arg['name']}
        initialize.append(ValueOperation({'op': 'id', 'dest': arg['name'], 'type': arg['type'], 'args': [arg['name']], 'funcs': [], 'labels': []}))

    initialize += [Const({'op': 'const', 'dest': name, 'type': datatype[name], 'value': 0}) for name in global_names]
    cfg.entry_block.instructions[:0] = initialize


def rename_variables(cfg: CFG, dom_tree: DominatorTree):
    """
    Renames variables to ensure each assignment is unique.
    """
    # TODO: Implement variable renaming
    blocks = [cfg.entry_block] + list(cfg.blocks.values())
    tree: Dict[BasicBlock, List[BasicBlock]] = {block: [] for block in blocks}

    global_names = set()
    for block in blocks:
        varkill = set()
        for instr in block.instructions:
            if instr.op == 'phi':
                continue

            if hasattr(instr, 'args'):
                for src in instr.args:
                    if src not in varkill:
                        global_names |= {src}
            if hasattr(instr, 'dest'):
                varkill |= {instr.dest}

        if dom_tree.idom[block] != None:
            tree[dom_tree.idom[block]].append(block)

    counter: Dict[str, int] = {name: 0 for name in global_names}
    stack: Dict[str, List[str]] = {name: [] for name in global_names}

    def newName(name: str) -> str:
        index = counter[name]
        counter[name] += 1
        stack[name].append('__' + str(index))
        return name + stack[name][-1]
    
    def rename(block: BasicBlock):
        for instr in block.instructions:
            if instr.op == 'phi':
                instr.dest = newName(instr.dest)

        for instr in block.instructions:
            if instr.op != 'phi':
                if hasattr(instr, 'args'):
                    for i in range(len(instr.args)):
                        if instr.args[i] in global_names and stack[instr.args[i]]:
                            instr.args[i] += stack[instr.args[i]][-1]
                if hasattr(instr, 'dest') and instr.dest in global_names:
                    instr.dest = newName(instr.dest)

        for succ in block.successors:
            for instr in succ.instructions:
                if instr.op == 'phi':
                    varname = instr.dest.rsplit('__', 1)[0]
                    if stack[varname]:
                        varname += stack[varname][-1]
                        instr.args.append(varname)
                        instr.labels.append(block.label)
        
        for succ in tree[block]:
            rename(succ)

        for instr in block.instructions:
            if hasattr(instr, 'dest') and '__' in instr.dest:
                stack[instr.dest.rsplit('__', 1)[0]].pop()

    rename(cfg.entry_block)

    for block in blocks:
        counter = dict()
        for instr in block.instructions:
            if hasattr(instr, 'args'):
                for i in range(len(instr.args)):
                    if instr.args[i] in counter:
                        instr.args[i] += '__' + str(counter[instr.args[i]])
            if hasattr(instr, 'dest'):
                varname = instr.dest.rsplit('__', 1)[0]
                if varname not in global_names:
                    if instr.dest in counter:
                        counter[instr.dest] += 1
                    else:
                        counter[instr.dest] = 0
                    instr.dest += '__' + str(counter[instr.dest])

def reconstruct_instructions(cfg: CFG) -> List[Instruction]:
    """
    Reconstructs the instruction list from the CFG after SSA transformation.
    """
    # TODO: Implement instruction reconstruction
    instructions: List[Instruction] = []

    for block in [cfg.entry_block] + list(cfg.blocks.values()):
        if block.label != None:
            instructions.append(Label({'op': None, 'label': block.label}))
        instructions += block.instructions

    return instructions


