import os
import tiktoken

def process_directory(project_dir, output_file, extensions, level=0, prefix=''):
    if level == 0:
        output_file.write(f"{os.path.basename(project_dir)}\n")
    
    entries = os.listdir(project_dir)
    entries = sorted(entries, key=lambda x: (os.path.isfile(os.path.join(project_dir, x)), x))
    
    for i, entry in enumerate(entries):
        entry_path = os.path.join(project_dir, entry)
        is_last = i == len(entries) - 1
        
        if os.path.isfile(entry_path):
            output_file.write(f"{prefix}{'└── ' if is_last else '├── '}{entry}\n")
            
            if entry.endswith(tuple(extensions)):
                relative_path = os.path.relpath(entry_path, project_dir)
                
                with open(entry_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                output_file.write(f"\nRelative Path: {relative_path}\n")
                output_file.write(code)
                output_file.write("\n\n")
        
        else:
            output_file.write(f"{prefix}{'└── ' if is_last else '├── '}{entry}/\n")
            process_directory(entry_path, output_file, extensions, level + 1, prefix + ('    ' if is_last else '│   '))

def main():
    project_dir = input("Enter the project directory path: ")
    output_path = "project-code.txt"
    
    # Check if the output file already exists
    if os.path.exists(output_path):
        raise FileExistsError(f"The file '{output_path}' already exists. Please choose a different output file name.")
    
    # Specify the file extensions to include
    extensions = ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css']
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        process_directory(project_dir, output_file, extensions)
    
    # Estimate the number of tokens using the cl100k_base tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")
    with open(output_path, 'r', encoding='utf-8') as output_file:
        content = output_file.read()
        num_tokens = len(tokenizer.encode(content))
    
    print(f"Code extracted and saved to {output_path}")
    print(f"Estimated number of tokens: {num_tokens}")

if __name__ == '__main__':
    main()