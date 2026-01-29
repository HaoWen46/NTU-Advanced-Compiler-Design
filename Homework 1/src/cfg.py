from typing import Dict, List, Set
from bril import Function, Instruction, EffectOperation

class BasicBlock:
    def __init__(self, label: str):
        self.label = label
        self.instructions: List[Instruction] = []
        self.predecessors: Set['BasicBlock'] = set()
        self.successors: Set['BasicBlock'] = set()

    def __repr__(self):
        return f'BasicBlock({self.label})'

class CFG:
    def __init__(self, function: Function):
        self.function = function
        self.blocks: Dict[str, BasicBlock] = {}
        self.entry_block: BasicBlock = self.construct_cfg()

    def construct_cfg(self) -> BasicBlock:
        """
        Constructs the CFG for the function and returns the entry block.
        """
        # TODO: Implement CFG construction logic
        # Steps:
        # 1. Divide instructions into basic blocks.
        # 2. Establish successor and predecessor relationships.
        # 3. Handle labels and control flow instructions.
        
        entry_block = BasicBlock('__entry__')
        current_block = entry_block

        for instr in self.function.instrs:
            if hasattr(instr, 'label'):
                self.blocks[instr.label] = BasicBlock(instr.label)
                current_block = self.blocks[instr.label]
            else:
                current_block.instructions.append(instr)
        
        prev_instr = None
        current_block = entry_block
        for instr in self.function.instrs:
            if hasattr(instr, 'label'):
                if prev_instr == None or prev_instr.op not in ['br', 'jmp', 'ret']:
                    current_block.successors.add(self.blocks[instr.label])
                    self.blocks[instr.label].predecessors.add(current_block)
                current_block = self.blocks[instr.label]
            elif instr.op in ['br', 'jmp']:
                for label in instr.labels:
                    current_block.successors.add(self.blocks[label])
                    self.blocks[label].predecessors.add(current_block)
            prev_instr = instr
        
        if not entry_block.instructions:
            instr = {'op': 'jmp', 'args': [], 'funcs': [], 'labels': [list(entry_block.successors)[0].label]}
            entry_block.instructions.append(EffectOperation(instr))
        return entry_block


    def get_blocks(self) -> List[BasicBlock]:
        return list(self.blocks.values())
