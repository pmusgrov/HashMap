# Name: Peter Musgrove
# OSU Email: musgrovp@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 HashMap Implementation
# Due Date: 6/9/23
# Description: HashMap implemented with open addressing 

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        # load check and initial index creation
        if self.table_load() >= .5:
            self.resize_table(self._capacity * 2)

        initial_index = self._hash_function(key) % self._capacity

        # if key is already in map, update with new value
        if self.contains_key(key) is True:
            for elements in range(self._capacity):
                if self._buckets[elements] is not None and self._buckets[elements].key == key and self._buckets[elements].is_tombstone is False:
                    self._buckets[elements].value = value
                    return

        count = 1
        index = initial_index
        for elements in range(self._capacity):
            if elements == initial_index:
                # if first index is free, add pair and increment size
                if self._buckets[index] is None:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                # if first index holds TS, replace with pair and increment size
                elif self._buckets[index].is_tombstone is True:
                     self._buckets[index] = HashEntry(key, value)
                     self._size += 1
                else:
                    # if first index is taken, probe till free index and then add as above
                    while self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                        index = (initial_index + (count ** 2)) % self._capacity
                        count += 1
                    if self._buckets[index] is None:
                        self._buckets[index] = HashEntry(key, value)
                        self._size += 1
                    elif self._buckets[index].is_tombstone is True:
                        self._buckets[index] = HashEntry(key, value)
                        self._size += 1



        
    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        load_factor = self.get_size() / self.get_capacity()
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        count = 0
        for elements in range(self._capacity):
            # check for empty buckets and buckets with TBs
            if self._buckets[elements] is None:
                count += 1
            elif self._buckets[elements] is not None and self._buckets[elements].is_tombstone is True:
                count +=1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table keeping existing key/value pairs. The hash table links are
        rehashed.
        """
        if new_capacity < self._size:
            return
        else:
            if self._is_prime(new_capacity) is True:
                # if prime, clear new array and fill with values from old array, TS values not taken
                holder_da = self._buckets
                self._capacity = new_capacity
                self.clear()
                for elements in range(holder_da.length()):
                    if holder_da[elements]  is not None and holder_da[elements].is_tombstone is False:
                        self.put(holder_da[elements].key, holder_da[elements].value)
            else:
                # if not prime, get new prime then same process as above
                new_capacity = self._next_prime(new_capacity)
                holder_da = self._buckets
                self._capacity = new_capacity
                self.clear()
                for elements in range(holder_da.length()):
                    if holder_da[elements] is not None and holder_da[elements].is_tombstone is False:
                        self.put(holder_da[elements].key, holder_da[elements].value)



    def get(self, key: str) -> object:
        """
        Returns the value associated with a given key. if the key is not in the hash, returns None
        """
        for elements in range(self._capacity):
            # check for values, avoid TS
            if self._buckets[elements] is not None and self._buckets[elements].key == key \
                    and self._buckets[elements].is_tombstone is False:
                return self._buckets[elements].value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise returns false
        """
        for elements in range(self._capacity):
            if self._buckets[elements] is not None and self._buckets[elements].key == key \
                    and self._buckets[elements].is_tombstone is False:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        method removes the given key and its associated value from the hash map.
        """
        if self.contains_key(key) is False:
            return
        else:
            for elements in range(self._capacity):
                # if found, change TS status to True and decrement size
                if self._buckets[elements] is not None and self._buckets[elements].key == key \
                        and self._buckets[elements].is_tombstone is False:
                    self._buckets[elements].is_tombstone = True
                    self._size -= 1

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        # replace buckets with new array, set capacity to old capacity, fill new array with None values
        capacity_holder = self.get_capacity()
        self._buckets = DynamicArray()
        self._size = 0
        self._capacity = capacity_holder
        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array of each key/value pair in the Hash Map
        """
        holder_array = DynamicArray()
        for elements in range(self._capacity):
            # move values to array, avoiding TS
            if self._buckets[elements] is not None and self._buckets[elements].is_tombstone is False:
                holder_array.append((self._buckets[elements].key, self._buckets[elements].value))
        return holder_array

    def __iter__(self):
        """
        Enables the hash map to iterate across itself
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based on the current location of the iterator
        """
        # check to avoid None issues
        try:
            value = self._buckets[self._index].value
        except AttributeError:
            raise StopIteration

        self._index = self._index + 1
        return value


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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
