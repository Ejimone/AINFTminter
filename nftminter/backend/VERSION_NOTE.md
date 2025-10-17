# Package Version Note

## Version Conflicts

There are some version conflicts between `eth-brownie` and the backend packages (`fastapi`, `google-generativeai`, etc.).

**This is normal and won't cause issues** because:

- Brownie is used for smart contract deployment (in the root project)
- The backend API runs independently (in the `backend/` folder)

## Solution

When working with:

- **Smart contracts**: Use the root virtual environment
- **Backend API**: The current venv works fine for the API server

If you need to deploy contracts AND run the API simultaneously, consider:

1. Using separate virtual environments
2. Or running them in different terminal sessions

## Current Status

✅ Backend API is fully functional with:

- `google-generativeai` (for Imagen image generation)
- `fastapi` (for REST API)
- All required dependencies

The version warnings can be safely ignored for backend operations.
