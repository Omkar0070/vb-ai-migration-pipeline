import sys, os

file = sys.argv[1]

if not os.path.exists(file) or os.path.getsize(file) == 0:
    print("Validation failed")
    sys.exit(1)

print("Validation passed")

