from typing import Dict, Set
from cfg import CFG, BasicBlock

class DominatorTree:
    def __init__(self, cfg: CFG):
        self.cfg = cfg
        self.dom: Dict[BasicBlock, Set[BasicBlock]] = {}
        self.idom: Dict[BasicBlock, BasicBlock] = {}
        self.dom_frontiers: Dict[BasicBlock, Set[BasicBlock]] = {}
        self.compute_dominators()
        self.compute_dominance_frontiers()

    def compute_dominators(self):
        """
        Computes the dominators for each basic block.
        """
        # TODO: Implement the iterative algorithm to compute dominators
        blocks = [self.cfg.entry_block] + list(self.cfg.blocks.values())
        self.dom = {block: set(blocks) for block in blocks}
        self.dom[self.cfg.entry_block] = {self.cfg.entry_block}

        changed = True
        while changed:
            changed = False
            for block in blocks[1:]:
                new_dom = set(blocks)
                for pred in block.predecessors:
                    new_dom &= self.dom[pred]
                new_dom |= {block}
                
                if new_dom != self.dom[block]:
                    self.dom[block] = new_dom
                    changed = True


    def compute_idom(self):
        """
        Computes the immediate dominator for each basic block.
        """
        # TODO: Compute immediate dominators based on the dominator sets.
        self.idom = {block: self.cfg.entry_block for block in self.cfg.blocks.values()}
        self.idom[self.cfg.entry_block] = None
        for block in self.cfg.blocks.values():
            for dominator in self.dom[block]:
                if self.dom[block] - {block} == self.dom[dominator]:
                    self.idom[block] = dominator
                    break


    def compute_dominance_frontiers(self):
        """
        Computes the dominance frontiers for each basic block.
        """
        # TODO: Implement dominance frontier computation.
        self.compute_idom()
        blocks = [self.cfg.entry_block] + list(self.cfg.blocks.values())
        self.dom_frontiers = {block: set() for block in blocks}

        for block in blocks:
            if len(block.predecessors) >= 2:
                for pred in block.predecessors:
                    runner = pred
                    while runner != self.idom[block]:
                        self.dom_frontiers[runner] |= {block}
                        runner = self.idom[runner]
