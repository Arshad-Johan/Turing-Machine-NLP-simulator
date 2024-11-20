import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import time

class TuringMachine:
    def __init__(self, states, input_symbols, tape_symbols, transitions, start_state, accept_states):
        self.states = states
        self.input_symbols = input_symbols
        self.tape_symbols = tape_symbols
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
        self.tape = []
        self.head_position = 0
        self.current_state = start_state

    def load_input(self, input_string):
        self.tape = list(input_string) + ['_'] * 10 
        self.head_position = 0
        self.current_state = self.start_state

    def step(self):
        if self.current_state in self.accept_states:
            return "Accepted"
        
        current_symbol = self.tape[self.head_position]

        if (self.current_state, current_symbol) in self.transitions:
            next_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.head_position] = write_symbol
            self.current_state = next_state
            
            if direction == 'R':
                self.head_position += 1
            elif direction == 'L':
                self.head_position -= 1

            if self.head_position < 0:
                self.tape.insert(0, '_')
                self.head_position = 0
            elif self.head_position >= len(self.tape):
                self.tape.append('_')
            
            return "Continue"
        else:
            return "Rejected"

    def display_tape(self):

        left_index = max(0, self.head_position - 5)
        right_index = min(len(self.tape), self.head_position + 5)
        return ''.join(self.tape[left_index:right_index]), self.head_position - left_index


class TuringMachine2:
    def __init__(self, tape): 
        self.tape = list(tape) + ['_'] 
        self.head = 0 
        self.state = 'START'
        self.tokens = []
        self.current_token = ""

    def transition(self):
        steps = [] 
        while self.head < len(self.tape):
            current_symbol = self.tape[self.head]

            if self.state == 'START':
                if current_symbol.isalnum() or current_symbol in ["'", "-"]:
                    self.state = 'READING_TOKEN'
                    self.current_token += current_symbol 
                else:
                    self.head += 1  
                self.head += 1  

            elif self.state == 'READING_TOKEN':
                if current_symbol.isalnum() or current_symbol in ["'", "-"]:
                    self.current_token += current_symbol  
                else:
                    if self.current_token:  
                        self.tokens.append(self.current_token) 
                        self.current_token = ""  
                    self.state = 'START' 
                    
                self.head += 1  

           
            steps.append((self.head, self.state, self.current_token, list(self.tokens)))

        
        if self.state == 'READING_TOKEN' and self.current_token:
            self.tokens.append(self.current_token)

        return steps  

    def tokenize(self):
        self.transition() 
        return self.tokens

def pos_tagging(tokens):
    pos_tags = []
    simple_pos_dict = {
        'NN': ['cat', 'dog', 'car', 'house', 'book', 'tree', 'garden', 'computer', 'phone', 'university', 'teacher', 'student', 'ball', 'fish', 'city', 'country'],
        'NNS': ['cats', 'dogs', 'cars', 'houses', 'books', 'trees', 'gardens', 'computers', 'phones', 'universities', 'teachers', 'students', 'balls', 'fishes', 'cities', 'countries'],
        'NNP': ['alice', 'mary', 'john', 'david', 'sophia', 'tom', 'new york', 'london', 'paris', 'google', 'openai'],  # Proper nouns
        'VB': ['run', 'walk', 'swim', 'eat', 'talk', 'read', 'write', 'jump', 'drive', 'sleep', 'watch', 'play', 'sing', 'dance', 'cook', 'study', 'travel'],  # Adding 'travel'
        'VBZ': ['runs', 'walks', 'swims', 'eats', 'talks', 'reads', 'writes', 'jumps', 'drives', 'sleeps', 'watches', 'plays', 'sings', 'dances', 'cooks', 'studies'],  # Third person singular present
        'JJ': ['big', 'small', 'red', 'blue', 'happy', 'sad', 'bright', 'dark', 'quick', 'slow', 'cold', 'hot', 'tall', 'short', 'wide', 'narrow'],
        'RB': ['quickly', 'silently', 'well', 'happily', 'sadly', 'loudly', 'softly', 'badly', 'carefully', 'easily', 'frequently', 'bravely', 'smartly'],
        'IN': ['in', 'on', 'at', 'between', 'with', 'under', 'over', 'about', 'for', 'to', 'from', 'by', 'through', 'during', 'before', 'after'],
        'CC': ['and', 'or', 'but'], 
        'DT': ['the', 'a', 'an'],  
    }


    for token in tokens:
        tag_found = False
        for tag, words in simple_pos_dict.items():
            if token.lower() in words:
                pos_tags.append((token, tag))
                tag_found = True
                break
        if not tag_found:
            pos_tags.append((token, 'NN'))  
    return pos_tags

def named_entity_recognition(tokens):
    named_entities = []
    simple_entities = {
        'PERSON': ['Alice', 'Bob', 'John', 'Mary', 'Tom', 'Sara', 'David', 'Emma', 'Sophia', 'Liam', 'Mia'],
        'ORG': ['OpenAI', 'Google', 'Microsoft', 'Amazon', 'Facebook', 'Twitter', 'Apple', 'NASA', 'IBM'],
        'GPE': ['Paris', 'New York', 'India', 'London', 'Tokyo', 'Sydney', 'Berlin', 'Rome', 'Toronto', 'Dubai']
    }

    for token in tokens:
        entity_found = False
        for entity, names in simple_entities.items():
            if token in names:
                named_entities.append((token, entity))
                entity_found = True
                break
        if not entity_found:
            named_entities.append((token, 'O'))  
    return named_entities


def display_turing_machine_tokenization(sentence):
    tm = TuringMachine2(sentence)
    
    unique_key = f"start_animation_{hash(sentence)}" 

    if st.button("Start Step", key=unique_key):  
        steps = tm.transition() 
        
        placeholder = st.empty()  
        for head_position, state, current_token, tokens in steps:
            with placeholder.container():  
                tape_display = " ".join(["_" if i == head_position else char for i, char in enumerate(tm.tape)])
                st.write(f"Tape: {tape_display}")
                st.write(f"Head Position: {head_position}")
                st.write(f"Current State: {state}")
                st.write(f"Current Token: '{current_token}'")
                st.write(f"Tokens: {tokens}")
                st.write("---")
            time.sleep(1) 
    display_dfa()

    tokens = tm.tokenize()  
    return tokens

def display_dfa():
    G = nx.DiGraph()

    G.add_node("q0", label="START")
    G.add_node("q1", label="READING_TOKEN")
    G.add_node("q2", label="TOKEN_COMPLETE")

    G.add_edge("q0", "q1", label="alphanumeric")  
    G.add_edge("q1", "q1", label="alphanumeric")  
    G.add_edge("q1", "q0", label="space")          
    G.add_edge("q0", "q2", label="blank")         

    plt.figure(figsize=(8, 6))  
    pos = nx.spring_layout(G, k=1.5) 
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    st.pyplot(plt) 
    plt.close()  
st.title("Turing Machine NLP Simulator")
st.write("Enter a sentence to see tokenization, POS tagging, named entities, and NDFA representation.")

st.subheader("Examples")
examples = [
    "Alice walks well silently to Google",
    "The quick brown fox jumps over the lazy dogs",
    "Mary eats at Google in New York",
    "John quickly writes code for OpenAI",
    "David sings loudly in the park",
    "The big red car drove through the city",
    "Sophia and Tom traveled to London and Paris",
    "The teacher reads a book about science",
    "A happy dog runs quickly in the garden",
    "Mia studies at the university in New York"
]
example_choice = st.selectbox("Select an example sentence:", examples)
user_input = st.text_input("Or enter your own sentence:", example_choice)



if user_input:
    st.subheader("Tokenization using Turing Machine")

    tokens = display_turing_machine_tokenization(user_input)
    pos_tags = pos_tagging(tokens)
    named_entities = named_entity_recognition(tokens)


    st.write("Tokens:", tokens)

    st.subheader("POS Tags")
    st.write(pos_tags)

    st.subheader("Named Entities")
    st.write([[ne[0], ne[1]] for ne in named_entities]) 

    st.title("Turing Machine Simulator")

    states = st.text_input("Enter states (comma-separated)", "q_start,q_odd,q_even,q_accept,q_reject").split(',')
    input_symbols = st.text_input("Enter input symbols (comma-separated)", "0,1").split(',')
    tape_symbols = st.text_input("Enter tape symbols (comma-separated)", "0,1,_").split(',')
    
    transitions_input = st.text_area("Enter transitions (format: current_state,current_symbol -> next_state,write_symbol,direction)\nSeparate multiple transitions with new lines",
                                      "q_start,0 -> q_even,0,R\nq_start,1 -> q_odd,1,R\nq_even,0 -> q_even,0,R\nq_even,1 -> q_odd,1,R\nq_even,_ -> q_accept,_,R\nq_odd,0 -> q_odd,0,R\nq_odd,1 -> q_even,1,R\nq_odd,_ -> q_reject,_,R")
    
    transitions = {}
    for line in transitions_input.splitlines():
        line = line.strip()
        if line:
            try:
                parts = line.split("->")
                if len(parts) != 2:
                    st.error(f"Invalid transition format: {line}")
                    continue

                state_symbol = parts[0].strip().split(',')
                action_parts = parts[1].strip().split(',')

                if len(state_symbol) != 2 or len(action_parts) != 3:
                    st.error(f"Invalid transition format: {line}. Expected format: current_state,current_symbol -> next_state,write_symbol,direction")
                    continue

                current_state, current_symbol = state_symbol[0].strip(), state_symbol[1].strip()
                next_state, write_symbol, direction = action_parts[0].strip(), action_parts[1].strip(), action_parts[2].strip()

                if direction not in ['L', 'R']:
                    st.error(f"Invalid direction '{direction}' in transition: {line}. Must be 'L' or 'R'.")
                    continue
                
                if current_symbol not in tape_symbols or write_symbol not in tape_symbols:
                    st.error(f"Invalid tape symbol in transition: {line}. Ensure symbols are defined in tape symbols.")
                    continue
                
                transitions[(current_state, current_symbol)] = (next_state, write_symbol, direction)

            except Exception as e:
                st.error(f"Error processing line: {line}. Error: {e}")

    start_state = st.selectbox("Select start state", states)
    accept_states = st.text_input("Enter accept states (comma-separated)", "q_accept").split(',')

    input_string = st.text_input("Enter input string", "0")

    if 'tm' not in st.session_state:
        st.session_state.tm = None

    if st.button("Initialize Turing Machine"):
        st.session_state.tm = TuringMachine(states, input_symbols, tape_symbols, transitions, start_state, accept_states)
        st.session_state.tm.load_input(input_string)
        st.success("Turing Machine initialized!")

    if st.session_state.tm is None:
        st.warning("Please initialize the Turing Machine before running steps.")
    step_button = st.button("Run Step")

    if step_button:
        result = st.session_state.tm.step()
        tape, head_position = st.session_state.tm.display_tape()

        if result == "Accepted":
            st.success(f"Result: {result}")
        elif result == "Rejected":
            st.error(f"Result: {result}")
        else:
            st.write(f"Continue... Current State: {st.session_state.tm.current_state}")

        tape_display = ''.join(['^' if i == head_position else char for i, char in enumerate(tape)])
        st.write(f"Tape: {tape}")
        st.write(f"Head Position: {head_position}")
        st.write(f"Tape with Head Position: {tape_display}")

    if st.button("Reset Turing Machine"):
        st.session_state.tm = None
        st.success("Turing Machine reset!")
