#!/bin/bash

# generate-prp-context.sh
# Prepares context for manual PRP generation with any AI assistant

if [ -z "$1" ]; then
    echo "Usage: ./generate-prp-context.sh <feature-file>"
    echo "Example: ./generate-prp-context.sh INITIAL.md"
    exit 1
fi

FEATURE_FILE="$1"
OUTPUT_FILE="prp-context.txt"

echo "=== CONTEXT FOR PRP GENERATION ===" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "FEATURE REQUEST:" >> "$OUTPUT_FILE"
cat "$FEATURE_FILE" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "PROJECT PLANNING:" >> "$OUTPUT_FILE"
cat "PLANNING.md" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "PROJECT RULES:" >> "$OUTPUT_FILE"
cat "CLAUDE.md" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "PRP TEMPLATE:" >> "$OUTPUT_FILE"
cat "PRPs/templates/prp_base.md" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "EXAMPLES:" >> "$OUTPUT_FILE"
if [ -d "examples" ]; then
    find examples -name "*.py" -o -name "*.md" | head -5 | while read file; do
        echo "--- $file ---" >> "$OUTPUT_FILE"
        cat "$file" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    done
fi

echo "Context prepared in $OUTPUT_FILE"
echo "Copy this content to your AI assistant and ask it to generate a PRP"
