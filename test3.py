from file_fragmentation import browse_and_fragment
from fragment import Fragment

# Call the browse_and_fragment function
fragments, metadata = browse_and_fragment()

# Print the fragments and metadata
for fragment in fragments:
    print(fragment)


print(metadata)