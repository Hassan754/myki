def get_permissions(obj):
    """
    Generic function for Employee and Team instances that returns a dictionary of all accessible
        items through direct or folder access with the highest access level
    :param obj:  Instance of Employee or Team
    :return: Dictionary in the form {'item_is':{'item':item , 'access_level':access_level},}
    """
    permissions = {}
    through = "Direct" if obj.__class__.__name__ == 'Employee' else f"Team {obj.name}"
    for item_access in obj.items.select_related('item'):
        permissions[str(item_access.item_id)] = {"item": item_access.item, "access_level": item_access.access_level,
                                                 "through": through}

    for folder_access in obj.folders.select_related('folder').prefetch_related('folder__items'):
        for item in folder_access.folder.items.all():
            if str(item.id) not in permissions.keys() or permissions[str(item.id)]['access_level'] \
                    > folder_access.access_level:  # If this item is not added yet  || this item's access level is higher than the previous -> Add it
                permissions[str(item.id)] = {"item": item, "access_level": folder_access.access_level,
                                             "through": f"{through} , Folder {folder_access.folder.name}"}
    return permissions


def get_all_user_permissions(user):
    """
    Get All the items a user can access , directly , in folders , through teams -- Highest accessibility returned
    :param user:
    :return:
    """
    permissions = get_permissions(user)
    through = "Direct"
    for team in user.teams.prefetch_related('items', 'folders').all():
        for item_access in team.items.select_related('item'):
            permissions[str(item_access.item_id)] = {"item": item_access.item, "access_level": item_access.access_level,
                                                     "through": through}

        for folder_access in team.folders.select_related('folder').prefetch_related('folder__items'):
            for item in folder_access.folder.items.all():
                if str(item.id) not in permissions.keys() or permissions[str(item.id)]['access_level'] \
                        > folder_access.access_level:
                    permissions[str(item.id)] = {"item": item, "access_level": folder_access.access_level,
                                                 "through": f"{through} , Folder {folder_access.folder.name}"}
    return list(permissions.values())
