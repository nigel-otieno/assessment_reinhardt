class ModelPermissionsMixin(object):
    """
    Model-based permissions methods

    :raises NotImplementedError: When the method hasn't been overwritten
    """

    @classmethod
    def can_browse(cls, user_obj):
        """
        Authorizes view permission - Class (Table) Level
        """
        raise NotImplementedError

    def can_read(self, user_obj):
        """
        Authorizes view permission - Instance (Row) Level
        """
        raise NotImplementedError

    def can_edit(self, user_obj):
        """
        Authorizes instance update permission - Instance (Row) Level
        """
        raise NotImplementedError

    @classmethod
    def can_add(cls, user_obj):
        """
        Authorizes instance creation permission - Class (Table) Level
        """
        raise NotImplementedError

    def can_delete(self, user_obj):
        """
        Authorizes instance deletion permission - Instance (Row) Level
        """
        raise NotImplementedError
