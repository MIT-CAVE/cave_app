# Framework Imports
from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal Imports
from cave_api.api import execute_command
from cave_core.models.cache import cache
from cave_core.utils.constants import api_keys, background_api_keys
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster
from cave_utils import Validator

# External Imports
from pamda import pamda


class Sessions(models.Model):
    """
    Model for storing Sessions
    """

    name = models.CharField(_("name"), max_length=128, help_text=_("Name of the session"))
    team = models.ForeignKey(
        "Teams",
        on_delete=models.CASCADE,
        verbose_name=_("team"),
        help_text=_("The associated team"),
    )
    description = models.TextField(
        _("description"),
        max_length=512,
        help_text=_("Description for the session"),
        default="",
        blank=True,
    )

    def broadcast_loading(self, loading: bool) -> None:
        """
        Broadcast the loading status for this session

        Requires:

        - `loading`:
            - Type: bool
            - What: The loading status to broadcast
        """
        CaveWSBroadcaster(self).broadcast(
            event="updateLoading",
            data={
                "data_path": ["session_loading"],
                "data": loading,
            },
        )

    def set_loading(self, value: bool, override_block: bool = False) -> None:
        """
        Set the loading status for this session and broadcast it to all users

        Requires:

        - `value`:
            - Type: bool
            - What: The value to set the executing status to

        Optional:

        - `override_block`:
            - Type: bool
            - What: If True, the session will be unblocked from execution status when set to False even if it was blocked due to execution status
            - Default: False
        """
        self.__dict__["is_executing"] = cache.get(f"session:{self.id}:executing", False)
        if value:
            if self.__dict__["is_executing"]:
                self.broadcast_loading(True)
                # Create a block for the loading state to prevent this error from killing the execution block
                self.__dict__["__blocked_due_to_execution__"] = True
                raise Exception(
                    "Oops! This session is already executing a task. Please wait for it to finish."
                )
            cache.set(f"session:{self.id}:executing", True)
            self.__dict__["is_executing"] = True
            self.broadcast_loading(True)
        else:
            if override_block:
                self.__dict__["__blocked_due_to_execution__"] = False
            if self.__dict__.get("__blocked_due_to_execution__"):
                # Release the block to allow other errors to be thrown and stop the loading state
                self.__dict__["__blocked_due_to_execution__"] = False
            else:
                cache.set(f"session:{self.id}:executing", False)
                self.__dict__["is_executing"] = False
                self.broadcast_loading(False)

    def get_user_ids(self) -> list:
        """
        Gets all user ids for users currently in this session as a list

        Returns:
            type: list
            what: A list of user ids

        Notes:
            - Used to determine which users are in this session
            - EG To broadcast messgaes to everyone in the session
            - EG to prevent deletion if more than one user is in the session
        """
        user_ids = cache.get(f"session:{self.id}:user_ids", None)
        # Auto heal User Ids On Cache Data Loss
        if user_ids == None:
            self.update_user_ids()
            user_ids = cache.get(f"session:{self.id}:user_ids", [])
        return user_ids

    def update_user_ids(self) -> None:
        """
        Gets all user ids for users currently in this session and stores it as a json object in the cache
        """
        CustomUser = apps.get_model("cave_core", "CustomUser")
        cache.set(
            f"session:{self.id}:user_ids",
            list(CustomUser.objects.filter(session=self).values_list("id", flat=True)),
        )

    def get_versions(self) -> dict:
        """
        Gets the current versions object for this session. This object is not dynamic and is only the version state when this function is called

        Returns:
            type: dict
            what: The data keys and their current versions for this session

        Note: Uses a local object for in memory storage of versions to prevent multiple calls to the cache if the session is_executing
              This is because only one session object can be executing at a time and the versions object is only used during execution
        """
        # Used a local object cached versions object to prevent multiple calls to the cache
        versions = self.__dict__.get("versions")
        if self.__dict__.get("is_executing") and versions:
            return versions
        self.__dict__["versions"] = cache.get(f"session:{self.id}:versions", {})
        return dict(self.__dict__["versions"])

    def set_versions(self, versions: dict) -> None:
        """
        Sets the versions object for this session

        Requires:

        - `versions`:
            - Type: dict
            - What: The data keys and their current versions for this session
        """
        cache.set(f"session:{self.id}:versions", versions)
        self.__dict__["versions"] = versions

    def get_data(
        self,
        keys: list[str] = None,
        client_only: bool = True,
        omit_keys=list(),
        create_missing_cache_keys=False,
    ) -> dict:
        """
        Returns all data for this session

        Optional:

        - `keys`:
            - Type: list of strings
            - What: The keys to get data for
            - Default: None
            - Note: If None, all keys are sent
        - `client_only`:
            - Type: bool
            - What: If True, only relevant client keys are returned
            - Default: True
        - `omit_keys`:
            - Type: list of strings
            - What: The keys to omit from the data
            - Default: []
            - Note: If None, no keys are omitted
        - `create_missing_cache_keys`:
            - Type: bool
            - What: If True, the function will create missing cache keys with empty dictionaries
            - Note: This is useful for initializing new data structures
            - Default: False
        Returns:
            - Type: dict
            - What: The related data given the inputs to this function
        """
        if keys == None:
            keys = list(self.get_versions().keys())
        if client_only:
            keys = pamda.intersection(keys, api_keys)
        if len(omit_keys) > 0:
            keys = pamda.difference(keys, omit_keys)
        keys_to_get_from_cache = []
        for key in keys:
            # Avoid additional cache hits by checking if the data is already in the session __dict__
            if not pamda.hasPath(path=["data", key], data=self.__dict__):
                keys_to_get_from_cache.append(key)
        # If there any keys to get from the cache, get them all at once and update the session __dict__
        if len(keys_to_get_from_cache) > 0:
            new_data = cache.get_many(
                [f"session:{self.id}:data:{key}" for key in keys_to_get_from_cache]
            )
            # Get the specific key names from the cache keys
            new_data = {
                key.split(":")[-1]: value for key, value in new_data.items() if value != None
            }
            if create_missing_cache_keys:
                # If creating missing cache keys, fill in any missing keys with empty dictionaries to prevent errors in the client
                for key in keys_to_get_from_cache:
                    if key not in new_data:
                        new_data[key] = {}
                        cache.set(f"session:{self.id}:data:{key}", new_data[key])
            # If the new data is not the same length as the keys to get from the cache, there was an error
            # Likely, some data was lost from the persistent cache
            if len(new_data.keys()) != len(keys_to_get_from_cache):
                CaveWSBroadcaster(self).notify(
                    title="Error:",
                    message="Oops! There was an error with the data from this session. It will be reset to initial values to fix the issue.",
                    theme="error",
                )
                self.set_loading(False, override_block=True)
                self.execute_api_command(command="init", broadcast_changes=True, command_keys=[])
                # Raise an exception to stop the current execution whatever it may be.
                raise Exception("The data error should now be fixed. Please try your action again.")
            for key, value in new_data.items():
                if value != None:
                    # Update the local session __dict__ with the new data to prevent multiple cache hits later
                    pamda.assocPath(path=["data", key], value=value, data=self.__dict__)
        return {key: pamda.path(["data", key], self.__dict__) for key in keys}

    def broadcast_changed_data(
        self, previous_versions: dict, broadcast_loading: bool = True, force_overwrite: bool = False
    ) -> None:
        """
        Broadcasts and returns all data that has changed given some set of previous versions

        Requires:

        - `previous_versions`:
            - Type: dict
            - What: The endpoint provided previous versions to check vs the current server versions to determine which data has changed

        Optional:

        - `broadcast_loading`:
            - Type: bool
            - What: If True, the loading state will be broadcasted to all users before and after the data is broadcasted
            - Default: True
        - `force_overwrite`:
            - Type: bool
            - What: If True, the data will be broadcasted to the client to force an update (even with matching versions) and will trigger reloading client side
            - Default: False
            - Note: Used primarily for switching between sessions

        """
        # print('==BROADCAST CHANGED DATA==')
        # Fill in missing session data if none is present
        versions = self.get_versions()
        # If there is no versions data, initialize the session data and get the new versions
        if len(versions) == 0:
            self.execute_api_command(command="init", broadcast_changes=True, command_keys=[])
            # print('==BROADCAST CHANGED DATA END==\n')
            # Execute API Command calls this function again and it will pass this if statement
            return
        updated_keys = [
            key for key, value in versions.items() if previous_versions.get(key) != value
        ]
        data = self.get_data(client_only=True, keys=updated_keys)
        # Broadcast the updated versions and data

        if broadcast_loading:
            self.broadcast_loading(True)
        # Pass force overwrite as an extra kwarg to keep backwards compatibiiity
        extra_kwargs = {"forceOverwrite": True} if force_overwrite else {}
        CaveWSBroadcaster(self).broadcast(
            event="overwrite",
            versions=versions,
            data=data,
            **extra_kwargs,
        )
        if broadcast_loading:
            self.broadcast_loading(False)
        # print('==BROADCAST CHANGED DATA END==')

    def replace_data(self, data, wipeExisting):
        """
        Replaces data in this session

        Requires:

        - `data`:
            - Type: dict
            - What: The data to be replaced
        - `wipeExisting`:
            - Type: bool
            - What: Boolean to indicate if previously existing data should be wiped

        `data` Example:
        ```
        {
            'data_key_here':{
                'data':{"desired":"data object here"}
            },
            'data2_key_here':{
                'data':{"desired":"data 2 object here"}
            }
            ...
        }
        ```
        """
        # print('==REPLACE DATA==')
        versions = self.get_versions()
        if wipeExisting:
            data_keys = list(data.keys())
            keys_to_delete = pamda.difference(list(versions.keys()), data_keys)
            cache.delete_many(
                [f"session:{self.id}:data:{key}" for key in keys_to_delete],
                memory=True,
                persistent=True,
            )
            for key in keys_to_delete:
                versions.pop(key, None)
        # Update the cache with the new data
        cache.set_many({f"session:{self.id}:data:{key}": value for key, value in data.items()})
        # Store the new data locally in the session __dict__ to prevent multiple cache hits
        for key, value in data.items():
            pamda.assocPath(path=["data", key], value=value, data=self.__dict__)
            versions[key] = versions.get(key, 0) + 1
        # Update versions post replacement
        self.set_versions(versions)
        # print('==REPLACE DATA END==')

    def execute_api_command(
        self,
        command,
        command_keys=None,
        mutate_dict=dict(),
        previous_versions=dict(),
        broadcast_changes=True,
    ):
        """
        Execute an API Command given the current data and replaces the entire current session state

        Requires:

        - `command`:
            - What: A string to pass to the api as the command parameter

        Optional:

        - `command_keys`:
            - Type: list[str]
            - What: List of strings to determine which top level keys should be passed with the command
            - Default: None
            - Note: If None, all keys are sent to the api
        - `mutate_dict`:
            - Type: dict
            - What: A dictionary that provides information on what mutation fired this command
            - Default: {}
        - `previous_versions`:
            - Type: dict
            - What: A dictionary of previous versions to determine what data has changed when broadcasting the changed data to the users
            - Default: {}
        - `broadcast_changes`:
            - Type: bool
            - What: A boolean to determine if the changes should be broadcasted to all users
            - Default: True
        """
        # print('\n==EXECUTE API COMMAND==')
        self.set_loading(True)
        session_data = self.get_data(
            keys=command_keys, client_only=False, omit_keys=background_api_keys
        )
        socket = CaveWSBroadcaster(self)
        command_output = execute_command(
            session_data=session_data, command=command, socket=socket, mutate_dict=mutate_dict
        )
        # Ensure that no reserved api keys are returned
        background_api_keys_used = pamda.intersection(
            list(command_output.keys()), background_api_keys
        )
        if len(background_api_keys_used) > 0:
            raise Exception(
                f"Oops! The following reserved api keys were returned: {str(background_api_keys_used)}"
            )
        # Pop out kwargs for use but not for storage
        extraKwargs = command_output.pop("extraKwargs", command_output.pop("kwargs", {}))
        # Update the session data with the command output
        self.replace_data(
            data=command_output,
            wipeExisting=extraKwargs.get("wipeExisting", settings.DEFAULT_WIPE_EXISTING),
        )

        # Validate if in debug + live api validation mode
        if settings.DEBUG:
            if settings.LIVE_API_VALIDATION_LOG or settings.LIVE_API_VALIDATION_PRINT:
                validator = Validator(
                    session_data=self.get_data(),
                    ignore_keys=["meta"],
                )
                if settings.LIVE_API_VALIDATION_PRINT:
                    validator.log.print_logs(max_count=settings.LIVE_API_VALIDATION_PRINT_MAX)
                if settings.LIVE_API_VALIDATION_LOG:
                    validator.log.write_logs(
                        f"./logs/validation/{self.name}.log",
                        max_count=settings.LIVE_API_VALIDATION_LOG_MAX,
                    )

        # Broadcast the changed data if specified
        if broadcast_changes:
            self.broadcast_changed_data(
                previous_versions=previous_versions, broadcast_loading=False
            )
        # Update the execution state overriding any blocks
        self.set_loading(False, override_block=True)
        # print('==EXECUTE API COMMAND END==\n')

    def mutate(
        self,
        data_version,
        data_name,
        data_path,
        data_value=None,
        ignore_version=False,
        create_missing_cache_keys=False,
    ):
        """
        Mutate a specific data_name inside of this session

        Requires:

        - `data_version`:
            - Type: str
            - What: The current data version to validate synchronization before processing the mutation request
        - `data_name`:
            - Type: str
            - What: The name of the data to mutate
        - `data_path`:
            - Type: list
            - What: The path in the data to mutate at which the new `data_value` should be assigned

        Optional:

        - `data_value`:
            - Type: dict | list
            - What: data to assign to the end of the `data_path` for the item specified by `data_name`
            - Default: None
        - `ignore_version`:
            - Type: bool
            - What: A boolean indicator to specify if the current data version should be considered before processing the mutation request
            - Default: False
        - `create_missing_cache_keys`:
            - Type: bool
            - What: If True, the function will create missing cache keys with empty dictionaries
            - Note: This is useful for creating missing data structures when syncing from local state
            - Default: False
        """
        # print('==MUTATE==')
        data = self.get_data(
            keys=[data_name], client_only=False, create_missing_cache_keys=create_missing_cache_keys
        ).get(data_name)
        versions = self.get_versions()
        if data == None:
            raise Exception(
                "Session Error: No session data found. This could be caused by an incorrect `data_name` or not being in a session."
            )
        if not ignore_version and versions.get(data_name) != data_version:
            return {"synch_error": True}
        self.replace_data(
            data={data_name: pamda.assocPath(path=data_path, value=data_value, data=data)},
            wipeExisting=False,
        )
        # print('==MUTATE END==')

    def get_associated_sessions(self, user=None):
        """
        Gets other sessions associated to the user or team that owns this session.

        - Used to determine if a team or user has reached a session limit
        - Used as helper to get associated session data

        Optional:

        - `user`:
            - Type: User object
            - What: A user object that is used to validate if the requesting user is staff or has multi-team session access
                - If so: This request will also return related group team sessions
            - Default: None
        """
        if user is not None:
            if user.get_multi_team_sessions:
                return Sessions.objects.filter(team__in=user.get_team_ids())
        return Sessions.objects.filter(team=self.team)

    def clone(self, name, description):
        """
        Copies the current session to a new session

        Requires:

        - `name`:
            - Type: str
            - What: The name of the new session based off of this clone
        - `description`:
            - Type: str
            - What: The description of the new session based off of this clone

        Returns:
            - Type: Session object
            - What: The new session object that was created
        """
        session_data = self.get_data(keys=list(self.get_versions().keys()), client_only=False)
        new_session = self
        new_session.name = str(name)
        new_session.description = str(description)
        new_session.pk = None
        new_session.save()
        cache.set_many(
            {f"session:{new_session.id}:data:{key}": value for key, value in session_data.items()}
        )
        new_session.set_versions({key: 0 for key in session_data.keys()})
        return new_session

    def get_cache_keys(self):
        """
        Gets all cache keys for this session
        """
        keys = [f"session:{self.id}:{key}" for key in ["versions", "executing", "user_ids"]]
        keys += [
            f"session:{self.id}:data:{key}"
            for key in list(cache.get(f"session:{self.id}:versions", {}).keys())
        ]
        return keys

    def persist_cache_data(self):
        """
        Persists the current session data to the persistent cache
        """
        cache.persist_many(self.get_cache_keys())

    def error_on_session_not_empty(self):
        """
        Raises an exception if the session is not empty
        """
        if len(self.get_user_ids()) > 0:
            raise Exception("Oops! That session still has users in it.")

    def save(self, *args, **kwargs):
        """
        Special post save event to update the team's session list
        - Note: Only applies when an update field is not specified or includes the session name
        """
        super(Sessions, self).save(*args, **kwargs)
        try:
            self.team.update_sessions_list()
        except:
            pass

    @staticmethod
    def error_on_invalid_name(name):
        """
        Raises an exception if the name is invalid
        """
        if name == None or len(str(name)) < 1:
            raise Exception("Oops! You need to provide a valid session name.")

    # Metadata
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

    # Methods
    def __str__(self):
        return _("{}").format(self.name)
