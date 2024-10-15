
# CMNTR - Code Mixed Note Taking and Retrieval

CMNTR is a command-line tool that allows users to create, index, edit, and search notes written in a code-mixed format of Telugu and English, using Roman script. It offers an efficient way to manage notes where users can search for them using queries in the same code-mixed style.

## Features

- **Create notes** in code-mixed Telugu and English using Roman script.
- **Edit existing notes** to update their content.
- **Index notes** for efficient searching and retrieval.
- **Search notes** using code-mixed queries to find the most relevant results.
- **Delete notes** along with their indexed embeddings.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CMNTR.git
   cd CMNTR
   ```

2. Install the required dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure that the `retrievalAPI.py` and `indexerAPI.py` are located in the `API` directory.

## Usage

Before running any command, navigate to the `/interface` directory:
```bash
cd interface
```

CMNTR provides a set of commands to manage and retrieve notes. You can access these commands through the command-line interface.

### Create a New Note

To create a new note:
```bash
python3 cmntr.py create <filename>
```

### Edit an Existing Note

To edit a note:
```bash
python3 cmntr.py edit <filename> <new_text>
```

### Index a Note

To index a note for searching:
```bash
python3 cmntr.py index_note <filename>
```

### Delete a Note

To delete a note:
```bash
python3 cmntr.py delete <filename>
```

### Query Notes

To search for similar notes using a code-mixed query:
```bash
python3 cmntr.py query "<query_text>"
```

## Example

1. Create a new note:
   ```bash
   python3 cmntr.py create "my_note.txt"
   ```

2. Edit the note:
   ```bash
   python3 cmntr.py edit "my_note.txt" "This is a test note."
   ```

3. Index the note for searching:
   ```bash
   python3 cmntr.py index_note "my_note.txt"
   ```

4. Query the notes:
   ```bash
   python3 cmntr.py query "test note"
   ```

5. Delete the note:
   ```bash
   python3 cmntr.py delete "my_note.txt"
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## Contact

For any questions, feel free to reach out at your-email@example.com.
