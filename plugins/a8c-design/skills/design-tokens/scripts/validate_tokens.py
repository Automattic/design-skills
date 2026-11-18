#!/usr/bin/env python3
"""
Design Token Validator

Validates design token files against DTCG 2025.10 specification rules.

Usage:
    python validate_tokens.py <path>           # Validate file or directory
    python validate_tokens.py tokens/          # Validate all .tokens.json files
    python validate_tokens.py tokens/file.json # Validate single file

Checks:
    - Valid JSON structure
    - Required $value property on tokens
    - Valid $type values
    - Alias reference resolution
    - Circular reference detection
    - Type inheritance from groups
"""

import json
import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, Optional

# Valid DTCG token types
VALID_TYPES = {
    'color',
    'dimension',
    'fontFamily',
    'fontWeight',
    'duration',
    'cubicBezier',
    'number',
    'typography',
    'shadow',
    'border',
    'gradient',
    'transition',
    'strokeStyle'
}

# Valid dimension units
VALID_DIMENSION_UNITS = {'px', 'rem'}

# Valid duration units
VALID_DURATION_UNITS = {'ms', 's'}

# Valid color spaces
VALID_COLOR_SPACES = {
    'srgb', 'srgb-linear', 'display-p3', 'hsl', 'hwb',
    'lab', 'lch', 'oklab', 'oklch', 'xyz', 'xyz-d50',
    'xyz-d65', 'rec2020', 'a98-rgb', 'prophoto-rgb'
}


class TokenValidator:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.tokens: Dict[str, Any] = {}
        self.all_token_paths: Set[str] = set()
    
    def validate_file(self, filepath: str) -> Tuple[List[str], List[str]]:
        """Validate a single token file."""
        self.errors = []
        self.warnings = []
        self.tokens = {}
        self.all_token_paths = set()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return self.errors, self.warnings
        except FileNotFoundError:
            self.errors.append(f"File not found: {filepath}")
            return self.errors, self.warnings
        
        # First pass: collect all token paths
        self._collect_token_paths(data, '')
        
        # Second pass: validate structure and values
        self._validate_node(data, '', inherited_type=None)
        
        # Third pass: validate references
        self._validate_references(data, '')
        
        return self.errors, self.warnings
    
    def _collect_token_paths(self, node: Any, path: str):
        """Collect all token paths for reference validation."""
        if not isinstance(node, dict):
            return
        
        for key, value in node.items():
            if key.startswith('$'):
                continue
            
            child_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                if '$value' in value:
                    self.all_token_paths.add(child_path)
                    self.tokens[child_path] = value
                else:
                    self._collect_token_paths(value, child_path)
    
    def _validate_node(self, node: Any, path: str, inherited_type: Optional[str]):
        """Validate a node in the token tree."""
        if not isinstance(node, dict):
            return
        
        # Check for type inheritance
        node_type = node.get('$type', inherited_type)
        
        # Validate $type if present
        if '$type' in node:
            if node['$type'] not in VALID_TYPES:
                self.errors.append(
                    f"Invalid $type '{node['$type']}' at '{path or 'root'}'. "
                    f"Valid types: {', '.join(sorted(VALID_TYPES))}"
                )
        
        for key, value in node.items():
            if key.startswith('$'):
                continue
            
            child_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                if '$value' in value:
                    # This is a token
                    self._validate_token(value, child_path, node_type)
                else:
                    # This is a group
                    self._validate_node(value, child_path, node_type)
    
    def _validate_token(self, token: Dict[str, Any], path: str, inherited_type: Optional[str]):
        """Validate a single token."""
        token_type = token.get('$type', inherited_type)
        value = token.get('$value')
        
        if value is None:
            self.errors.append(f"Token '{path}' missing required $value property")
            return
        
        # Check for deprecated property
        if '$deprecated' in token:
            deprecated = token['$deprecated']
            if not isinstance(deprecated, (bool, str)):
                self.errors.append(
                    f"Token '{path}' has invalid $deprecated value. "
                    "Must be boolean or string."
                )
        
        # Skip alias tokens for value validation
        if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
            return
        
        # Validate value based on type
        if token_type:
            self._validate_value(value, token_type, path)
    
    def _validate_value(self, value: Any, token_type: str, path: str):
        """Validate a token value against its type."""
        validators = {
            'color': self._validate_color,
            'dimension': self._validate_dimension,
            'fontFamily': self._validate_font_family,
            'fontWeight': self._validate_font_weight,
            'duration': self._validate_duration,
            'cubicBezier': self._validate_cubic_bezier,
            'number': self._validate_number,
            'typography': self._validate_typography,
            'shadow': self._validate_shadow,
            'border': self._validate_border,
            'gradient': self._validate_gradient,
            'transition': self._validate_transition,
            'strokeStyle': self._validate_stroke_style,
        }
        
        validator = validators.get(token_type)
        if validator:
            validator(value, path)
    
    def _validate_color(self, value: Any, path: str):
        """Validate color token value."""
        if isinstance(value, str):
            # Legacy hex format (warn)
            self.warnings.append(
                f"Token '{path}' uses legacy string color format. "
                "Consider using DTCG color object format."
            )
            return
        
        if not isinstance(value, dict):
            self.errors.append(f"Token '{path}' color value must be an object")
            return
        
        if 'colorSpace' not in value:
            self.errors.append(f"Token '{path}' color missing 'colorSpace'")
        elif value['colorSpace'] not in VALID_COLOR_SPACES:
            self.errors.append(
                f"Token '{path}' has invalid colorSpace '{value['colorSpace']}'"
            )
        
        if 'components' not in value:
            self.errors.append(f"Token '{path}' color missing 'components'")
        elif not isinstance(value['components'], list):
            self.errors.append(f"Token '{path}' color components must be an array")
    
    def _validate_dimension(self, value: Any, path: str):
        """Validate dimension token value."""
        if not isinstance(value, dict):
            self.errors.append(f"Token '{path}' dimension must be an object")
            return
        
        if 'value' not in value:
            self.errors.append(f"Token '{path}' dimension missing 'value'")
        
        if 'unit' not in value:
            self.errors.append(f"Token '{path}' dimension missing 'unit'")
        elif value['unit'] not in VALID_DIMENSION_UNITS:
            self.errors.append(
                f"Token '{path}' has invalid unit '{value['unit']}'. "
                f"Valid units: {', '.join(VALID_DIMENSION_UNITS)}"
            )
    
    def _validate_font_family(self, value: Any, path: str):
        """Validate fontFamily token value."""
        if isinstance(value, str):
            return  # Single font name is valid
        
        if not isinstance(value, list):
            self.errors.append(
                f"Token '{path}' fontFamily must be a string or array of strings"
            )
            return
        
        for i, font in enumerate(value):
            if not isinstance(font, str):
                self.errors.append(
                    f"Token '{path}' fontFamily[{i}] must be a string"
                )
    
    def _validate_font_weight(self, value: Any, path: str):
        """Validate fontWeight token value."""
        valid_keywords = {
            'thin', 'hairline', 'extra-light', 'ultra-light', 'light',
            'normal', 'regular', 'book', 'medium', 'semi-bold', 'demi-bold',
            'bold', 'extra-bold', 'ultra-bold', 'black', 'heavy',
            'extra-black', 'ultra-black'
        }
        
        if isinstance(value, str):
            if value.lower() not in valid_keywords:
                self.errors.append(
                    f"Token '{path}' has invalid fontWeight keyword '{value}'"
                )
        elif isinstance(value, (int, float)):
            if not (1 <= value <= 1000):
                self.errors.append(
                    f"Token '{path}' fontWeight must be between 1 and 1000"
                )
        else:
            self.errors.append(
                f"Token '{path}' fontWeight must be a number or keyword string"
            )
    
    def _validate_duration(self, value: Any, path: str):
        """Validate duration token value."""
        if not isinstance(value, dict):
            self.errors.append(f"Token '{path}' duration must be an object")
            return
        
        if 'value' not in value:
            self.errors.append(f"Token '{path}' duration missing 'value'")
        
        if 'unit' not in value:
            self.errors.append(f"Token '{path}' duration missing 'unit'")
        elif value['unit'] not in VALID_DURATION_UNITS:
            self.errors.append(
                f"Token '{path}' has invalid duration unit '{value['unit']}'. "
                f"Valid units: {', '.join(VALID_DURATION_UNITS)}"
            )
    
    def _validate_cubic_bezier(self, value: Any, path: str):
        """Validate cubicBezier token value."""
        if not isinstance(value, list):
            self.errors.append(f"Token '{path}' cubicBezier must be an array")
            return
        
        if len(value) != 4:
            self.errors.append(
                f"Token '{path}' cubicBezier must have exactly 4 values"
            )
            return
        
        for i, v in enumerate(value):
            if not isinstance(v, (int, float)):
                self.errors.append(
                    f"Token '{path}' cubicBezier[{i}] must be a number"
                )
    
    def _validate_number(self, value: Any, path: str):
        """Validate number token value."""
        if not isinstance(value, (int, float)):
            self.errors.append(f"Token '{path}' must be a number")
    
    def _validate_typography(self, value: Any, path: str):
        """Validate typography composite token."""
        if not isinstance(value, dict):
            self.errors.append(f"Token '{path}' typography must be an object")
            return
        
        # All typography properties are optional
        valid_props = {'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing'}
        for key in value:
            if key not in valid_props:
                self.warnings.append(
                    f"Token '{path}' has unknown typography property '{key}'"
                )
    
    def _validate_shadow(self, value: Any, path: str):
        """Validate shadow token value."""
        if isinstance(value, list):
            # Multiple shadows
            for i, shadow in enumerate(value):
                self._validate_single_shadow(shadow, f"{path}[{i}]")
        elif isinstance(value, dict):
            self._validate_single_shadow(value, path)
        else:
            self.errors.append(f"Token '{path}' shadow must be an object or array")
    
    def _validate_single_shadow(self, value: Dict[str, Any], path: str):
        """Validate a single shadow value."""
        required = {'color', 'offsetX', 'offsetY', 'blur'}
        for prop in required:
            if prop not in value:
                self.warnings.append(f"Token '{path}' shadow missing '{prop}'")
    
    def _validate_border(self, value: Any, path: str):
        """Validate border token value."""
        if not isinstance(value, dict):
            self.errors.append(f"Token '{path}' border must be an object")
            return
        
        required = {'color', 'width', 'style'}
        for prop in required:
            if prop not in value:
                self.warnings.append(f"Token '{path}' border missing '{prop}'")
    
    def _validate_gradient(self, value: Any, path: str):
        """Validate gradient token value."""
        if not isinstance(value, list):
            self.errors.append(f"Token '{path}' gradient must be an array of stops")
            return
        
        for i, stop in enumerate(value):
            if not isinstance(stop, dict):
                self.errors.append(f"Token '{path}' gradient stop {i} must be an object")
                continue
            if 'color' not in stop:
                self.errors.append(f"Token '{path}' gradient stop {i} missing 'color'")
            if 'position' not in stop:
                self.errors.append(f"Token '{path}' gradient stop {i} missing 'position'")
    
    def _validate_transition(self, value: Any, path: str):
        """Validate transition token value."""
        if not isinstance(value, dict):
            self.errors.append(f"Token '{path}' transition must be an object")
            return
        
        if 'duration' not in value:
            self.warnings.append(f"Token '{path}' transition missing 'duration'")
    
    def _validate_stroke_style(self, value: Any, path: str):
        """Validate strokeStyle token value."""
        if isinstance(value, str):
            return  # Simple keyword is valid
        
        if isinstance(value, dict):
            if 'dashArray' not in value:
                self.errors.append(
                    f"Token '{path}' strokeStyle object missing 'dashArray'"
                )
        else:
            self.errors.append(
                f"Token '{path}' strokeStyle must be a string or object"
            )
    
    def _validate_references(self, node: Any, path: str, visited: Set[str] = None):
        """Validate token references and detect circular dependencies."""
        if visited is None:
            visited = set()
        
        if not isinstance(node, dict):
            return
        
        for key, value in node.items():
            if key.startswith('$'):
                if key == '$value' and isinstance(value, str):
                    self._validate_reference(value, path, visited.copy())
                continue
            
            child_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                if '$value' in value:
                    val = value['$value']
                    if isinstance(val, str):
                        self._validate_reference(val, child_path, visited.copy())
                else:
                    self._validate_references(value, child_path, visited)
    
    def _validate_reference(self, value: str, path: str, visited: Set[str]):
        """Validate a single reference."""
        if not (value.startswith('{') and value.endswith('}')):
            return
        
        ref_path = value[1:-1]  # Remove braces
        
        # Check for circular reference
        if ref_path in visited:
            self.errors.append(
                f"Circular reference detected: '{path}' -> '{ref_path}'"
            )
            return
        
        visited.add(path)
        
        # Check if reference target exists
        if ref_path not in self.all_token_paths:
            self.errors.append(
                f"Token '{path}' references non-existent token '{ref_path}'"
            )
            return
        
        # Check for chained references
        target = self.tokens.get(ref_path, {})
        target_value = target.get('$value')
        if isinstance(target_value, str) and target_value.startswith('{'):
            self._validate_reference(target_value, ref_path, visited)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_tokens.py <path>")
        print("  path: File or directory containing .tokens.json files")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    validator = TokenValidator()
    
    files_to_validate = []
    if path.is_file():
        files_to_validate.append(path)
    elif path.is_dir():
        files_to_validate.extend(path.rglob('*.tokens.json'))
        files_to_validate.extend(path.rglob('*.tokens'))
    else:
        print(f"Error: Path '{path}' not found")
        sys.exit(1)
    
    if not files_to_validate:
        print(f"No token files found in '{path}'")
        sys.exit(1)
    
    total_errors = 0
    total_warnings = 0
    
    for filepath in sorted(files_to_validate):
        errors, warnings = validator.validate_file(str(filepath))
        
        if errors or warnings:
            print(f"\n{filepath}:")
            for error in errors:
                print(f"  ❌ {error}")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
        else:
            print(f"  ✓ {filepath}")
        
        total_errors += len(errors)
        total_warnings += len(warnings)
    
    print(f"\n{'='*50}")
    print(f"Validated {len(files_to_validate)} file(s)")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")
    
    sys.exit(1 if total_errors > 0 else 0)


if __name__ == '__main__':
    main()
