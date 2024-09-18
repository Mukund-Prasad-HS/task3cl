import streamlit as st

class WordEditor:
    def __init__(self):
        self.words = []
        self.undo_stack = []
        self.redo_stack = []

    def insert(self, new_words):
        self.undo_stack.append(self.words.copy())
        self.words.extend(new_words.split())
        self.redo_stack.clear()

    def delete(self, num_words):
        if num_words > len(self.words):
            num_words = len(self.words)
        self.undo_stack.append(self.words.copy())
        self.words = self.words[:-num_words]
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.words.copy())
            self.words = self.undo_stack.pop()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.words.copy())
            self.words = self.redo_stack.pop()

    def get_text(self):
        return ' '.join(self.words)

    def get_stacks(self):
        # Convert stacks to human-readable format
        return {
            "Undo Stack": [' '.join(stack) for stack in self.undo_stack],
            "Redo Stack": [' '.join(stack) for stack in self.redo_stack]
        }

# Initialize the session state
if 'editor' not in st.session_state:
    st.session_state.editor = WordEditor()

st.set_page_config(page_title="Word Editor", layout="wide")

st.title('Word-based Text Editor with Undo/Redo')

st.write("**Welcome to the Word Editor!** Use this tool to manage a list of words. You can insert new words, delete existing ones, and use undo/redo functionality to manage your text.")

# Create columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    new_text = st.text_input("Enter words to insert:", placeholder="Type words here...")
    if st.button('Insert'):
        if new_text.strip():
            st.session_state.editor.insert(new_text)
        else:
            st.error("Please enter some words to insert.")

    delete_words = st.number_input("Number of words to delete:", min_value=0, value=0, step=1, format="%d")
    if st.button('Delete'):
        if delete_words > 0:
            st.session_state.editor.delete(int(delete_words))
        else:
            st.error("Please enter a number greater than zero to delete.")

with col2:
    st.button('Undo', on_click=st.session_state.editor.undo, use_container_width=True)
    st.button('Redo', on_click=st.session_state.editor.redo, use_container_width=True)

# Display current text
st.text_area("Current Text:", value=st.session_state.editor.get_text(), height=200, disabled=True)

# Word count
st.write(f"**Word count:** {len(st.session_state.editor.words)}")

# Display undo and redo stacks
st.write("**Undo Stack:**")
undo_stack = st.session_state.editor.get_stacks()["Undo Stack"]
if undo_stack:
    st.selectbox("Select undo state", options=undo_stack, index=len(undo_stack) - 1)
else:
    st.write("Undo stack is empty.")

st.write("**Redo Stack:**")
redo_stack = st.session_state.editor.get_stacks()["Redo Stack"]
if redo_stack:
    st.selectbox("Select redo state", options=redo_stack, index=len(redo_stack) - 1)
else:
    st.write("Redo stack is empty.")
