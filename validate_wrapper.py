
#!/usr/bin/env python3
import sys
import os
import re
import tempfile
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: validate_wrapper.py <schema_file>")
        sys.exit(1)
    
    schema_file = sys.argv[1]
    if not os.path.exists(schema_file):
        print(f"Error: File {schema_file} does not exist")
        sys.exit(1)
    
    # Read the schema file
    with open(schema_file, 'r') as f:
        content = f.read()
    
    # Create a temporary file with the modified content
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tdg', delete=False) as temp_file:
        # Replace 'schema Name {' with 'schema "Name" {'
        modified_content = re.sub(r'schema\s+(\w+)\s+{', r'schema "\1" {', content)
        temp_file.write(modified_content)
        temp_file_path = temp_file.name
    
    try:
        # Run the validation command on the temporary file
        cmd = ["testdatagen", "validate", temp_file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print the output, but replace the temporary file path with the original file path
        output = result.stdout.replace(temp_file_path, schema_file)
        error = result.stderr.replace(temp_file_path, schema_file)
        
        if output:
            print(output)
        if error:
            print(error, file=sys.stderr)
        
        # Return the exit code
        sys.exit(result.returncode)
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    main()
