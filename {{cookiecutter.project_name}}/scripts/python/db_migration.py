from os import environ
from pathlib import Path
from subprocess import run
from time import sleep
from typing import List, Tuple


class _AlembicMigration:
    def __init__(self):

        # Creates the class-created fields
        self._current_revision_id = self._get_current_revision_id()
        self._revision_history_ids = self._get_revision_history_ids()
        self._target_revision_id = (
            environ.get("TARGET_REVISION_ID") if environ.get("TARGET_REVISION_ID") else None
        )

    @staticmethod
    def _run_alembic_command(command: List[str]) -> str:
        """
        Function that runs an alembic command in a subprocess. The standard output is returned
        once the subprocess has completed. When an error containing the word 'Error:' is returned
        from the subcommand a SystemExit error is raised

        :param command: The alembic command to run

        :returns: The output from the command
        """

        # Runs the alembic command and gets the result
        root_path = Path(__file__).parent / "../../"
        result = run(args=["alembic", *command], cwd=root_path, capture_output=True, text=True)
        if "Error:" in result.stderr:
            raise SystemExit(f"\n{result.stderr}")

        # Returns the output from the command
        return result.stdout

    @property
    def current_revision_id(self) -> str | None:
        """
        Property that gets the current alembic
        revision id being used

        :return The current alembic revision id
        """

        # Returns the current alembic revision id
        return self._current_revision_id

    @property
    def revision_history_ids(self) -> List[str]:
        """
        Property that gets the list of all alembic revision
        ids in chronological order of revision creation

        :return: The list of all alembic revisions ids
        """

        # Returns the list of all alembic revisions ids
        return self._revision_history_ids

    @property
    def revision_placements(self) -> Tuple[int, int]:
        """
        Property that gets the placement of the current and target alembic revisions relative to
        the total revision history. When a current or target revision does not exist a Value error
        is raised

        :returns: the current revision id relative placement, the target evision id relative placement
        """

        # Attempts to get the placement of the revisions relative to the total revision history
        try:
            current_revision_placement = (
                self._revision_history_ids.index(self._current_revision_id)
                if self._current_revision_id
                else -1
            )
            if self._target_revision_id:
                target_revision_placement = self._revision_history_ids.index(
                    self._target_revision_id
                )
                return current_revision_placement, target_revision_placement
            else:
                raise ValueError()
        except ValueError:
            message = (
                f"Error: Revision {self._current_revision_id} or {self._target_revision_id} "
                f"does not exist"
            )
            raise ValueError(message)

    @property
    def target_revision_id(self) -> str | None:
        """
        Property that gets the target
        revision id to migrate to

        :return: The target revision id to migrate to
        """

        # Returns the target revision id to migrate to
        return self._target_revision_id

    def downgrade(self, revision_id: str):
        """
        Function that performs an alembic
        downgrade using the given revision

        :param revision_id: The revision id to downgrade to
        """

        # Performs an alembic upgrade
        self._run_alembic_command(["downgrade", revision_id])

    def upgrade(self, revision_id: str):
        """
        Function that performs an alembic upgrade
        using the given revision

        :param revision_id: The revision id to upgrade to
        """

        # Performs an alembic upgrade
        self._run_alembic_command(["upgrade", revision_id])

    def _get_current_revision_id(self) -> str | None:
        """
        Function that gets the current
        alembic revision id being used

        :return: The current alembic revision id
        """

        # Gets the current alembic revision being used
        output = self._run_alembic_command(["current"])
        current_revision = output.split(" ")[0].replace("\n", "")
        if not current_revision:
            return None

        # Returns the current alembic revision
        return current_revision

    def _get_revision_history_ids(self) -> List[str]:
        """
        Function that gets the list of all alembic revision
        ids in chronological order of revision creation

        :return: The list of all alembic revisions ids
        """

        # Gets the alembic revision history in chronological order
        output = self._run_alembic_command(["history"])

        # Creates a list of revision IDs in the order they appear in the history
        revision_history_ids = []
        for line in output.splitlines():
            if " -> " in line:
                revision_id = line.split(" -> ")[1].split(" ")[0].replace(",", "")
                revision_history_ids.append(revision_id)

        # Returns te list of all alembic revisions ids
        return revision_history_ids


def main():
    """
    Function that runs when the
    migration script begins
    """

    # Shows that the alembic migrations script has started
    print(f"{'*' * 25} Alembic Migration {'*' * 25}")

    # Instantiates the alembic migrations class
    migrations = _AlembicMigration()

    # Gets the current and target revision ids
    current_revision_id = migrations.current_revision_id
    target_revision_id = migrations.target_revision_id

    # Prints the current and target revision ids
    print(f"\nRevisions:")
    print(f"Current Revision Id: {current_revision_id}")
    print(f"Target Revision Id: {target_revision_id}")

    # When no target revision id is given, skip taking
    if target_revision_id is None:
        print("Action Needed: None")
        print("\nMigration:")
        print("No target revision given, skipping migration.")
        return

    # When the current and target revisions are the same, no action is needed
    elif current_revision_id == target_revision_id:
        print("Action Needed: None")
        print("\nMigration:")
        print("Up to date, skipping migration.")
        return

    # Attempts to perform an upgrade or downgrade migration
    try:

        # Gets the placement of the revisions relative to the total revision history
        current_placement, target_placement = migrations.revision_placements

        # When an upgrade migration needs to be performed
        if current_placement > target_placement or current_placement == -1:
            print("Action Needed: Upgrade")
            print("\nMigration:")
            print(f"Upgrading from {current_revision_id} to {target_revision_id}")
            migrations.upgrade(target_revision_id)

        # When a downgrade migration needs to be performed
        else:
            print("Action Needed: Downgrade")
            print("\nMigration:")
            print(f"Downgrading from {current_revision_id} to {target_revision_id}")
            migrations.downgrade(target_revision_id)

    # When an error occurs exit the script
    except Exception as exc:
        print("Action Needed: N/A")
        print("\nMigration:")
        sleep(0.01)
        raise SystemExit(exc)


if __name__ == "__main__":
    main()
