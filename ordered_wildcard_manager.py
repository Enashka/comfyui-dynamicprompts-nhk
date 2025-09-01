"""
Custom WildcardManager that preserves file order instead of sorting alphabetically.
"""
from pathlib import Path
from typing import List


class OrderedWildcardManager:
    """
    WildcardManager that preserves the order of wildcards as they appear in files
    instead of sorting them alphabetically.
    """
    
    def __init__(self, path: Path = None):
        self.path = Path(path) if path else None
    def _load_wildcard_file(self, file_path: Path) -> List[str]:
        """
        Load wildcards from a file, preserving the order they appear in the file.
        Override the parent method to prevent alphabetical sorting.
        """
        if not file_path.exists():
            return []
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Strip whitespace and filter out empty lines and comments
            wildcards = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    wildcards.append(line)
            
            # Return in original file order - DO NOT SORT
            return wildcards
            
        except Exception as e:
            print(f"Error loading wildcard file {file_path}: {e}")
            return []
    
    def get_wildcards(self, wildcard_name: str) -> List[str]:
        """
        Get wildcards for a given wildcard name, preserving file order.
        """
        # Find the wildcard file
        wildcard_file = self._find_wildcard_file(wildcard_name)
        if wildcard_file:
            wildcards = self._load_wildcard_file(wildcard_file)
            print(f"OrderedWildcardManager: '{wildcard_name}' -> First: '{wildcards[0] if wildcards else 'EMPTY'}', Total: {len(wildcards)}")
            return wildcards
        print(f"OrderedWildcardManager: '{wildcard_name}' NOT FOUND")
        return []
    
    def _find_wildcard_file(self, wildcard_name: str) -> Path | None:
        """
        Find the wildcard file for a given wildcard name.
        """
        if not self.path:
            return None
            
        # Try different extensions
        for ext in ['.txt', '.yaml', '.json']:
            file_path = self.path / f"{wildcard_name}{ext}"
            if file_path.exists():
                return file_path
        
        return None
