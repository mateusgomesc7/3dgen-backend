FORBIDDEN_TOKENS = [
    'eval(',
    'Function(',
    'setTimeout(',
    'setInterval(',
    'document.cookie',
    'localStorage',
    'sessionStorage',
    'indexedDB',
    'window.location',
    'window.parent',
    'window.top',
    '.innerHTML',
    '.outerHTML',
    'document.write',
]


def validate_threejs_code(code: str) -> None:
    for token in FORBIDDEN_TOKENS:
        if token in code:
            raise ValueError(f'Forbidden API usage detected: {token}')
