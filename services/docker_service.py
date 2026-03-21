# services/docker_service.py
"""
Provides Docker container listing utilities for the bot.
"""
import docker

def list_docker_containers():
    """Returns a list of Docker containers with Docker-style status text."""
    try:
        client = docker.from_env()
        containers = client.api.containers(all=True)

        if not containers:
            return "No containers found."

        lines = []
        for c in containers:
            names = c.get("Names", [])
            name = names[0].lstrip("/") if names else "unknown"
            status_text = c.get("Status", "unknown")
            lines.append(f"{name} ({status_text})")

        return "\n".join(lines)

    except Exception as e:
        return f"Error retrieving Docker containers: {e}"