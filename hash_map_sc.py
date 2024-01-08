# Name: Peter Musgrove
# OSU Email: musgrovp@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 HashMap Implementation
# Due Date: 6/9/23
# Description: HashMap implemented with chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If a given key already exists, the old value will be replaced
        by the new value. If the key does not exist, the new key/value pair is added.
        """
        # table load check and capacity change if needed
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        index = self._hash_function(key) % self._capacity

        for elements in range(self._capacity):
            if elements == index:
                # if there is nothing in the linked list, add new value pair and increment size
                if self._buckets[index].length() == 0:
                    self._buckets[index] = LinkedList()
                    self._buckets[index].insert(key, value)
                    self._size += 1
                elif self._buckets[index].length() > 0:
                    # if the key is already in map, replace with new value
                    if self._buckets[index].contains(key) is not None:
                        org_node = self._buckets[index].contains(key)
                        org_node.value = value
                    else:
                        # if there is already a list, but no value
                        self._buckets[index].insert(key, value)
                        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        count = 0
        # increment each time there is an empty list
        for elements in range(self._capacity):
            if self._buckets[elements].length() < 1:
                count += 1
        return  count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        load_factor = self.get_size()/self.get_capacity()
        return load_factor

    def clear(self) -> None:
        """
        Method clears contents of hash map without changing the underlying table capacity
        """
        # replace buckets with new array, set capacity to old capacity, fill new array with lists
        capacity_holder = self.get_capacity()
        self._buckets = DynamicArray()
        self._size = 0
        self._capacity = capacity_holder
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table keeping existing key/value pairs. The hash table links are
        rehashed.
        """
        if new_capacity < 1:
            return
        else:
            if self._is_prime(new_capacity) is True:
                # if prime, clear new array and fill with values from old array
                holder_da = self._buckets
                self._capacity = new_capacity
                self.clear()
                for elements in range(holder_da.length()):
                    if holder_da[elements].length() > 0:
                        for number in holder_da[elements]:
                            self.put(number.key, number.value)
            else:
                # if not prime, get new prime then same process as above
                new_capacity = self._next_prime(new_capacity)
                holder_da = self._buckets
                self._capacity = new_capacity
                self.clear()
                for elements in range(holder_da.length()):
                    if holder_da[elements].length() > 0:
                        for number in holder_da[elements]:
                            self.put(number.key,number.value)

    def get(self, key: str):
        """
        Returns the value associated with a given key. if the key is not in the hash, returns None
        """
        for elements in range(self._capacity):
            if self._buckets[elements].contains(key) is not None:
                return self._buckets[elements].contains(key).value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise returns false
        """
        for elements in range(self._capacity):
            if self._buckets[elements].contains(key) is not None:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and associated value from the hash map
        """
        if self.contains_key(key) is False:
            return
        else:
            for elements in range(self._capacity):
                # if key is found, remove and decrement size
                if self._buckets[elements].contains(key) is not None:
                    self._buckets[elements].remove(key)
                    self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of each key/value pair in the Hash Map
        """
        holder_array = DynamicArray()
        for elements in range(self._capacity):
            if self._buckets[elements] is not None:
                for things in self._buckets[elements]:
                    holder_array.append((things.key, things.value))
        return holder_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function that receives a dynamic array and returns a tuple containing a dynamic array of the mode values and an
    integer of the frequency.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()
    # go through values in given array and add to map with initial 1 value
    for elements in range(da.length()):
        if map.contains_key(da[elements]) is False:
            map.put(da[elements], 1)
        else:
            # if value is a repeat, increment value
            count = map.get(da[elements])
            count += 1
            map.put(da[elements], count)

    # move map values to an array
    things = map.get_keys_and_values()
    mode_array = DynamicArray()
    mode = 0
    for numbers in range(things.length()):
        # add first value to mode and mode array
        if numbers == 0:
            mode_array.append(things[numbers][0])
            mode = things[numbers][1]
        # if a value is equal to current mode, append to array
        elif things[numbers][1] == mode:
            mode_array.append(things[numbers][0])
        # if a value is more than current mode, clear array and add value and key to mode and array
        elif things[numbers][1] > mode:
            mode_array = DynamicArray()
            mode_array.append(things[numbers][0])
            mode = things[numbers][1]
    return (mode_array, mode)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
