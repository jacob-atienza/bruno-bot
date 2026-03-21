# services/docker_service.py
"""
Provides Docker container listing utilities for the bot.
"""
import subprocess

def list_docker_containers():
    """Returns a list of running Docker containers (names and status)."""
    try:
        result = subprocess.run([
            "docker", "ps", "--format", "{{.Names}} ({{.Status}})"
        ], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return "Docker not available or permission denied."
        containers = result.stdout.strip().split("\n")
        if not containers or containers == ['']:
            return "No running containers."
        return "\n".join(containers)
    except Exception as e:
        return f"Error retrieving Docker containers: {e}"