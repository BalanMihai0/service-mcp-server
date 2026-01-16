# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:alpine3.22

# Setup a non-root user
RUN adduser -D nonroot

# Create a cache directory for uv and give ownership
RUN mkdir -p /home/nonroot/.cache/uv \
    && chown -R nonroot:nonroot /home/nonroot/.cache

# Use the non-root user
USER nonroot

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

ENV UV_CACHE_DIR=/home/nonroot/.cache/uv

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/home/nonroot/.cache/uv,uid=1000,gid=1000 \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app

RUN --mount=type=cache,target=/home/nonroot/.cache/uv,uid=1000,gid=1000 \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

EXPOSE 8420

CMD ["uv", "run", "uvicorn", "app:app", "--host=0.0.0.0", "--port=8420"]