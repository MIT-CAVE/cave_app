import os
import django

# Note: We must first setup django - then we can import and use models or other django features
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cave_app.settings.development"),
)
django.setup()

from cave_core.models import CustomUser, Teams

# An example test that confirms we have setup the DB with at least one user and their personal team.
def test_user_and_personal_team():
    users = CustomUser.objects.all()
    user_count = users.count()
    print(f"Found {user_count} users.")
    assert user_count > 0, "No users found in the database. Ensure a user exists."

    for user in users:
        # A user's personal team should have is_personal_team=True
        # and the user should be a member of it.
        personal_teams = Teams.objects.filter(id__in=user.team_ids, is_personal_team=True)
        print(f"User {user.username} (ID: {user.id}) has {personal_teams.count()} personal team(s).")

        assert personal_teams.exists(), f"User {user.username} does not have a personal team."

        for team in personal_teams:
            # Verify user is indeed in this team
            assert user.id in team.get_user_ids(), f"User {user.username} is not a member of their own personal team {team.name}."

if __name__ == "__main__":
    try:
        test_user_and_personal_team()
        print("Test passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
