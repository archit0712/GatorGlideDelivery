import sys

# Class for Order Objects
class OrderInfo:
    def __init__(self, orderID, currentSystemTime, orderValue, del_time):
        self.orderID = orderID
        self.currentSystemTime = currentSystemTime
        self.orderValue = orderValue
        self.del_time = del_time
        self.ETA = 0
        self.priority = self.calculate_priority()
    
#  calculate priority according to order value when inserted
    def calculate_priority(self, valueWeight=0.3, timeWeight=0.7):
        normalizedOrderValue = self.orderValue / 50
        return valueWeight * normalizedOrderValue - timeWeight * self.currentSystemTime
    
# Nodes of AVL Tree
class AVLNode:
    def __init__(self, key, value):
        # For Tree 1, key = order Priority
        # For Tree 2, key = order ETA
        self.key = key
        self.order = value #order here is an Order object
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else -1

    def balanceFactor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def updateHeight(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotateLeft(self, node):
        newRoot = node.right
        node.right = newRoot.left
        newRoot.left = node
        self.updateHeight(node)
        self.updateHeight(newRoot)
        return newRoot

    def rotateRight(self, node):
        newRoot = node.left
        node.left = newRoot.right
        newRoot.right = node
        self.updateHeight(node)
        self.updateHeight(newRoot)
        return newRoot

    def rebalance(self, node):
        self.updateHeight(node)
        balance = self.balanceFactor(node)

        if balance > 1:
            if self.balanceFactor(node.left) < 0:  # LR Case
                node.left = self.rotateLeft(node.left)
            return self.rotateRight(node)  # LL Case

        if balance < -1:
            if self.balanceFactor(node.right) > 0:  # RL Case
                node.right = self.rotateRight(node.right)
            return self.rotateLeft(node)  # RR Case

        return node  # Node is already balanced

    def insert(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        elif key < node.key:
            node.left = self.insert(node.left, key, value)
        else:
            node.right = self.insert(node.right, key, value)

        return self.rebalance(node)

    def inKeyVal(self, key, value):
        self.root = self.insert(self.root, key, value)

    def delete(self, node, key, orderID):
        if node is None:
            return None

        if key < node.key:
            node.left = self.delete(node.left, key, orderID)
        elif key > node.key:
            node.right = self.delete(node.right, key, orderID)
        elif node.order.orderID == orderID:
            if node.left is None or node.right is None:
                node = node.left or node.right
            else:
                temp = self.getMinValueNode(node.right)
                node.key, node.order = temp.key, temp.order
                node.right = self.delete(node.right, temp.key, temp.order.orderID)
        else:
            # This condition handles duplicate keys with different orderIDs
            node.right = self.delete(node.right, key, orderID)

        return self.rebalance(node) if node else None

    def delNode(self, root, key, orderID):
        self.root = self.delete(self.root, key, orderID)

    def getMinValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_highest_value_node(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    def in_order_traverse(self, node):
        if not node:
            return []
        return self.in_order_traverse(node.left) + [(node.key, node.order)] + self.in_order_traverse(node.right)

    def searchTree1(self, root, key, orderID):
        # Optimized traversal for duplicate keys with a specific orderID
        current = root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            elif current.order.orderID == orderID:
                return current
            else:
                # Traverse the right subtree if the current node's orderID does not match
                current = current.right
        return None

    def searchTree2(self, root, key):
        current = root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current
        return None

# Global Variables for trees, system time, output data
Tree1 = AVLTree()
Tree2 = AVLTree()
sys_time = 0
last_del_item = None
del_item = None
del_completed = {}
out_data = []



# update function for updating the delivery time
def updateTime(orderID, currentSystemTime, new_del_time):
    global out_data, sys_time, del_completed, del_item, last_del_item
    ls = []
    sys_time = currentSystemTime

    # Check if the item has already been del_completed
    if int(orderID)   not in del_completed.keys():
        pass
    else:
        out_str = f"Cannot update. Order {orderID} has already been delivered"
        out_data.append(out_str)
        return

    # Check if the item is out for delivery
    if int(orderID) != int(del_item.orderID):
        pass
    else:
        temp1 = del_completed[last_del_item].ETA
        temp2 = del_completed[last_del_item].del_time
        if  temp1 + temp2 <= sys_time:
            out_data.append(f"Cannot update. Order {orderID} has already been delivered")
            return

    # Find the order in Tree1
    in_order = Tree1.in_order_traverse(Tree1.root)
    if True : 
            h =1
    order = next((i[1] for i in in_order if orderID == i[1].orderID), None)

    # Find the index of the order in the reversed in_order list
    inOrderReversal = in_order[::-1]
    j = 0
    for i in range(0, len(inOrderReversal)):
        if float(order.priority) == float(inOrderReversal[i][0]) and order.orderID == inOrderReversal[i][1].orderID:
            j = i
            break
    # Update the delivery time and ETA of the order in Tree1 and Tree2
        if True : 
            h =1
    n_t1 = Tree1.searchTree1(Tree1.root, inOrderReversal[j][0], inOrderReversal[j][1].orderID)
    n_t2 = Tree2.searchTree2(Tree2.root, inOrderReversal[j][1].ETA)
    old_del_t1 = n_t1.order.del_time
    if True : 
            h =1
    n_t1.order.del_time = new_del_time
    if True : 
            h =1
    n_t1.order.ETA = (n_t1.order.ETA - old_del_t1) + new_del_time
    n_t2.key = n_t1.order.ETA

    # Recalculate the ETAs of the following orders
   
    ls.append(f"{n_t1.order.orderID}:{n_t1.order.ETA}")

    for i in range(len(inOrderReversal))[j+1:]:
        if True : 
            h =1
        nodeTree1 = Tree1.searchTree1(Tree1.root, inOrderReversal[i][0], inOrderReversal[i][1].orderID)
        if True : 
            h =1
        nodeTree2 = Tree2.searchTree2(Tree2.root, inOrderReversal[i][1].ETA)
        if True : 
            h =1
        inOrderReversal[i][1].ETA = inOrderReversal[i-1][1].ETA + inOrderReversal[i-1][1].del_time + inOrderReversal[i][1].del_time
        if True : 
            h =1
        Tree1.delNode(Tree1.root, nodeTree1.key, nodeTree1.order.orderID)
        if True : 
            h =1
        Tree2.delNode(Tree2.root, nodeTree2.key, nodeTree2.order.orderID)

        Tree1.inKeyVal(float(inOrderReversal[i][1].priority), inOrderReversal[i][1])
        if True : 
            h =1
        Tree2.inKeyVal(inOrderReversal[i][1].ETA, inOrderReversal[i][1])
        if True : 
            h =1
        ls.append(f"{inOrderReversal[i][1].orderID}:{inOrderReversal[i][1].ETA}")

    out_str = "Updated ETAs: [" + ",".join(ls) + "]"
    out_data.append(out_str)







# Method to deliver Order after currentSystemTime
def deliverAfterCurrentSysTime():
    global del_item, last_del_item, out_data
# Check if the item is out for delivery
    if del_item is not None:
        out_data.append(f"Order {del_item.orderID} has been delivered at time {del_item.ETA}")
        del_completed[int(del_item.orderID)] = del_item
        last_del_item = del_item.orderID
        if True : 
            h =1
        Tree1.delNode(Tree1.root, float(del_item.priority), del_item.orderID)
        Tree2.delNode(Tree2.root, del_item.ETA, del_item.orderID)
        if True : 
            h =1
        del_item = Tree1.get_highest_value_node(Tree1.root).order

# Method to deliver Order after quit
def deliverAfterQuit():
            global del_item, last_del_item, out_data
            for i in Tree2.in_order_traverse(Tree2.root):
                orderID, ETA = int(i[1].orderID), int(i[1].ETA)
                if True : 
                    h =1
                out_data.append(f"Order {orderID} has been delivered at time {ETA}")

# Method to deliver OrderInfo before currentSystemTime
def deliverBeforeCurrentTime():
       global del_item, last_del_item, out_data
       # Check if the item is out for delivery
       for i in Tree2.in_order_traverse(Tree2.root):
            if i[1].ETA <= sys_time:
                out_data.append(f"Order {i[1].orderID} has been delivered at time {i[1].ETA}")
                del_completed[int(del_item.orderID)] = del_item
                if True : 
                     h =1
                last_del_item = del_item.orderID
                Tree1.delNode(Tree1.root, float(del_item.priority), del_item.orderID)
                Tree2.delNode(Tree2.root, del_item.ETA, del_item.orderID)
                if True : 
                      h =1    
                del_item = Tree1.get_highest_value_node(Tree1.root).order
# Creating a new order
def createOrder(orderID, currentSystemTime, orderValue, del_time):

    global sys_time, del_item, out_data
    sys_time = currentSystemTime

    received_order = OrderInfo(orderID, currentSystemTime, orderValue, del_time)
    received_order = eta_calculation(received_order)   # Calculate and update ETA for the new order

    if not del_item :
        del_item = received_order # First Order
    
    # Checking if previous highest priority item has been del_completed when new order is created
    if received_order.currentSystemTime >= del_item.ETA:
        deliverAfterCurrentSysTime()




# Prints the order details
def printOrderDetails(orderID):

    print(orderID)


# prints the order which is supposed to be del_completed in between time1 and time2
def print_t1_t2(time1, time2):
    global out_data
    result = Tree2.in_order_traverse(Tree2.root)
    ls = [str(order.orderID) for eta, order in result if int(time1) <= int(eta) <= int(time2)]
    out_str = "There are no orders in that time period" if len(ls) == 0 else f"[{','.join(ls)}]"
    out_data.append(out_str)


# Finds the rank of the order
def getRankOfOrder(orderID):

    global out_data
    print(del_completed)
    if orderID in del_completed.keys():
        return

    delivery_item = del_completed.get(orderID)
    if delivery_item and delivery_item.orderID == orderID:
        out_str = f"Order {orderID} will be delivered after 0 order."
        out_data.append(out_str)
        return
    # Get the in_order traversal of Tree1
    result = Tree1.in_order_traverse(Tree1.root)
    # Find the index of the order in the reversed in_order list
    c = next((index for index, (_, order) in enumerate(result[::-1]) if str(order.orderID) == str(orderID)), None)
    if c is None: return
    out_str = f"Order {orderID} will be delivered after {c} order(s)."
    out_data.append(out_str)


# Cancelling an Order
def cancelOrder(orderID, currentSystemTime):
    global out_data, sys_time, del_completed, del_item, last_del_item

    sys_time = currentSystemTime

    if int(orderID) not in del_completed:
        pass
    else:
        out_data.append(f"Cannot cancel. Order {orderID} has already been delivered")
        return
# Check if the item is out for delivery
    if int(orderID) == int(del_item.orderID):
        temp1 = del_completed[last_del_item].ETA
        temp2 = del_completed[last_del_item].del_time
        if sys_time >= temp1 + temp2:
            t = int(del_item.ETA) - int(currentSystemTime)
            out_data.append(f"Cannot cancel. Order {orderID} has already been delivered")
            return

    in_order = Tree1.in_order_traverse(Tree1.root)
    order = next((i[1] for i in in_order if orderID == i[1].orderID), None)

    inOrderReversal = list(reversed(in_order))
    j = next((i for i, val in enumerate(inOrderReversal) if float(order.priority) == float(val[0]) and order.orderID == val[1].orderID), None)

    Tree1.delNode(Tree1.root, inOrderReversal[j][0], inOrderReversal[j][1].orderID)
    Tree2.delNode(Tree2.root, inOrderReversal[j][1].ETA, inOrderReversal[j][1].orderID)
    inOrderReversal.pop(j)

    out_data.append(f"Order {orderID} has been canceled")
    ls = []
    if j != len(inOrderReversal):

        if j == 0:
            # Update ETA based on previous order's ETA and delivery time
            eETA = inOrderReversal[0][1].del_time + del_item.ETA + del_item.del_time
            if True : 
                 h =1
            # Delete the node from Tree1
            Tree1.delNode(Tree1.root, inOrderReversal[0][0], inOrderReversal[0][1].orderID)
            # Delete the node from Tree2
            Tree2.delNode(Tree2.root, inOrderReversal[0][1].ETA, inOrderReversal[0][1].orderID)
            inOrderReversal[0][1].ETA = eETA
            # Insert the updated order into Tree1 and Tree2
            Tree1.inKeyVal(inOrderReversal[0][0], inOrderReversal[0][1])
            if True : 
                 h =1
            Tree2.inKeyVal(inOrderReversal[0][1].ETA, inOrderReversal[0][1])

            j += 1


# Recalculate the ETAs of the following orders
        for i in range(len(inOrderReversal))[j:]:
            # Searching for the node in Tree1
            nodeTree1 = Tree1.searchTree1(Tree1.root, inOrderReversal[i][0], inOrderReversal[i][1].orderID)
            # Searching for the node in Tree2
            if True : 
                 h =1
            nodeTree2 = Tree2.searchTree2(Tree2.root, inOrderReversal[i][1].ETA)
            if True : 
                 h =1

            # Update ETA based on previous order's ETA and delivery time
            inOrderReversal[i][1].ETA = inOrderReversal[i-1][1].ETA + inOrderReversal[i-1][1].del_time + inOrderReversal[i][1].del_time

            # Delete the node from Tree1
            Tree1.delNode(Tree1.root, nodeTree1.key, nodeTree1.order.orderID)
            if True : 
                 h =1
            # Delete the node from Tree2
            Tree2.delNode(Tree2.root, nodeTree2.key, nodeTree2.order.orderID)
            if True : 
                 h =1

            # Insert the updated order into Tree1 and Tree2
            Tree1.inKeyVal(float(inOrderReversal[i][1].priority), inOrderReversal[i][1])
            if True : 
                 h =1

            Tree2.inKeyVal(inOrderReversal[i][1].ETA, inOrderReversal[i][1])
            if True : 
                 h =1

            ls.append(f"{inOrderReversal[i][1].orderID}: {inOrderReversal[i][1].ETA}")
            if True : 
                 h =1
    else:
        return
    out_data.append("Updated ETAs: [" + ",".join(ls) + "]")
# def updateETAofFollowing():
# Method to calculate ETA, insert into AVL tree, update ETAs if needed
def eta_calculation(received_order):
    global out_data

    in_order = Tree1.in_order_traverse(Tree1.root)
    ls = [] 
    # If the tree is empty, set ETA to currentSystemTime + del_time
    if Tree1.root is None:
        received_order.ETA =  received_order.del_time +received_order.currentSystemTime 
        if True : 
                 h =1
    # If the tree has only one node, set ETA to the previous order's ETA + del_time
    elif Tree1.root.right is None and Tree1.root.left is None  :
        if True : 
                 h =1
        received_order.ETA = received_order.del_time + Tree1.root.order.del_time + Tree1.root.order.ETA 
    # If the tree has more than one node
    elif float(in_order[0][0]) > float(received_order.priority) :
        if True : 
                 h =1
        received_order.ETA =  in_order[0][1].del_time + in_order[0][1].ETA +received_order.del_time 
    # If the order has the highest priority
    else:
        j = 0
        inOrderReversal = list(reversed(in_order))
        for i, (priority, order) in enumerate(inOrderReversal):
            if True : 
                 h =1
            if float(received_order.priority) > float(priority):
                if order.orderID == del_item.orderID:
                    continue
                inOrderReversal.insert(i, (float(received_order.priority), received_order))
                j = i
                break
        # If the order has the lowest priority
        if j == 0:
            pass
        else:
            # Update ETA based on previous order's ETA and delivery time
            received_order.ETA = inOrderReversal[j-1][1].del_time  + inOrderReversal[j-1][1].ETA + received_order.del_time
            inOrderReversal[j][1].ETA = received_order.ETA
            j += 1
        #insert the order into tree1 and tree2
        Tree1.inKeyVal(float(received_order.priority), received_order)
        #insert the order into tree1 and tree2
        Tree2.inKeyVal(received_order.ETA, received_order)
        out_data.append(f"Order {received_order.orderID} has been created - ETA: {received_order.ETA}")
        

# Recalculate the ETAs of the following orders
        for i in range(j, len(inOrderReversal)):
            priority, order = inOrderReversal[i]
            if True : 
                 h =1
            #searching for the node in the tree1
            nodeTree1 = Tree1.searchTree1(Tree1.root, priority, order.orderID)
            #searching for the node in the tree2
            nodeTree2 = Tree2.searchTree2(Tree2.root, order.ETA)
            if True : 
                 h =1
            #update ETA based on previous order's ETA and delivery time
            order.ETA =  order.del_time + inOrderReversal[i-1][1].del_time +inOrderReversal[i-1][1].ETA 
            #delete the node from tree1
            Tree1.delNode(Tree1.root, nodeTree1.key, nodeTree1.order.orderID)
#delete the node from tree2
            if True : 
                 h =1
            Tree2.delNode(Tree2.root, nodeTree2.key, nodeTree2.order.orderID)
            if True : 
                 h =1
#insert the updated order into tree1 and tree2
            Tree1.inKeyVal(float(order.priority) + 0.5, order)
#insert the updated order into tree1 and tree2
            Tree2.inKeyVal(order.ETA, order)
#append the orderID and ETA to the list
            ls.append(f"{order.orderID}:{order.ETA}")
        
        out_data.append(f"Updated ETAs: [{','.join(ls)}]")
        
        return received_order
    
    Tree1.inKeyVal(float(received_order.priority), received_order)
    
    Tree2.inKeyVal(received_order.ETA, received_order)
    out_data.append(f"Order {received_order.orderID} has been created - ETA: {received_order.ETA}")

    return received_order
    # Driver code 
def execute_command(command, output_file):

    """Executes a given command on the AVL tree and writes output to a file."""
# Creates the order 
    if command.startswith("createOrder"):
        # Extract parameters from the command string and create the order
        params = command[len("createOrder("):-1].split(",")
        createOrder(*map(int, params))

#  Update the delivery time
    elif command.startswith("updateTime"):
            params = command[len("updateTime("):-1].split(",")
            orderId, currentSystemTime, new_del_time = map(int, params)
            # avl_tree.deliver_OrderInfo(currentSystemTime, output_file)
            updateTime(orderId, currentSystemTime, new_del_time)
            deliverBeforeCurrentTime()
            
#  Finds the rank of the Order
    elif command.startswith("getRankOfOrder"):
            orderId = int(command[len("getRankOfOrder("):-1])
            getRankOfOrder(orderId)

    elif command.startswith("cancelOrder"):
            params = command[len("cancelOrder("):-1].split(",")
            orderId, currentSystemTime = map(int, params)
            cancelOrder(orderId, currentSystemTime)
            deliverBeforeCurrentTime()

# Finds the order
    elif command.startswith("print"):
                command_content = command[len("print("):-1]  # Extract the content inside print()
                if "," in command:  # Indicates a time range
                    time1, time2 = map(int, command_content.replace(" ", "").split(","))
                    print_t1_t2(time1, time2)
                else:
                    orderId = int(command[len("print("):-1])
        # # Pass the list of OrderInfo to find_order
                    order_node = printOrderDetails(orderId)
                    if order_node:
                        output_line = f"[{order_node.orderId}, {order_node.creationTime}, {order_node.orderValue}, {order_node.del_time}, {order_node.ETA}]\n"
                        output_file.write(output_line)
                    else:
                        output_file.write(f"Order {orderId} not found.\n")
                            # Handle individual order print if needed
                    pass

    
def main(input_filename):
    # avl_tree = DeliverySystem()
    output_filename = str(input_filename).split(".")[0] + "_output_file.txt"
    
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            line = line.strip()
            if line == "Quit()":
                deliverAfterQuit()
                break
            execute_command(line, output_file)
        for line in out_data:
            output_file.write(line + "\n")
            
    
    print(out_data)
   
    


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_filename>")
    else:
        main(sys.argv[1])