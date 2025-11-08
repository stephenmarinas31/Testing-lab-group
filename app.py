from flask import Flask, render_template, request, redirect, url_for, session


# --- 1. DATA STRUCTURES IMPLEMENTATION ---

# --- Doubly Linked List Node for Deque ---
class DLLNode:
    """Represents a single node in the Doubly Linked List."""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None  # Pointer to the previous node


# --- Singly Linked List Node for Queue ---
class SLLNode:
    """Represents a single node in the Singly Linked List (used for Queue)."""

    def __init__(self, data):
        self.data = data
        self.next = None


# --- A. Queue (FIFO) using Singly Linked List ---
class Queue:
    """Implements a Queue (FIFO) using a Singly Linked List."""

    def __init__(self):
        self.head = None  # Front (for Dequeue)
        self.tail = None  # Rear (for Enqueue)

    def is_empty(self):
        return self.head is None

    def enqueue(self, item):
        """Adds an item to the rear (O(1))."""
        new_node = SLLNode(item)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        """Removes and returns the item from the front (O(1))."""
        if self.is_empty():
            return None

        removed_data = self.head.data
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        return removed_data

    def get_elements(self):
        """Returns a list of all elements, Front -> Rear."""
        elements = []
        current = self.head
        while current is not None:
            elements.append(current.data)
            current = current.next
        return elements


# --- B. Deque (Double-Ended Queue) using Doubly Linked List ---
class Deque:
    """Implements a Deque using a Doubly Linked List."""

    def __init__(self):
        self.front = None  # Head of the DLL
        self.rear = None  # Tail of the DLL

    def is_empty(self):
        return self.front is None

    def insert_front(self, item):
        """Adds an item to the front (O(1))."""
        new_node = DLLNode(item)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node

    def insert_rear(self, item):
        """Adds an item to the rear (O(1))."""
        new_node = DLLNode(item)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node

    def delete_front(self):
        """Removes and returns the item from the front (O(1))."""
        if self.is_empty():
            return None

        removed_data = self.front.data
        self.front = self.front.next

        if self.front is None:  # Deque is now empty
            self.rear = None
        else:
            self.front.prev = None  # Clear the new front's previous link

        return removed_data

    def delete_rear(self):
        """Removes and returns the item from the rear (O(1))."""
        if self.is_empty():
            return None

        removed_data = self.rear.data
        self.rear = self.rear.prev

        if self.rear is None:  # Deque is now empty
            self.front = None
        else:
            self.rear.next = None  # Clear the new rear's next link

        return removed_data

    def get_elements(self):
        """Returns a list of all elements, Front -> Rear."""
        elements = []
        current = self.front
        while current is not None:
            elements.append(current.data)
            current = current.next
        return elements


# --- 2. FLASK APPLICATION SETUP ---

app = Flask(__name__)
app.secret_key = 'your_group_project_secret_key_123'


# --- Helper Functions for Session Management ---

def initialize_ds_from_session(ds_class, session_key, insert_func_name):
    """Initializes a DS object and populates it from session data."""
    ds = ds_class()
    if session_key in session:
        insert_func = getattr(ds, insert_func_name)
        for item in session[session_key]:
            insert_func(item)
    return ds

# ... (all your existing code: imports, DS classes, Queue/Deque routes) ...

@app.route('/profiles')
def profiles_page():
    """Route for the group members' profile page."""
    group_members = [
        {"name": "Aldred Custodio", "id": "aldred", "bio": "Eme eme."},
        {"name": "Dhandrei Blanco", "id": "dhandrei", "bio": "eme eme."},
        {"name": "Johan Fernandez", "id": "johan", "bio": "mmmhmmm."},
        {"name": "Kurt Alcoriza", "id": "kurt", "bio": "emee."},
        {"name": "Rafael Pillejera", "id": "rafael", "bio": "eme ememe emee."},
        {"name": "Rob Vera", "id": "rob", "bio": "eme emeem ."},
        {"name": "Stephen Mark Mariñas", "id": "stephen", "bio": "eme emee emee ."}
    ]
    return render_template(
        'profiles.html',
        members=group_members
    )

# ... (the rest of your app.py, including the if __name__ == '__main__': block) ...


def save_ds_to_session(ds_obj, session_key):
    """Saves the current state of the DS object back to the session."""
    session[session_key] = ds_obj.get_elements()


# --- 3. FLASK ROUTES ---

@app.route('/')
def index():
    """Simple index to navigate to the data structure pages."""
    return render_template('index.html')


@app.route('/queue', methods=['GET', 'POST'])
def queue_page():
    """Route for interacting with the Linked List Queue."""
    # Load and setup
    current_queue = initialize_ds_from_session(Queue, 'queue_data', 'enqueue')
    message = None

    if request.method == 'POST':
        action = request.form.get('action')
        item = request.form.get('item')

        if action == 'enqueue' and item:
            current_queue.enqueue(item)
            message = f"✅ ENQUEUED: '{item}' to the rear (tail)."

        elif action == 'dequeue':
            dequeued_item = current_queue.dequeue()
            if dequeued_item is not None:
                message = f"❌ DEQUEUED: '{dequeued_item}' from the front (head)."
            else:
                message = "🛑 The Queue is empty! Cannot dequeue."

        # Save state and redirect
        save_ds_to_session(current_queue, 'queue_data')
        session['queue_message'] = message
        return redirect(url_for('queue_page'))

    # Render page
    return render_template(
        'ds_template.html',
        ds_name="Queue (Linked List)",
        ds_elements=current_queue.get_elements(),
        message=session.pop('queue_message', None),
        operations={
            'primary_add': {'name': 'Enqueue (Rear)', 'action': 'enqueue', 'placeholder': 'Item to add'},
            'primary_remove': {'name': 'Dequeue (Front)', 'action': 'dequeue'},
        },
        display_info="FIFO: First element in is the first element out."
    )


@app.route('/deque', methods=['GET', 'POST'])
def deque_page():
    """Route for interacting with the Doubly Linked List Deque."""
    # Load and setup
    # We use 'insert_rear' as the initial loading function for the Deque
    current_deque = initialize_ds_from_session(Deque, 'deque_data', 'insert_rear')
    message = None

    if request.method == 'POST':
        action = request.form.get('action')
        item = request.form.get('item')

        if action == 'insert_front' and item:
            current_deque.insert_front(item)
            message = f"✅ INSERTED: '{item}' to the **front**."

        elif action == 'insert_rear' and item:
            current_deque.insert_rear(item)
            message = f"✅ INSERTED: '{item}' to the **rear**."

        elif action == 'delete_front':
            deleted_item = current_deque.delete_front()
            message = f"❌ DELETED: '{deleted_item}' from the **front**." if deleted_item else "🛑 Deque is empty!"

        elif action == 'delete_rear':
            deleted_item = current_deque.delete_rear()
            message = f"❌ DELETED: '{deleted_item}' from the **rear**." if deleted_item else "🛑 Deque is empty!"

        # Save state and redirect
        save_ds_to_session(current_deque, 'deque_data')
        session['deque_message'] = message
        return redirect(url_for('deque_page'))

    # Render page
    return render_template(
        'ds_template.html',
        ds_name="Deque (Doubly Linked List)",
        ds_elements=current_deque.get_elements(),
        message=session.pop('deque_message', None),
        operations={
            'add_front': {'name': 'Insert Front', 'action': 'insert_front', 'placeholder': 'Item to add'},
            'add_rear': {'name': 'Insert Rear', 'action': 'insert_rear', 'placeholder': 'Item to add'},
            'remove_front': {'name': 'Delete Front', 'action': 'delete_front'},
            'remove_rear': {'name': 'Delete Rear', 'action': 'delete_rear'},
        },
        display_info="Allows insertion and deletion from both the **front** and **rear**."
    )


# --- 4. EXECUTION ---
if __name__ == '__main__':
    app.run(debug=True)