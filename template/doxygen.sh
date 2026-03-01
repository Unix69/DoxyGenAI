#!/usr/bin/env bash
# ------------------------------------------------------------
# ⚙️ setup_doxygen.sh — Auto-generate and configure Doxygen
# Reads configuration from doxygen.ini
# ------------------------------------------------------------

set -e  # Exit on error

INI_FILE="doxygen.ini"

# --- Check dependencies ---
if ! command -v doxygen &> /dev/null; then
  echo "❌ Doxygen not found. Please install it (sudo apt install doxygen graphviz)."
  exit 1
fi

# --- Create base Doxyfile if missing ---
if [ ! -f Doxyfile ]; then
  echo "🛠️  Generating base Doxyfile..."
  doxygen -g Doxyfile
fi

echo "⚙️  Applying custom configuration..."

# Helper: ensure key=value (override if exists)
set_tag() {
  local key="$1"
  local value="$2"
  if grep -q "^${key}" Doxyfile; then
    sed -i "s|^${key}.*|${key} = ${value}|" Doxyfile
  else
    echo "${key} = ${value}" >> Doxyfile
  fi
}

# --- Read doxygen.ini and apply tags ---
if [ ! -f "$INI_FILE" ]; then
  echo "❌ Configuration file $INI_FILE not found!"
  exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
  # Ignore empty lines or comments
  [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue

  # Parse key=value
  if [[ "$line" =~ ^([A-Za-z0-9_]+)[[:space:]]*=[[:space:]]*\"(.*)\" ]]; then
    key="${BASH_REMATCH[1]}"
    value="${BASH_REMATCH[2]}"
    set_tag "$key" "$value"
  fi
done < "$INI_FILE"

# --- Optional: add default aliases if not already present ---
if ! grep -q "ALIASES" Doxyfile; then
cat <<'EOF' >> Doxyfile

# ---- Custom Aliases ----
ALIASES += fix="🛠️ **FIX:** "
ALIASES += bug="🐞 **BUG:** "
ALIASES += change="🔄 **CHANGE:** "
ALIASES += todo="📝 **TODO:** "
ALIASES += api="🔗 **API:** "
ALIASES += namespace="📦 **NAMESPACE:** "
ALIASES += feature="✨ **FEATURE:** "
EOF
fi

echo "✅ Doxyfile configured successfully!"
echo "📂 Output directory: $(grep OUTPUT_DIRECTORY Doxyfile | awk '{print $3}')"
echo "💡 Run: doxygen Doxyfile"
