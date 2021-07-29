def aight_bit_alignment(num):
    return num + 8 - num % 8

class Block:
    def __init__(self, size, next, prev, free):
        self.size = size
        self.current = 0
        self.next = next
        self.prev = prev
        self.free = free

    def set_size(self, size):
        self.size = size

    def set_next(self, next):
        self.next = next

    def set_current(self, current):
        if(current > self.size):
            raise Exception("current > size")
        self.current = current

    def set_prev(self, prev):
        self.prev = prev

    def set_free(self, free):
        self.free = free


class Memory:
    def __init__(self, size):
        self.size = size
        self.block_count = 1
        self.first_block = Block(size, None, None, True)

    def get_size(self):
        return self.size

    def get_first_block(self):
        return self.first_block

    def add_block(self, block_size):
        firstB = self.first_block
        while firstB and firstB.size >= block_size*2:
            newBlock = Block(firstB.size/2, None, firstB, True)
            firstB.next = newBlock
            self.block_count += 1
            firstB.set_size(firstB.size/2)
            firstB = firstB.next

        firstB = self.first_block
        minB = firstB
        minSize = firstB.size
        while firstB and firstB.size >= block_size and firstB.free:
            if firstB.size < minSize:
                minSize = firstB.size
                minB = firstB
            firstB = firstB.next

        if minB:
            minB.set_current(block_size)
            minB.set_size(aight_bit_alignment(block_size))
            minB.set_free(False)


def main():
    memory = Memory(128)
    memory.add_block(9)

    crn_block = memory.get_first_block()

    print(f'Memory: {memory.block_count}')
    while crn_block:
        print(f'{crn_block.current}/{crn_block.size} - Frei: {crn_block.free}')
        crn_block = crn_block.next



if __name__ == '__main__':
    main()
