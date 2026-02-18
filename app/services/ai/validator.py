FORBIDDEN_TOKENS = [
    'document.cookie',
    'localStorage',
    'sessionStorage',
    'indexedDB',
]


def validate_threejs_code(code: str) -> None:
    for token in FORBIDDEN_TOKENS:
        if token in code:
            raise ValueError(f'Forbidden API usage detected: {token}')
