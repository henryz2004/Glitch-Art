import random
import glob
import os


header_size = 1000
footer_size = 1500
chunk_range = (200000, 500000)
group_range = (1, 2)
run_id = 8                  # Used for differntiating between output files of different runs


def glitch(source, dest):
    
    header = None
    footer = None

    chunks = []

    current_pos = header_size
    file_size = os.path.getsize(source)

    with open(source, "rb") as image_file:
        header = image_file.read(header_size)      # Skip header_size bytes

        while True:
            if current_pos >= (file_size - footer_size):
                break
            
            chunk_size = random.randint(*chunk_range)

            if current_pos + chunk_size > (file_size - footer_size):
                chunk_size = (file_size - footer_size) - current_pos
                
            chunk = image_file.read(chunk_size)
            chunks.append(chunk)

            current_pos += chunk_size

        footer = image_file.read()

    # Group chunks based on proximity
    groups = []
    chunk_pos = 0

    while True:
        if chunk_pos >= len(chunks):
            break
        
        group_size = random.randint(*group_range)

        group = chunks[chunk_pos:chunk_pos + group_size]
        random.shuffle(group)       # Shuffle chunk group
        groups.append(group)

        chunk_pos += group_size

    # Write it back into a file
    with open(dest, "wb") as write_file:

        write_file.write(header)

        # Write groups to file
        for group in groups:
            for chunk in group:
                write_file.write(chunk)
        
        write_file.write(footer)
            

if __name__ == "__main__":

    src_dir = r'C:\Users\henry\AppData\Local\Programs\Python\Glitch Art\images\*.jpg'
    dest_dir = r'C:\Users\henry\AppData\Local\Programs\Python\Glitch Art\glitched'

    # Find all images in src directory
    images = glob.glob(src_dir)

    for i, image in enumerate(images):
        glitch(image, dest_dir + r'\glitch{}_{}.jpg'.format(i, run_id))
