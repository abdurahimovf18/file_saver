# use uv images
FROM python:3.13-slim-bookworm
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

# create group and user
RUN addgroup -gid 1000 appgroup \
    && adduser -uid 1000 -gid 1000 appuser

# declare app folder
WORKDIR /app

# Change ownership BEFORE copying files
RUN chown -R appuser:appgroup /app

# copy dependency files
COPY --chown=appuser:appgroup uv.lock pyproject.toml .python-version ./

# install dependencies
RUN uv venv && uv sync --group app

# copy project
COPY --chown=appuser:appgroup . .

# switch user
USER appuser

# expose external port
EXPOSE 8000

# declare entrypoint
ENTRYPOINT ["uv", "run", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
