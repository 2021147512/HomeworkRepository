"""
NAME: [Dongil Kim]
YID: [2021147512]

CSI2103: Data Structures
doublylinkedlist.py
Instructor: Seong Jae Hwang

2D doubly linked list utils for HW1.
"""

import numpy as np

class Node:
    """ Node class
        
            up
             |
    left - data - right
             |
           down
    """

    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        
        
def dllToArray(dll_ptr):
    """ Converts a 2D doubly linked list into an array.
    
    input: 
        dll_ptr: the head (most upper left node) of a 2D dll.
        
    output:
        image: a multi-dimensional array of height x width x channel
            where channel is the dimension of dll.data.
            If dll is originally constructed from a color image, then channel = 3.
            If dll is originally constructed from a 2D array, then channel = 1.
    """
    
    # Height and width of the dll determines the size of the array
    height = getHeight(dll_ptr);
    width = getWidth(dll_ptr);
    
    # Check the dimension of the data
    channel = dll_ptr.data.size
    image = np.empty([height, width, channel])
    down_ptr = dll_ptr
    x = 0
    y = 0
    
    while down_ptr != None:
        right_ptr = down_ptr
        x = 0
        
        while right_ptr != None:
            # When image is stored in a 2D array, the (x,y) location of the image
            # has to be accessed by array[y][x]. This is because the first dimension
            # index of array is for the vertical index 
            # (y-direction, or row-direction) while the second dimension of array 
            # is for the horizontal index (x-direction, or column-direction)
            image[y][x] = right_ptr.data
            right_ptr = right_ptr.right
            x += 1
        down_ptr = down_ptr.down
        y += 1
        
    return image


def display(dll_ptr):
    """ Prints the 2D dll according to their positions similar to 
        printing a 2D array.
    
    input:
        dll_ptr: the head (most upper left node) of a 2D dll.
        
    output:
        None
    """
    right_ptr = None
    down_ptr = dll_ptr
    
    while down_ptr != None:
        right_ptr = down_ptr
        
        while right_ptr != None:
            print(right_ptr.data, end=' ')
            right_ptr = right_ptr.right
        print()
        down_ptr = down_ptr.down
        
        
def compareDLL(dll1, dll2):
    """ Compare two DLLs. This compares all four pointers of each node.
    
    input:
        dll1: the first DLL to compare
        dll2: the second DLL to compare
        
    output:
        true iff dll1 == dll2. false iff not.
    """
    right_dll1 = None
    down_dll1 = dll1
    right_dll2 = None
    down_dll2 = dll2
    
    try:
        while down_dll1 != None:
            right_dll1 = down_dll1
            right_dll2 = down_dll2

            while right_dll1 != None:
                assert(compareNodes(right_dll1, right_dll2))
                assert(compareNodes(right_dll1.left, right_dll2.left))
                assert(compareNodes(right_dll1.right, right_dll2.right))
                assert(compareNodes(right_dll1.up, right_dll2.up))
                assert(compareNodes(right_dll1.down, right_dll2.down))
                right_dll1 = right_dll1.right
                right_dll2 = right_dll2.right
            down_dll1 = down_dll1.down
            down_dll2 = down_dll2.down
            
        print("DLL Comparison: Two DLLs Match!")
    except AssertionError as e:
        print("DLL Comparison: Two DLLs Do NOT Match!")
        
        
def compareNodes(node1, node2):
    """ Simple comparison of two nodes.
    
    input:
        node1
        node2
        
    output:
        boolean: true iff node1 == node2, also handles None
    """
    if node1 is None or node2 is None:
        return node1 == node2
    else:
        return node1.data == node2.data
        

def findSeam(energy_map):
    """ Assigns negative infinity to the horizontal seam given an energy map.
    This is a greedy algorithm which starts from the right most column and
    iteratively picks the minimum entry from left, left.up, and left.down.
    The path is marked by changing the energy_map value along the path to be
    negative infinity.
    
    input:
        energy_map: The cumulative energy map to find the path.
        
    output:
        energy_map: The new cumulative energy map where the path has values
            with negative infinity.
    """
    y_ptr = energy_map
    
    while y_ptr.right != None:
        y_ptr = y_ptr.right
        
    min_ptr = y_ptr
    
    while y_ptr.down != None:
        y_ptr = y_ptr.down
        if y_ptr.data < min_ptr.data:
            min_ptr = y_ptr
            
    min_ptr.data = np.NINF
    while min_ptr.left != None:
        
        min_ptr_leftup = min_ptr.left.up
        min_ptr_left = min_ptr.left
        min_ptr_leftdown = min_ptr.left.down
        
        if(min_ptr_leftup.data <= min_ptr_left.data
           and min_ptr_leftup.data <= min_ptr_leftdown.data):
            min_ptr = min_ptr_leftup
        elif(min_ptr_left.data <= min_ptr_leftup.data
           and min_ptr_left.data <= min_ptr_leftdown.data):
            min_ptr = min_ptr_left
        else:
            min_ptr = min_ptr_leftdown
        
        min_ptr.data = np.NINF
        
    return energy_map


def constructDoublyLinkedListRecursion(arr):
    """ Converts a 2D array into a 2D doubly linked list by calling
    the recursee constructDLLRecursiveStep.
 
    input:
        arr: 2D array to turn into a 2D DLL
        
    output:
        head (top left node) of the 2D DLL of the input arr.
    """
    return constructDLLRecursiveStep(arr, 0, 0, None)
        
    
def getHeight(dll_ptr):
    """ Returns the height of a 2D dll. 
    
    input:
        dll_ptr: the head (most upper left node) of a 2D dll.
        
    output:
        height: the vertical length of the 2D dll.
    """
    height = 0
    while dll_ptr != None:
        dll_ptr = dll_ptr.down
        height += 1
    return height


def removeSeam(image, energy_map):
    """ 
    1. Finds the starting node of the recursive seam removal which is the
        node with -infinity value in the leftmost column of energy map (em_ptr).
        a. Note we also move the pointer to the same location in the image (im_ptr).
    2. Calls the recursive function removeNodeRecursive which starts
        from the node found in step 1, and moves towards the left
        to remove the nodes with -infinity values.
    
    input:
        image: The image in 2D DLL. The seam to remove is the path
            alont the nodes with -infinity values in energy_map.
        energy_map: The energy map in 2D DLL. This contains the seam
            which is the horizontal path of nodes with -infinity values.
                
    output:
        image: The image in 2D DLL after the seam has been removed.
        energy_map: The energy map in 2D DLL after teh seam has been removed.
    """
    em_ptr = energy_map
    im_ptr = image
    
    while em_ptr.down != None:
        em_ptr = em_ptr.down
        im_ptr = im_ptr.down
        if np.isneginf(em_ptr.data):
            min_em_ptr = em_ptr
            min_im_ptr = im_ptr
    
    removeNodeRecursive(min_em_ptr, min_im_ptr)
    
    return [image, energy_map]

# -------------------------- DO NOT CHANGE ABOVE CODES ------------------- #

# -------------------------- IMPLEMENT BELOW YOURSELF -------------------- #


def getWidth(dll_ptr):
    """ Returns the width of a 2D dll. 
    
    input:
        dll_ptr: the head (most upper left node) of a 2D dll.
        
    output:
        width: the horizontal length of the 2D dll.
    """
    width = 0
    # Go to the right until there is no node
    while dll_ptr != None:
        dll_ptr = dll_ptr.right
        width += 1
    return width


def constructDoublyLinkedListLoop(arr):
    """ Converts a 2D array into a 2D doubly linked list with loops.
 
    input:
        arr: 2D array to turn into a 2D DLL
        
    output:
        top_left_ptr: head (top left node) of the 2D DLL of the input arr.
    """
    # init variables
    current_ptr = Node(arr[0][0])
    top_left_ptr = current_ptr

    # iterate the outer loop (y-axis)
    for i in range(len(arr)):

        # store the 0th index (x index)
        down_ptr = current_ptr

        # iterate the inner loop (x-axis)
        for j in range(len(arr[0])-1):
            rightNode = Node(arr[i][j+1]) # create a new node on the right and connect
            current_ptr.right = rightNode
            rightNode.left = current_ptr

            # connect the new node with the node above it
            if i > 0: 
                rightNode.up = current_ptr.up.right
                current_ptr.up.right.down = rightNode
            
            # move the pointer to the right
            current_ptr = current_ptr.right

        # create a new node below(down) and connect when finished iterating one line (x-axis)
        if i < len(arr)-1: 
            current_ptr = down_ptr
            downNode = Node(arr[i+1][0])
            current_ptr.down = downNode
            downNode.up = current_ptr

            current_ptr = current_ptr.down
        
    return top_left_ptr


def constructDLLRecursiveStep(arr, y, x, curr):
    """ Recursively construct the 2D DLL from the given array.
    This is the "recursee" of constructDoublyLinkedListRecursion.
    
    input:
        arr: The 2D array to construct the 2D DLL from.
        y: y-coordinate of the array to get the value from.
        x: x-coordinate of the array to get the value from.
        curr: The current node to connect the new node from.
        
    output:
        new_node: The newly created node which connects to curr node.
    """
    # create a new node
    new_node = Node(arr[y][x]) 
    
    # create nodes along the 0th x-index first until we reach the end(down)
    if y < len(arr)-1 and x == 0: 
        down_node = constructDLLRecursiveStep(arr, y+1, x, new_node)
        new_node.down = down_node
        down_node.up = new_node

    # then create nodes on the right for each line recursively until we reach the top
    if x < len(arr[0])-1:
        right_node = constructDLLRecursiveStep(arr, y, x+1, new_node)
        new_node.right = right_node
        right_node.left = new_node

    # connect nodes up and down 
    if y < len(arr)-1 and x == 0:
        tempNode = new_node

        while x < len(arr[0])-1:
            tempNode.right.down = tempNode.down.right
            tempNode.down.right.up = tempNode.right
            tempNode = tempNode.right
            x += 1
                
    return new_node
    
    
def removeNodeRecursive(em_ptr, im_ptr):
    """ Recursive seam removal function.
    Given the current node (em_ptr), suppose it has the
    following neighbor nodes:
    
    UL: Upper Left
    U: Up
    UR: Upper Right
    L: Left
    DL: Down Left
    D: Down
    DR: Down Right
        
    UL --   U    -- UR
    |       |       |
    L  -- em_ptr -- R
    |       |       |
    DL --   D    -- DR
    
    1. em_ptr should be removed because em_ptr.data has NINF.
        a. Do the same for the image 2D DLL using im_ptr.
    2. Only one of UR, R, or DR has -INF data.
        a. Example: if checking R, use np.isneginf(em_ptr.right.data)
    3. Recursively call the next node with NINF you found.
        a. Depending which one of UR, R, or DR you remove next, you need to
            carefully restructure the nodes. See Step 3 of the HW2 slides
            for an example.
           
    Note: You do not need to consider the corner case where
        the nodes to remove are along the image edges (e.g., nodes with up or down 
        nodes that are None). 
           
    input:
        em_ptr: pointer to the energy map node to remove.
        im_ptr: pointer to the image node to remove.
        
    output:
        none
    """

    # start from left to right
    # "marking" which nodes to later remove
    if em_ptr.right != None:
        UR = em_ptr.right.up
        R = em_ptr.right
        DR = em_ptr.right.down

        if np.isneginf(UR.data):
            removeNodeRecursive(UR, im_ptr.right.up)

        elif np.isneginf(R.data):
            removeNodeRecursive(R, im_ptr.right)

            
        elif np.isneginf(DR.data):
            removeNodeRecursive(DR, im_ptr.right.down)

    # connect the node's (the node we are removing) top and down nodes
    if em_ptr.up != None and em_ptr.down != None:
        em_ptr.up.down = em_ptr.down
        em_ptr.down.up = em_ptr.up

        # do the same for image nodes
        im_ptr.down.up = im_ptr.up
        im_ptr.up.down = im_ptr.down

    # when there no nodes above or below respectively
    elif em_ptr.up == None:
        em_ptr.down.up = None
    
    elif em_ptr.down == None:
        em_ptr.up.down = None
        

    # start from right to left 
    # restructure nodes according to the position of the node we are removing
    if em_ptr.left != None:
        if np.isneginf(em_ptr.left.up.data):
            em_ptr.up.left = em_ptr.left
            em_ptr.left.right = em_ptr.up

            im_ptr.up.left = im_ptr.left
            im_ptr.left.right = im_ptr.up

        elif np.isneginf(em_ptr.left.down.data):
            em_ptr.down.left = em_ptr.left
            em_ptr.left.right = em_ptr.down

            im_ptr.down.left = im_ptr.left
            im_ptr.left.right = im_ptr.down
