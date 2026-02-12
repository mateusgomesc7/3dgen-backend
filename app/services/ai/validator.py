REQUIRED_TOKENS = [
    'THREE.Scene',
    'THREE.PerspectiveCamera',
    'WebGLRenderer',
    'requestAnimationFrame',
]

FORBIDDEN_TOKENS = [
    'fetch(',
    'XMLHttpRequest',
    'eval(',
    'Function(',
    'document.cookie',
    'localStorage',
    'window.location',
]


def validate_threejs_code(code: str) -> None:
    for token in REQUIRED_TOKENS:
        if token not in code:
            raise ValueError(f'Missing required Three.js structure: {token}')

    for token in FORBIDDEN_TOKENS:
        if token in code:
            raise ValueError(f'Forbidden API usage detected: {token}')
