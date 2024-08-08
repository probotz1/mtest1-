# Constants used for progress display
FINISHED_PROGRESS_STR = "█"
UN_FINISHED_PROGRESS_STR = "░"
EDIT_SLEEP_TIME_OUT = 1  # Time interval (in seconds) to update the progress

# Logger setup (replace with your actual logger setup if needed)
import logging

LOGGER = logging.getLogger(__name__)

# Dictionary to track progress (use in a thread-safe manner if needed)
gDict = {}
