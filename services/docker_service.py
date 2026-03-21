# services/docker_service.py
"""
Provides Docker container listing utilities for the bot.
"""
import docker

def list_docker_containers():
    """Returns a list of Docker containers (names and status)."""
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)

        if not containers:
            return "No containers found."

        lines = []
        for c in containers:
            lines.append(f"{c.name} ({c.status})")

        return "\n".join(lines)

    except Exception as e:
        return f"Error retrieving Docker containers: {e}"