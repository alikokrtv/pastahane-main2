class PosRouter:
    """
    Route all database operations for the 'pos' app to the 'viapos' database.
    """
    app_label = 'pos'
    db_name = 'viapos'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            # Never migrate POS models; they are managed=False and live in external DB
            return False
        return None
